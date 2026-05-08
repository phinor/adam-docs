#!/usr/bin/env node
/*
 * Identify markdown lines that are inline warning/danger callouts inherited
 * from the Google Doc — an icon image at the start of a paragraph followed
 * by italic text — and rewrite them as `!!! warning` / `!!! danger`
 * admonitions. The icon images themselves are deleted from the chapter
 * asset directory along the way.
 *
 * The Google Doc used three distinct icon images, each appearing many
 * times. Their per-chapter copies in docs/assets/screenshots/ all share
 * the same bytes as the source, so we identify them by SHA-256 hash.
 *
 * Usage: node convert_admonitions.mjs
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const DOCS_DIR = path.resolve (import.meta.dirname, '..', 'docs');
const ASSETS_ROOT = path.join (DOCS_DIR, 'assets', 'screenshots');

// Hashes of the three marker icons in the original Google Docs export.
const ICON_TYPE = new Map ([
    ['2ec511d4bbaf4e0c07d292ef8bc4f5df305c12e4215d1f8782d0a90a1ab1e069', 'warning'],
    ['ae0166b14bf626cfbd11cbcc2140d40b2e2a5fe6f4cf32d42cb54b2c58870214', 'warning'],
    ['3389edbab37c05df12d136fc62aca06b1450616332409c98e76f3f2f4f3415aa', 'danger'],
]);

function sha256 (file) {
    return crypto.createHash ('sha256').update (fs.readFileSync (file)).digest ('hex');
}

function indexIcons () {
    const map = new Map (); // relative-path-from-docs -> 'warning' | 'danger'
    if (!fs.existsSync (ASSETS_ROOT)) return map;
    for (const dir of fs.readdirSync (ASSETS_ROOT, { withFileTypes: true })) {
        if (!dir.isDirectory ()) continue;
        const chapterDir = path.join (ASSETS_ROOT, dir.name);
        for (const file of fs.readdirSync (chapterDir)) {
            const full = path.join (chapterDir, file);
            const type = ICON_TYPE.get (sha256 (full));
            if (!type) continue;
            const rel = `assets/screenshots/${dir.name}/${file}`;
            map.set (rel, { type, full });
        }
    }
    return map;
}

function indent (text, by = '    ') {
    return text.split ('\n').map (l => l.length ? by + l : l).join ('\n');
}

function processFile (file, iconMap, deletions) {
    const text = fs.readFileSync (file, 'utf8');
    const lines = text.split ('\n');
    const out = [];
    const conversions = [];

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        // Match a line that *starts* with an image tag whose src is a known icon.
        const m = line.match (/^!\[[^\]]*\]\(([^)]+)\)\s*(.*)$/);
        if (!m) { out.push (line); continue; }

        const imgPath = m[1];
        const tail = m[2];
        const icon = iconMap.get (imgPath);
        if (!icon) { out.push (line); continue; }

        // Strip a leading bold-italic-italic wrapping from the tail so the
        // body of the admonition is plain prose. Preserve the *italic*
        // boundary inside the body intact otherwise.
        let body = tail.trim ();
        body = body.replace (/^\*\*\*([\s\S]*)\*\*\*$/, '***$1***'); // leave bold-italic alone
        const wrapped = body.match (/^\*([\s\S]*)\*$/);
        if (wrapped && !wrapped[1].includes ('*')) body = wrapped[1].trim ();

        const admonition = [`!!! ${icon.type}`, indent (body), ''];

        // Drop a leading blank line we'd be doubling up.
        if (out.length && out[out.length - 1] !== '') out.push ('');
        out.push (...admonition);

        conversions.push ({ line: i + 1, type: icon.type });
        deletions.add (icon.full);
    }

    if (conversions.length) {
        let collapsed = out.join ('\n').replace (/\n{3,}/g, '\n\n');
        if (!collapsed.endsWith ('\n')) collapsed += '\n';
        fs.writeFileSync (file, collapsed, 'utf8');
    }

    return conversions;
}

function listMarkdown (dir) {
    return fs.readdirSync (dir, { withFileTypes: true })
        .filter (e => e.isFile () && e.name.endsWith ('.md'))
        .map (e => path.join (dir, e.name));
}

function main () {
    const iconMap = indexIcons ();
    console.log (`Indexed ${iconMap.size} marker-icon copies across the asset tree.`);

    const deletions = new Set ();
    let totalConversions = 0;
    let filesTouched = 0;

    for (const file of listMarkdown (DOCS_DIR)) {
        const conversions = processFile (file, iconMap, deletions);
        if (!conversions.length) continue;
        filesTouched += 1;
        totalConversions += conversions.length;
        const summary = conversions.reduce ((acc, c) => {
            acc[c.type] = (acc[c.type] || 0) + 1;
            return acc;
        }, {});
        const parts = Object.entries (summary).map (([t, n]) => `${n} ${t}`).join (', ');
        console.log (`${path.basename (file)}: ${parts}`);
    }

    for (const f of deletions) fs.unlinkSync (f);

    console.log (`Total: ${totalConversions} admonition${totalConversions === 1 ? '' : 's'} across ${filesTouched} file${filesTouched === 1 ? '' : 's'}; ${deletions.size} icon image${deletions.size === 1 ? '' : 's'} removed.`);
}

main ();
