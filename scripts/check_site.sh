#!/usr/bin/env bash
# Boots every page of the site (EN and ES) in a stubbed DOM and fails on any uncaught error.
# Usage: from the site folder, run: bash scripts/check_site.sh
cd "$(dirname "$0")/.." || exit 1
fail=0
for pg in home publications news post cv about project; do
  for lang in en es; do
    out=$(timeout 30 node scripts/boot_page.js "$lang" observaia "$pg" 2>&1 | grep -E "UNHANDLED|UNCAUGHT|EVAL ERR")
    if [ -n "$out" ]; then echo "FAIL $pg $lang: $out"; fail=1; else echo "ok   $pg $lang"; fi
  done
done
for f in data/*.json; do python3 -c "import json,sys;json.load(open('$f',encoding='utf-8'))" || { echo "FAIL json $f"; fail=1; }; done
node --check assets/app.js || fail=1
exit $fail
