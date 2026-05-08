#!/usr/bin/env node
/*
 * Read scripts/chapters.json (produced by convert.mjs) and append/replace
 * the `nav:` section of mkdocs.yml.
 */

import fs from 'node:fs';
import path from 'node:path';

const REPO_ROOT = path.resolve (import.meta.dirname, '..');
const CHAPTERS_JSON = path.join (REPO_ROOT, 'scripts', 'chapters.json');
const MKDOCS_YML = path.join (REPO_ROOT, 'mkdocs.yml');

const chapters = JSON.parse (fs.readFileSync (CHAPTERS_JSON, 'utf8'));
chapters.sort ((a, b) => a.title.localeCompare (b.title, 'en'));

const navLines = ['nav:'];
for (const c of chapters) {
    const safeTitle = c.title.includes (':') || c.title.includes ('"')
        ? `"${c.title.replace (/"/g, '\\"')}"`
        : c.title;
    navLines.push (`  - ${safeTitle}: ${c.file}`);
}
const navBlock = navLines.join ('\n') + '\n';

let yml = fs.readFileSync (MKDOCS_YML, 'utf8');
yml = yml.replace (/\n# nav is generated[\s\S]*$/, '');
yml = yml.replace (/\nnav:[\s\S]*$/, '');
yml = yml.trimEnd () + '\n\n' + navBlock;
fs.writeFileSync (MKDOCS_YML, yml, 'utf8');
console.log (`Wrote nav with ${chapters.length} entries to ${MKDOCS_YML}`);
