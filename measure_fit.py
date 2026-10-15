#!/usr/bin/env python3
"""Print-layout fit check: page heights (budget 1056px = 11in) and any wrapped one-line rows on page 1."""
import subprocess,re,sys,os,tempfile
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
f=sys.argv[1] if len(sys.argv)>1 else 'resume.html'
s=open(f,encoding='utf-8').read()
s=re.sub(r'@media screen[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}','',s)        # drop screen-only rules
s=s.replace('.page{ width:8.5in; height:11in;','.page{ width:8.5in; height:auto;').replace('overflow:hidden;','overflow:visible;')
s=s.replace('</body>','<script>document.body.innerHTML="<pre id=m>"+[...document.querySelectorAll(".page")].map(p=>Math.round(p.getBoundingClientRect().height)).join(",")+"|"+[...document.querySelectorAll(".page.first ul.b li, .page.first .entry-head")].map(e=>Math.round(e.getBoundingClientRect().height)).join(",")+"</pre>";</script></body>')
fd,tmp=tempfile.mkstemp(suffix='.html'); os.write(fd,s.encode()); os.close(fd)
out=subprocess.run([CH,'--headless=new','--disable-gpu','--window-size=1400,3000','--dump-dom','file://'+tmp],capture_output=True,text=True).stdout
os.remove(tmp)
pages,rows=re.search(r'<pre id="m">([^<]+)',out).group(1).split('|')
pages=[int(x) for x in pages.split(',')]; rows=[int(x) for x in rows.split(',')]
ok=all(p<=1052 for p in pages) and max(rows)<=20
print(f'{f}: page heights {pages} (budget 1056) | tallest row {max(rows)}px | {"OK" if ok else "OVER or WRAPPED"}')
sys.exit(0 if ok else 1)
