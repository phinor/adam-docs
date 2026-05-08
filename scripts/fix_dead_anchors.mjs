#!/usr/bin/env node
/*
 * Walks every Markdown file under docs/ and unwraps internal links whose
 * target anchor doesn't exist anywhere in the corpus. The unwrapped link
 * is replaced with the link text alone, so the prose reads unchanged but
 * no longer offers a click that goes nowhere.
 *
 * Only `#h-*` anchors (the ones our converter emits from Google Docs IDs)
 * are touched; ordinary `#section-name` references generated from heading
 * text are left alone.
 *
 * Usage: node fix_dead_anchors.mjs
 */

import fs from 'node:fs';
import path from 'node:path';

const DOCS_DIR = path.resolve (import.meta.dirname, '..', 'docs');

const HREF_RE = /\[([^\]]+)\]\(((?:[a-z0-9-]+\.md)?#h-[a-z0-9]+)\)/gi;
const ANCHOR_DECL_RE = /\{#([a-z0-9-]+)\}/gi;

function listMarkdown (dir) {
    const out = [];
    for (const entry of fs.readdirSync (dir, { withFileTypes: true })) {
        if (entry.isFile () && entry.name.endsWith ('.md')) {
            out.push (path.join (dir, entry.name));
        }
    }
    return out;
}

function buildAnchorIndex (files) {
    const index = new Map (); // file basename -> Set<anchor>
    for (const file of files) {
        const base = path.basename (file);
        const anchors = new Set ();
        const text = fs.readFileSync (file, 'utf8');
        for (const m of text.matchAll (ANCHOR_DECL_RE)) anchors.add (m[1]);
        index.set (base, anchors);
    }
    return index;
}

function fix (file, index) {
    const base = path.basename (file);
    const text = fs.readFileSync (file, 'utf8');
    const fixes = [];

    const replaced = text.replace (HREF_RE, (whole, linkText, href) => {
        const [targetFile, anchor] = href.includes ('#')
            ? [href.split ('#')[0] || base, href.split ('#')[1]]
            : [href, ''];
        const targetAnchors = index.get (targetFile);
        if (targetAnchors && targetAnchors.has (anchor)) return whole;
        fixes.push ({ linkText, href });
        return linkText;
    });

    if (fixes.length) fs.writeFileSync (file, replaced, 'utf8');
    return fixes;
}

function main () {
    const files = listMarkdown (DOCS_DIR);
    const index = buildAnchorIndex (files);
    let totalFixed = 0;
    for (const file of files) {
        const fixes = fix (file, index);
        if (!fixes.length) continue;
        console.log (`${path.basename (file)}: unwrapped ${fixes.length} dead link${fixes.length === 1 ? '' : 's'}`);
        for (const f of fixes) console.log (`  "${f.linkText}" -> ${f.href}`);
        totalFixed += fixes.length;
    }
    console.log (`Total: ${totalFixed} dead links unwrapped across ${files.length} files.`);
}

main ();
