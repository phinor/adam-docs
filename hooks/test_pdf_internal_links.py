"""Tests for hooks/pdf_internal_links.py."""
import sys
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, Destination, DictionaryObject, Fit, FloatObject, NameObject, TextStringObject

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdf_internal_links as links  # noqa: E402


def chapter(url, offset, dests=None):
    return links.Chapter(url=url, offset=offset, dests=dests or {})


class TestChapterAt(unittest.TestCase):
    def setUp(self):
        self.chapters = [chapter('index.html', 0), chapter('grades.html', 4), chapter('subjects.html', 9)]

    def test_first_page_belongs_to_first_chapter(self):
        self.assertEqual(links.chapter_at(self.chapters, 0).url, 'index.html')

    def test_page_inside_a_chapter(self):
        self.assertEqual(links.chapter_at(self.chapters, 6).url, 'grades.html')

    def test_page_on_a_chapter_boundary_starts_the_new_chapter(self):
        self.assertEqual(links.chapter_at(self.chapters, 9).url, 'subjects.html')

    def test_last_chapter_extends_to_the_end(self):
        self.assertEqual(links.chapter_at(self.chapters, 40).url, 'subjects.html')


class TestResolveNamed(unittest.TestCase):
    """A name resolved against the chapter the link sits in, not the manual."""

    def setUp(self):
        # Both chapters have a `settings` heading: 30 heading slugs in the
        # manual are repeated across chapters, and pypdf keeps only one entry
        # per name when it merges, so a shared table would send both links to
        # whichever chapter was appended last.
        self.grades = chapter('grades.html', 4, {'settings': links.Dest(2, 6.0, 327.75)})
        self.subjects = chapter('subjects.html', 9, {'settings': links.Dest(1, 6.0, 500.0)})

    def test_resolves_to_a_page_in_the_manual(self):
        self.assertEqual(links.resolve_named(self.grades, 'settings'), links.Dest(6, 6.0, 327.75))

    def test_the_same_name_resolves_differently_in_another_chapter(self):
        self.assertEqual(links.resolve_named(self.subjects, 'settings'), links.Dest(10, 6.0, 500.0))

    def test_chrome_writes_destination_names_with_a_leading_slash(self):
        self.assertEqual(links.resolve_named(self.grades, '/settings'), links.Dest(6, 6.0, 327.75))

    def test_percent_encoded_name(self):
        marks = chapter('marks.html', 0, {'a b': links.Dest(0, 1.0, 2.0)})
        self.assertEqual(links.resolve_named(marks, 'a%20b'), links.Dest(0, 1.0, 2.0))

    def test_unknown_name_does_not_resolve(self):
        self.assertIsNone(links.resolve_named(self.grades, 'nowhere'))


class TestResolveUrl(unittest.TestCase):
    """The site URLs mkdocs-exporter rewrites relative links into."""

    ROOT = 'https://help.adam.co.za/'

    def setUp(self):
        self.chapters = [
            chapter('index.html', 0),
            chapter('grades.html', 4, {'settings': links.Dest(2, 6.0, 327.75)}),
        ]

    def resolve(self, url):
        return links.resolve_url(self.chapters, url, self.ROOT)

    def test_link_to_a_heading(self):
        self.assertEqual(self.resolve('https://help.adam.co.za/grades.html#settings'), links.Dest(6, 6.0, 327.75))

    def test_link_to_a_page_lands_at_its_first_page(self):
        self.assertEqual(self.resolve('https://help.adam.co.za/grades.html'), links.Dest(4, None, None))

    def test_unknown_heading_falls_back_to_the_chapter(self):
        self.assertEqual(self.resolve('https://help.adam.co.za/grades.html#gone'), links.Dest(4, None, None))

    def test_percent_encoded_path(self):
        self.chapters.append(chapter('a b.html', 9))
        self.assertEqual(self.resolve('https://help.adam.co.za/a%20b.html'), links.Dest(9, None, None))

    def test_page_that_is_not_in_the_manual_stays_a_web_link(self):
        self.assertIsNone(self.resolve('https://help.adam.co.za/assets/logo.png'))

    def test_the_site_homepage_stays_a_web_link(self):
        # `docs/index.md` links to the site root. It is a reference to the
        # website, not a cross-reference, so it keeps pointing there.
        self.assertIsNone(self.resolve('https://help.adam.co.za/'))

    def test_another_host_stays_a_web_link(self):
        self.assertIsNone(self.resolve('https://www.youtube.com/watch?v=abc'))

    def test_mailto_stays_a_web_link(self):
        self.assertIsNone(self.resolve('mailto:help@adam.co.za'))


