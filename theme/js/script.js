/*
 * ADAM Help nav script — adapted from the legacy display.js.
 *
 * Behaviour:
 *   - On load, mark the current page's <li> as .selected and scroll it
 *     into view in the nav.
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
        var path = window.location.pathname.split ('/').pop ();
        return path || 'index.html';
    }

    function findActiveLink (page) {
        var selector = 'nav a[href$="/' + page + '"], nav a[href="' + page + '"]';
        return document.querySelector (selector);
    }

    function highlightActivePage () {
        var page = currentPagePath ();
        var link = findActiveLink (page);
        if (!link) return;
        var li = link.closest ('li');
        if (!li) return;
        li.classList.add ('selected');
        if (li.scrollIntoView) {
            li.scrollIntoView ({ block: 'nearest', behavior: 'auto' });
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
        bindNavToggle ();
    });
}) ();
