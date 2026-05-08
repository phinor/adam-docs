#!/usr/bin/env node
/*
 * Walks every Markdown file under docs/ and replaces any line containing
 * a YouTube link with an embedded <iframe>. Mirrors the legacy
 * adam-documentation/src/generate.php behaviour: a paragraph containing
 * a YouTube reference is replaced wholesale by the embed, dropping the
 * surrounding "video here" text (which was discarded by the legacy
 * pipeline anyway).
 *
 * Recognised link forms:
 *   https://youtu.be/CODE
 *   http://youtu.be/CODE
 *   https://www.youtube.com/watch?v=CODE
 *   https://www.youtube.com/watch?v%3DCODE   (URL-encoded "=", from
 *                                              Google redirector links)
 *
 * Usage: node embed_youtube.mjs
 */

import fs from 'node:fs';
import path from 'node:path';

const DOCS_DIR = path.resolve (import.meta.dirname, '..', 'docs');

const YT_RE = /https?:\/\/(?:www\.)?youtu(?:be\.com|\.be)\/(?:watch\?v=|watch\?v%3[dD])?([a-zA-Z0-9_\-]+)/;

function listMarkdown (dir) {
    return fs.readdirSync (dir, { withFileTypes: true })
        .filter (entry => entry.isFile () && entry.name.endsWith ('.md'))
        .map (entry => path.join (dir, entry.name));
}

function embed (videoId) {
    return `<div class="video-embed"><iframe src="https://www.youtube.com/embed/${videoId}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`;
}

function processFile (file) {
    const text = fs.readFileSync (file, 'utf8');
    const lines = text.split ('\n');
    const replacements = [];
    const out = [];
    let pendingBlank = false;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        // Markdown-escaped chars (e.g. `\_` for an underscore in the link
        // text) would otherwise truncate our YouTube ID match. Strip
        // backslash escapes before matching; renders identically.
        const unescaped = line.replace (/\\([_*\[\]])/g, '$1');
        const m = unescaped.match (YT_RE);
        if (!m) { out.push (line); continue; }

        // Replace the whole line with a block-level iframe; drop a blank
        // line before/after to ensure it renders as its own block.
        if (out.length && out[out.length - 1] !== '') out.push ('');
        out.push (embed (m[1]));
        pendingBlank = true;
        replacements.push ({ line: i + 1, videoId: m[1] });
    }

    // Make sure the last embed has a trailing blank line if it ended the file.
    if (pendingBlank && out[out.length - 1] !== '') out.push ('');

    if (replacements.length) {
        // Collapse runs of three or more blank lines that we may have
        // introduced (or that already existed near a replacement).
        let collapsed = out.join ('\n').replace (/\n{3,}/g, '\n\n');
        if (!collapsed.endsWith ('\n')) collapsed += '\n';
        fs.writeFileSync (file, collapsed, 'utf8');
    }

    return replacements;
}

function main () {
    const files = listMarkdown (DOCS_DIR);
    let totalEmbeds = 0;
    let totalFiles = 0;

    for (const file of files) {
        const replacements = processFile (file);
        if (!replacements.length) continue;
        totalFiles += 1;
        totalEmbeds += replacements.length;
        console.log (`${path.basename (file)}: ${replacements.length} embed${replacements.length === 1 ? '' : 's'}`);
        for (const r of replacements) console.log (`  line ${r.line}: ${r.videoId}`);
    }

    console.log (`Total: ${totalEmbeds} YouTube link${totalEmbeds === 1 ? '' : 's'} embedded across ${totalFiles} files.`);
}

main ();
