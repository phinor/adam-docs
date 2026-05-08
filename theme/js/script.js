/*
 * ADAM Help nav script — adapted from the legacy display.js.
 *
 * Behaviour:
 *   - On load, identify the current page by URL and:
 *       - mark its <li> with the .selected class (highlight)
 *       - expand the parent section so its menu2 is visible
 *       - scroll the nav so the selected item is in view
 *   - Toggle a section's menu2 when its label is clicked.
 *   - Toggle the mobile nav overlay when #navtoggle is clicked, and
 *     close the overlay automatically when an in-nav link is followed.
 */

(function () {
    'use strict';

    function ready (fn) {
        if (document.readyState !== 'loading') fn ();
        else document.addEventListener ('DOMContentLoaded', fn);
    }

    function currentPagePath () {
        // We use use_directory_urls: false in mkdocs.yml, so each page is
        // served at /foo.html. Match against just the final path segment.
        var path = window.location.pathname.split ('/').pop ();
        return path || 'index.html';
    }

    function findActiveLink (page) {
        // Try exact match first, then any link whose href ends with the
        // page filename (handles the index page being served as "/").
        var selector = 'nav a[href$="/' + page + '"], nav a[href="' + page + '"]';
        return document.querySelector (selector);
    }

    function highlightActivePage () {
        var page = currentPagePath ();
        var link = findActiveLink (page);
        if (!link) return;
        var li = link.closest ('li');
        if (li) li.classList.add ('selected');
        var section = link.closest ('li.section');
        if (section) section.classList.add ('expanded');
        // Bring the selected item into the visible area of the nav.
        if (li && li.scrollIntoView) {
            li.scrollIntoView ({ block: 'nearest', behavior: 'auto' });
        }
    }

    function bindSectionToggles () {
        var labels = document.querySelectorAll ('nav .section-label');
        for (var i = 0; i < labels.length; i++) {
            labels[i].addEventListener ('click', function (ev) {
                var section = ev.currentTarget.closest ('li.section');
                if (section) section.classList.toggle ('expanded');
            });
        }
    }

    function bindNavToggle () {
        var btn = document.getElementById ('navtoggle');
        var nav = document.querySelector ('nav');
        if (!btn || !nav) return;
        btn.addEventListener ('click', function () {
            var open = nav.classList.toggle ('open');
            btn.setAttribute ('aria-expanded', open ? 'true' : 'false');
        });
        // Close the mobile overlay when an in-nav link is clicked.
        var links = nav.querySelectorAll ('a');
        for (var i = 0; i < links.length; i++) {
            links[i].addEventListener ('click', function () {
                nav.classList.remove ('open');
                btn.setAttribute ('aria-expanded', 'false');
            });
        }
    }

    ready (function () {
        highlightActivePage ();
        bindSectionToggles ();
        bindNavToggle ();
    });
}) ();
