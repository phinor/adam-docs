#!/usr/bin/env node
/*
 * Convert the Google Docs HTML export of the ADAM instruction manual into
 * one Markdown file per chapter. Handles:
 *   - bold/italic CSS classes (auto-discovered) to <strong>/<em>
 *   - Word-path alt text on images (dropped)
 *   - Google Docs heading IDs ("h.xxxxx") preserved as MkDocs anchors
 *     via attr_list ({#h-xxxxx}); cross-references rewritten with
 *     correct chapter targets when they cross page boundaries.
 *   - per-chapter image copying with renamed sequential filenames
 *
 * Usage: node convert.mjs [SOURCE_DIR]
 *   SOURCE_DIR defaults to /tmp/adam-docs-source
 */

import fs from 'node:fs';
import path from 'node:path';
import * as cheerio from 'cheerio';
import TurndownService from 'turndown';

const SOURCE_DIR = process.argv[2] || '/tmp/adam-docs-source';
const SOURCE_HTML = path.join (SOURCE_DIR, 'ADAMInstructionManual.html');
const SOURCE_IMAGES = path.join (SOURCE_DIR, 'images');

const REPO_ROOT = path.resolve (import.meta.dirname, '..');
const DOCS_DIR = path.join (REPO_ROOT, 'docs');
const ASSETS_DIR = path.join (DOCS_DIR, 'assets', 'screenshots');
const NAV_OUT = path.join (REPO_ROOT, 'scripts', 'chapters.json');

const WINDOWS_PATH_RE = /^[A-Z]:\\/i;

function slugify (text) {
    return (text || '').trim ().toLowerCase ()
        .replace (/[‘’“”]/g, '')
        .replace (/&/g, ' and ')
        .replace (/[^a-z0-9]+/g, '-')
        .replace (/^-+|-+$/g, '');
}

function ensureUnique (slug, used) {
    if (!used.has (slug)) { used.add (slug); return slug; }
    let n = 2;
    while (used.has (`${slug}-${n}`)) n += 1;
    const s = `${slug}-${n}`;
    used.add (s);
    return s;
}

function discoverFormattingClasses (html) {
    const styleMatch = html.match (/<style[^>]*>([\s\S]*?)<\/style>/);
    const css = styleMatch ? styleMatch[1] : '';
    const classes = { bold: new Set (), italic: new Set () };
    const ruleRe = /\.(c\d+)\s*\{([^}]+)\}/g;
    let m;
    while ((m = ruleRe.exec (css)) !== null) {
        const [, cls, body] = m;
        const compact = body.replace (/\s+/g, '');
        if (compact.includes ('font-weight:700')) classes.bold.add (cls);
        if (compact.includes ('font-style:italic')) classes.italic.add (cls);
    }
    return classes;
}

function chapterSlices (bodyHtml) {
    const re = /<h1\b[^>]*>/g;
    const positions = [];
    let m;
    while ((m = re.exec (bodyHtml)) !== null) positions.push (m.index);
    positions.push (bodyHtml.length);
    const slices = [];
    for (let i = 0; i < positions.length - 1; i++) {
        slices.push (bodyHtml.slice (positions[i], positions[i + 1]));
    }
    return slices;
}

const docsAnchorOf = (gid) => 'h-' + gid.slice (2); // "h.xxxx" -> "h-xxxx"

function buildAnchorMap (slices) {
    const map = new Map ();
    const usedSlugs = new Set ();
    const chapters = [];
    for (const slice of slices) {
        const $ = cheerio.load (`<div id="root">${slice}</div>`, null, false);
        const title = $('h1').first ().text ().trim ();
        if (!title) continue;
        const slug = ensureUnique (slugify (title), usedSlugs);
        chapters.push ({ title, slug, html: slice });
        $('[id]').each ((_, el) => {
            const id = $(el).attr ('id');
            if (!id || !id.startsWith ('h.')) return;
            map.set (id, { chapterSlug: slug, anchor: docsAnchorOf (id) });
        });
    }
    return { map, chapters };
}

function buildTurndown () {
    const td = new TurndownService ({
        headingStyle: 'atx',
        bulletListMarker: '-',
        codeBlockStyle: 'fenced',
        emDelimiter: '*',
        hr: '---',
    });
    td.remove (['style', 'script']);

    td.addRule ('headingsWithAnchor', {
        filter: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
        replacement: (content, node) => {
            const level = Number (node.nodeName[1]);
            const prefix = '#'.repeat (level);
            const anchor = node.getAttribute ('data-anchor');
            const text = content.trim ().replace (/\n+/g, ' ');
            const tail = anchor ? ` {#${anchor}}` : '';
            return `\n\n${prefix} ${text}${tail}\n\n`;
        },
    });

    td.addRule ('strippedSpan', {
        filter: 'span',
        replacement: (content) => content,
    });

    return td;
}

