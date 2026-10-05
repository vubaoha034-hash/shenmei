"""Recover the unchanged V29 maker recipe; never overwrite an existing artwork.

The public maker source intentionally runs only in its original private path.
This thin entry prepares that path in a fresh checkout. --run is allowed only
before a poster exists. Photograph/font acquisition remains a separate step.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    base = root / 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29'
    contract = json.loads((base / 'ROOT_FROZEN_INPUT_CONTRACT.json').read_text('utf-8'))
    refs = {Path(x['path']).name: x for x in contract['production_inputs']}
    dest = root / '.liu-visual-private/shanyeji-v29-production'
    prepared = []
    for name in ('build_v29.py', 'render_svg.cjs'):
        source = root / refs[name]['path']
        raw = source.read_bytes()
        if hashlib.sha256(raw).hexdigest() != refs[name]['sha256']:
            raise ValueError('SEALED_SOURCE_CHANGED:' + name)
        target = dest / name
        if target.exists():
            if target.read_bytes() != raw:
                raise ValueError('EXISTING_RECIPE_DIFFERS:' + name)
        else:
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        prepared.append(name)
    if args.run:
        if (dest / 'poster.png').exists():
            raise ValueError('PRESERVED_ARTWORK_EXISTS: use a fresh checkout; no overwrite')
        for key in ('photography', 'font', 'brand_source', 'reference'):
            item = contract[key]
            target = root / item['path']
            if not target.is_file():
                raise FileNotFoundError('RESTORE_REQUIRED:' + item['path'])
            if hashlib.sha256(target.read_bytes()).hexdigest() != item['sha256']:
                raise ValueError('RESTORED_INPUT_CHANGED:' + key)
        subprocess.run([sys.executable, '-X', 'utf8', '-B', str(dest / 'build_v29.py')],
                       cwd=root, check=True)
    print(json.dumps({'result': 'RECIPE_READY', 'prepared': prepared,
                      'executed': args.run, 'artwork_overwritten': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
