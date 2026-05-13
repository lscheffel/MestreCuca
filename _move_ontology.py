#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move all N3-*.md and N4-*.md from project root to data/ontology/"""
import os
import shutil
import glob
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    base = os.getcwd()
    print(f"Base: {base}", flush=True)

    dest = os.path.join(base, 'data', 'ontology')
    os.makedirs(dest, exist_ok=True)

    # Collect all N3 and N4 .md files in root
    root_files = []
    for f in os.listdir(base):
        if (f.startswith('N3-') or f.startswith('N4-')) and f.endswith('.md'):
            root_files.append(os.path.join(base, f))

    print(f"Found {len(root_files)} N3/N4 files in root", flush=True)

    moved = 0
    errors = []
    for src in root_files:
        basename = os.path.basename(src)
        dst = os.path.join(dest, basename)
        try:
            if os.path.exists(dst):
                os.remove(src)
                print(f"  Removed duplicate: {basename}", flush=True)
            else:
                shutil.move(src, dst)
                moved += 1
        except Exception as e:
            errors.append(f"{basename}: {e}")
            print(f"  ERROR {basename}: {e}", flush=True)

    print(f"\nMoved {moved} files to data/ontology/", flush=True)
    if errors:
        print(f"Errors ({len(errors)}):", flush=True)
        for e in errors:
            print(f"  {e}", flush=True)

    # Verify
    remaining = [f for f in os.listdir(base) if (f.startswith('N3-') or f.startswith('N4-')) and f.endswith('.md')]
    print(f"\nRemaining in root: {len(remaining)}", flush=True)
    if remaining:
        for f in remaining:
            print(f"  STILL IN ROOT: {f}", flush=True)

    in_dest = [f for f in os.listdir(dest) if f.startswith('N3-') or f.startswith('N4-')]
    print(f"In data/ontology/: {len(in_dest)}", flush=True)

    # Write status file
    with open(os.path.join(base, '_move_status.txt'), 'w', encoding='utf-8') as sf:
        sf.write(f"moved={moved}\n")
        sf.write(f"errors={len(errors)}\n")
        sf.write(f"remaining={len(remaining)}\n")
        sf.write(f"in_dest={len(in_dest)}\n")

    print("\nDone.", flush=True)

if __name__ == '__main__':
    main()