function processChapter (chapter, anchorMap, formatting, td) {
    const $ = cheerio.load (`<div id="root">${chapter.html}</div>`, null, false);

    // 1) Promote bold/italic spans to <strong>/<em> before stripping classes.
    $('span').each ((_, el) => {
        const $el = $(el);
        const cls = ($el.attr ('class') || '').split (/\s+/);
        const isBold = cls.some (c => formatting.bold.has (c));
        const isItalic = cls.some (c => formatting.italic.has (c));
        if (isBold && isItalic) {
            $el.replaceWith (`<strong><em>${$el.html () || ''}</em></strong>`);
        } else if (isBold) {
            $el.replaceWith (`<strong>${$el.html () || ''}</strong>`);
        } else if (isItalic) {
            $el.replaceWith (`<em>${$el.html () || ''}</em>`);
        }
    });

    // 2) Translate heading IDs to a data-anchor attribute that our turndown
    //    rule will emit as `{#h-xxxx}`. Also unwrap any <strong>/<em> we
    //    promoted inside headings — heading text is already styled.
    $('h1, h2, h3, h4, h5, h6').each ((_, el) => {
        const $el = $(el);
        const id = $el.attr ('id');
        if (id && id.startsWith ('h.')) {
            $el.attr ('data-anchor', docsAnchorOf (id));
        }
        $el.find ('strong, em').each ((_, inner) => {
            const $inner = $(inner);
            $inner.replaceWith ($inner.html () || '');
        });
    });

    // 3) Rewrite internal cross-reference links.
    $('a[href^="#h."]').each ((_, el) => {
        const $a = $(el);
        const href = $a.attr ('href') || '';
        const gid = href.slice (1); // drop leading "#"
        const target = anchorMap.get (gid);
        if (!target) {
            $a.attr ('href', `#${docsAnchorOf (gid)}`);
            return;
        }
        if (target.chapterSlug === chapter.slug) {
            $a.attr ('href', `#${target.anchor}`);
        } else {
            $a.attr ('href', `${target.chapterSlug}.md#${target.anchor}`);
        }
    });

    // 4) Drop Word-path alt text and absolute file path titles.
    $('img').each ((_, el) => {
        const $img = $(el);
        const alt = $img.attr ('alt') || '';
        if (WINDOWS_PATH_RE.test (alt) || alt.includes ('AppData')) {
            $img.attr ('alt', '');
        }
    });

    // 5) Copy referenced images, rename per chapter, rewrite src.
    const assetDir = path.join (ASSETS_DIR, chapter.slug);
    let imgIdx = 0;
    let copied = 0;
    let missing = 0;
    $('img').each ((_, el) => {
        imgIdx += 1;
        const $img = $(el);
        const src = $img.attr ('src') || '';
        if (!src.startsWith ('images/')) return;
        const sourceFile = path.join (SOURCE_IMAGES, path.basename (src));
        if (!fs.existsSync (sourceFile)) {
            console.warn (`  MISSING ${sourceFile} (chapter "${chapter.title}")`);
            missing += 1;
            return;
        }
        if (!fs.existsSync (assetDir)) fs.mkdirSync (assetDir, { recursive: true });
        const newName = `${chapter.slug}-${String (imgIdx).padStart (2, '0')}.png`;
        fs.copyFileSync (sourceFile, path.join (assetDir, newName));
        copied += 1;
        $img.attr ('src', `assets/screenshots/${chapter.slug}/${newName}`);
        $img.removeAttr ('style');
        $img.removeAttr ('title');
        $img.removeAttr ('width');
        $img.removeAttr ('height');
    });

    // 6) Strip remaining decorative attrs.
    $('[style]').removeAttr ('style');
    $('[class]').removeAttr ('class');
    $('[id]').each ((_, el) => {
        const id = $(el).attr ('id');
        if (id && (id.startsWith ('cmnt') || id.startsWith ('h.'))) {
            $(el).removeAttr ('id');
        }
    });

    const cleanedHtml = $('#root').html () || '';
    let md = td.turndown (cleanedHtml);

    md = md.replace (/ /g, ' ');
    md = md.replace (/[ \t]+\n/g, '\n');
    md = md.replace (/\n{3,}/g, '\n\n').trim () + '\n';

    const mdPath = path.join (DOCS_DIR, `${chapter.slug}.md`);
    fs.writeFileSync (mdPath, md, 'utf8');

    return { copied, missing };
}

function clean () {
    if (fs.existsSync (ASSETS_DIR)) fs.rmSync (ASSETS_DIR, { recursive: true });
    fs.mkdirSync (ASSETS_DIR, { recursive: true });
    for (const f of fs.readdirSync (DOCS_DIR)) {
        if (f.endsWith ('.md')) fs.rmSync (path.join (DOCS_DIR, f));
    }
}

function main () {
    if (!fs.existsSync (SOURCE_HTML)) {
        console.error (`Source HTML not found: ${SOURCE_HTML}`);
        process.exit (1);
    }
    if (!fs.existsSync (DOCS_DIR)) fs.mkdirSync (DOCS_DIR, { recursive: true });
    clean ();

    const html = fs.readFileSync (SOURCE_HTML, 'utf8');
    const formatting = discoverFormattingClasses (html);
    console.log (`Bold classes: ${[...formatting.bold].join (',') || '(none)'}`);
    console.log (`Italic classes: ${[...formatting.italic].join (',') || '(none)'}`);

    const $ = cheerio.load (html);
    const bodyHtml = $('body').html () || '';
    if (!bodyHtml) {
        console.error ('No <body> content found');
        process.exit (1);
    }

    const slices = chapterSlices (bodyHtml);
    console.log (`Found ${slices.length} chapter slices.`);

    const { map: anchorMap, chapters } = buildAnchorMap (slices);
    console.log (`Anchor map size: ${anchorMap.size}`);

    const td = buildTurndown ();
    const navOut = [];
    let totalCopied = 0;
    let totalMissing = 0;

    for (const chapter of chapters) {
        const { copied, missing } = processChapter (chapter, anchorMap, formatting, td);
        totalCopied += copied;
        totalMissing += missing;
        navOut.push ({ title: chapter.title, file: `${chapter.slug}.md` });
    }

    fs.writeFileSync (NAV_OUT, JSON.stringify (navOut, null, 2));
    console.log (`Wrote ${chapters.length} chapters, copied ${totalCopied} images${totalMissing ? `, ${totalMissing} missing` : ''}.`);
}

main ();