class TestReadDestinations(unittest.TestCase):
    """What a rendered chapter offers to link to, read back from its PDF."""

    def write(self, destinations):
        path = Path(self.directory.name) / 'chapter.pdf'
        writer = PdfWriter()

        for _ in range(3):
            writer.add_blank_page(width=595, height=842)
        for name, (page, left, top) in destinations.items():
            writer.add_named_destination_object(
                Destination(name, writer.pages[page].indirect_reference, Fit.xyz(left=left, top=top))
            )

        writer.write(str(path))

        return str(path)

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)

    def test_reads_the_page_and_position_of_each_destination(self):
        path = self.write({'settings': (1, 6.0, 327.75), 'top': (0, 0.0, 842.0)})

        self.assertEqual(
            links.read_destinations(path),
            {'settings': links.Dest(1, 6.0, 327.75), 'top': links.Dest(0, 0.0, 842.0)},
        )

    def test_a_chapter_with_no_destinations(self):
        self.assertEqual(links.read_destinations(self.write({})), {})

    def test_names_are_normalised_the_way_a_fragment_is(self):
        # Chrome writes the name with the leading slash of the fragment it came
        # from; a name with a space comes back percent-encoded.
        path = self.write({'/a b': (2, 1.0, 2.0)})

        self.assertEqual(links.read_destinations(path), {'a b': links.Dest(2, 1.0, 2.0)})


class TestRetarget(unittest.TestCase):
    """Rewriting the merged manual's links, the way `save()` does."""

    ROOT = 'https://help.adam.co.za/'

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)

        self.writer = PdfWriter()

        for _ in range(12):
            self.writer.add_blank_page(width=595, height=842)

        # Both chapters have a `settings` heading, as 30 slugs in the manual do.
        self.chapters = [
            chapter('index.html', 0),
            chapter('grades.html', 4, {'settings': links.Dest(2, 6.0, 327.75)}),
            chapter('subjects.html', 9, {'settings': links.Dest(1, 6.0, 500.0)}),
        ]

    def link(self, page, **target):
        """Puts a link annotation on a page of the merged document."""

        annotation = DictionaryObject()
        annotation[NameObject('/Type')] = NameObject('/Annot')
        annotation[NameObject('/Subtype')] = NameObject('/Link')
        annotation[NameObject('/Rect')] = ArrayObject([FloatObject(n) for n in (6, 700, 100, 715)])

        if 'url' in target:
            action = DictionaryObject()
            action[NameObject('/S')] = NameObject('/URI')
            action[NameObject('/URI')] = TextStringObject(target['url'])
            annotation[NameObject('/A')] = action
        else:
            annotation[NameObject('/Dest')] = TextStringObject(target['name'])

        # Attached by hand rather than through `add_annotation()`, which
        # rejects a `/Dest` it did not build itself.
        target_page = self.writer.pages[page]

        if '/Annots' not in target_page:
            target_page[NameObject('/Annots')] = ArrayObject()

        target_page[NameObject('/Annots')].append(annotation)

    def retarget(self):
        """Rewrites the links, then reads the document back as a reader would."""

        count = links.retarget(self.writer, self.chapters, self.ROOT)
        path = Path(self.directory.name) / 'manual.pdf'

        self.writer.write(str(path))

        return count, PdfReader(str(path))

    def destination(self, reader, page, index=0):
        """Where an annotation now points: a place in the manual, or a URL."""

        annotation = reader.pages[page]['/Annots'][index].get_object()

        if '/Dest' not in annotation:
            return annotation['/A']['/URI']

        dest = annotation['/Dest']
        pages = [p.indirect_reference.idnum for p in reader.pages]

        return links.Dest(pages.index(dest[0].idnum), float(dest[2]), float(dest[3]))

    def test_link_to_a_heading_in_another_chapter(self):
        self.link(0, url='https://help.adam.co.za/grades.html#settings')

        _, reader = self.retarget()

        self.assertEqual(self.destination(reader, 0), links.Dest(6, 6.0, 327.75))

    def test_link_without_an_anchor_lands_at_the_top_of_its_chapter(self):
        self.link(0, url='https://help.adam.co.za/subjects.html')

        _, reader = self.retarget()

        self.assertEqual(self.destination(reader, 0), links.Dest(9, 0.0, 842.0))

    def test_a_shared_name_resolves_within_the_chapter_the_link_sits_in(self):
        self.link(5, name='/settings')
        self.link(10, name='/settings')

        _, reader = self.retarget()

        self.assertEqual(self.destination(reader, 5), links.Dest(6, 6.0, 327.75))
        self.assertEqual(self.destination(reader, 10), links.Dest(10, 6.0, 500.0))

    def test_an_external_link_is_left_alone(self):
        self.link(0, url='https://www.youtube.com/watch?v=abc')

        _, reader = self.retarget()

        self.assertEqual(self.destination(reader, 0), 'https://www.youtube.com/watch?v=abc')

    def test_a_site_link_to_something_outside_the_manual_is_left_alone(self):
        self.link(0, url='https://help.adam.co.za/assets/logo.png')

        _, reader = self.retarget()

        self.assertEqual(self.destination(reader, 0), 'https://help.adam.co.za/assets/logo.png')

    def test_counts_the_links_it_rewrote(self):
        self.link(0, url='https://help.adam.co.za/grades.html#settings')
        self.link(5, name='/settings')
        self.link(1, url='https://www.youtube.com/watch?v=abc')

        count, _ = self.retarget()

        self.assertEqual(count, 2)


if __name__ == '__main__':
    unittest.main()
