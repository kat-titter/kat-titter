#!/usr/bin/env python3
"""Verify that the [n] publication numbers on page 1 match the order of the page-2 list."""
import re,sys
for f in sys.argv[1:] or ['resume.html']:
    s=open(f,encoding='utf-8').read()
    p2=s.split('<div class="page p2">')[1]
    pubs=re.split(r'<h2>',p2)[1]  # first page-2 section = peer-reviewed publications
    entries=re.findall(r'<li>(.*?)</li>',pubs,re.S)
    def key(e):
        j=re.search(r'<i>([^<]+)</i>\. (\d{4})',e); return f'{j.group(1)} {j.group(2)}'
    order={key(e):i+1 for i,e in enumerate(entries)}
    bad=[]
    for j,n in re.findall(r'(?:<p class="pubs">|</span>)([A-Za-z][A-Za-z ]+? \d{4}) <span class="ref">\[(\d+)\]</span>',s):
        if order.get(j)!=int(n): bad.append((j,n,order.get(j)))
    print(f, 'refs OK' if not bad else f'MISMATCH {bad}')
    if bad: sys.exit(1)
