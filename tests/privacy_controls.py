"""Real Chromium DOM/privacy/controls tests by injecting production files into about:blank.
Reason: runtime Chromium navigation to localhost/file/data is blocked by administrator.
Does NOT verify Firebase HTTP headers, real ISP results or subjective horror effect.
"""
from pathlib import Path
import re,base64
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
h=(root/'public/index.html').read_text()
h=re.sub(r'<link rel="stylesheet"[^>]*>','',h)
h=re.sub(r'<script defer src="[^"]+"></script>','',h)
css=(root/'public/styles.css').read_text()
js=(root/'public/app.js').read_text()
for p in (root/'public/assets').glob('*.webp'):
 u='data:image/webp;base64,'+base64.b64encode(p.read_bytes()).decode()
 css=css.replace('./assets/'+p.name,u)
 js=js.replace('./assets/'+p.name,u)

def load(browser,mobile=False,reduced=False):
 c=browser.new_context(viewport={'width':390,'height':844} if mobile else {'width':1280,'height':850},is_mobile=mobile,has_touch=mobile,reduced_motion='reduce' if reduced else 'no-preference')
 p=c.new_page();p.set_default_timeout(4000)
 errors=[];out=[]
 p.on('pageerror',lambda e:errors.append(str(e)))
 p.on('request',lambda r:out.append(r.url) if 'ipwho.is' in r.url else None)
 p.set_content(h);p.add_style_tag(content=css);p.add_script_tag(content=js)
 return c,p,errors,out
with sync_playwright() as w:
 b=w.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 # Consent and voluntary withdrawal: profile must disappear from the on-page oracle.
 c,p,errors,out=load(b)
 p.locator('#approachMirror').click();p.locator('#readNotice').check();p.locator('#profileNotice').check();p.locator('#acceptNotice').click()
 assert p.locator('#revoke').is_visible()
 p.locator('#revoke').click();assert p.locator('#revoke').is_hidden()
 assert p.locator('.ledger-paper').is_visible()
 p.locator('#ledgerNext').click();p.locator('#witnessSkip').click();p.locator('#corridorForward').click()
 p.locator('#ledgerNext').click();p.locator('#witnessSkip').click();p.locator('#corridorForward').click()
 p.locator('#letterNext').click();p.locator('#dollNext').click();p.locator('.relic[data-relic="sound"]').click()
 p.locator('#marketNext').click();p.locator('#radioNext').click();p.locator('#oracleTrace').click()
 assert '沒有資格' in p.locator('#oraclePersonal').inner_text()
 assert not out and not errors,(out,errors)
 c.close();print('PASS: revoke immediately prevents profile ads; no network calls')
 # Reduced motion + audio only by a deliberate user click; exit clears session.
 c,p,errors,out=load(b,mobile=True,reduced=True)
 assert p.evaluate('document.body.classList.contains("reduce-motion")')
 assert p.locator('#sound').get_attribute('aria-pressed')=='false'
 p.locator('#sound').click()
 assert p.locator('#sound').get_attribute('aria-pressed') in ('true','false')
 p.locator('#leave').click();assert '此處無人' in p.locator('h1').inner_text()
 assert not out and not errors,(out,errors)
 c.close();print('PASS: reduced-motion, explicit sound, emergency exit')
 # Unreachable third-party API after affirmative opt-in is not treated as fact.
 c,p,errors,out=load(b)
 p.route('https://ipwho.is/',lambda route:route.abort())
 p.locator('#approachMirror').click();p.locator('#readNotice').check();p.locator('#networkNotice').check();p.locator('#acceptNotice').click()
 p.wait_for_timeout(400)
 assert '台中' not in p.locator('#ledgerRows').inner_text()
 assert '中華電信' not in p.locator('#ledgerRows').inner_text()
 assert len(out)==1,(out,errors)
 assert not errors,errors
 c.close();print('PASS: ISP failure creates no guessed city/operator')
 b.close()
