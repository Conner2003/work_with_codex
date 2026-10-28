from pathlib import Path
from playwright.sync_api import sync_playwright
import re,base64
r=Path(__file__).resolve().parents[1]
html=(r/'public/index.html').read_text('utf-8')
html=re.sub(r'<link rel="stylesheet"[^>]*>', '',html)
html=re.sub(r'<script defer src="[^"]+"></script>','',html)
css=(r/'public/styles.css').read_text('utf-8')
js=(r/'public/app.js').read_text('utf-8')
for p in (r/'public/assets').glob('*.webp'):
 u='data:image/webp;base64,'+base64.b64encode(p.read_bytes()).decode()
 css=css.replace('./assets/'+p.name,u)
 js=js.replace('./assets/'+p.name,u)
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for mobile in [False,True]:
  page=b.new_page(viewport={'width':390,'height':844} if mobile else {'width':1440,'height':900},is_mobile=mobile,has_touch=mobile)
  page.set_content(html);page.add_style_tag(content=css);page.add_script_tag(content=js)
  page.wait_for_timeout(1200)
  page.screenshot(path=str(r/'tests'/('entry_mobile.png' if mobile else 'entry_desktop.png')))
  print('screenshot entry',mobile,page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'))
  page.close()
 b.close()
