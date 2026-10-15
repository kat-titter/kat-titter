#!/usr/bin/env python3
"""Keep publication numbering consistent.
- every page-1/experience journal tag "Journal YYYY [n]" must point at entry n of the publication list
- every #pubN link must have a matching id
- resume and CV must list the same DOIs in the same order
"""
import re,sys
def pubs_of(s):
    sec=s.split('Peer-reviewed publications',1)[1].split('<h2>',1)[0]
    return re.findall(r'<li[^>]*>(.*?)</li>',sec,re.S)
def check(f):
    s=open(f,encoding='utf-8').read(); entries=pubs_of(s); bad=[]
    order={}
    for i,e in enumerate(entries):
        j=re.search(r'<i>([^<]+)</i>\. (\d{4})',e); order[f'{j.group(1)} {j.group(2)}']=i+1
    for j,n in re.findall(r'(?:<p class="pubs">|</span>)([A-Za-z][A-Za-z ]+? \d{4}) <span class="ref">(?:<a[^>]*>)?\[(\d+)\]',s):
        if order.get(j)!=int(n): bad.append(('tag',j,n,order.get(j)))
    ids=set(re.findall(r'id="(pub\d+)"',s))
    for t in re.findall(r'href="#(pub\d+)"',s):
        if t not in ids: bad.append(('missing anchor',t))
    print(f, 'refs OK' if not bad else f'MISMATCH {bad}')
    return [re.search(r'doi\.org/([^"]+)"',e).group(1) for e in entries], bad
d1,b1=check('resume.html'); d2,b2=check('cv.html')
same=d1==d2; print('resume and CV publication order', 'match' if same else f'DIFFER {d1} vs {d2}')
sys.exit(0 if not b1 and not b2 and same else 1)
