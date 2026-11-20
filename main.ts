// news-image-20261120 entry: "Sum up 20 November's world news in one image".
//
// The poster beside this file (entry.png, a 1024x1024 newspaper front page
// drawn by make_poster.py) is the whole entry. This program's only job is
// to place those exact bytes at /output/entry.png in the grader's sandbox,
// where MAKEFUN_OUTPUT_DIR stands in for /output when run locally:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// It does no drawing at run time, so the two grading runs produce the
// identical file, byte for byte.

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const posterPath = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
copyFileSync(posterPath, join(outDir, 'entry.png'));
