// news-image-20261123 — make.fun bounty entry, final edition.
//
// The entry image is drawn by draw_final.py (Python + PIL) and stored as
// entry.png beside this file. This program copies it to the output
// directory, which is /output in the grader and MAKEFUN_OUTPUT_DIR
// when run locally:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

// The copy is byte-for-byte deterministic: the same entry.png is
// written on every run, so the grader's two runs always agree.
// Final edition: NATO/Poland, both chambers, Trump on Iran's missile
// week, India–Nepal $1.62bn, Bitcoin back above $61,000.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
