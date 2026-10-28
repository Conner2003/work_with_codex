from pathlib import Path
from playwright.sync_api import sync_playwright
import re, json, base64
ROOT=Path(__file__).resolve().parents[1]
# Chromium runtime in this environment blocks ALL navigation (even localhost/file/data).
# Inject the actual production HTML/CSS/JS into about:blank through CDP instead.
html=(ROOT/'public/index.html').read_text('utf-8')
css=(ROOT/'public/styles.css').read_text('utf-8')
js=(ROOT/'public/app.js').read_text('utf-8')
html=re.sub(r'<link rel="stylesheet"[^>]*>', '',html)
html=re.sub(r'<script defer src="[^"]+"></script>','',html)
for path in sorted((ROOT/'public/assets').glob('*.webp')):
    u='data:image/webp;base64,'+base64.b64encode(path.read_bytes()).decode()
    css=css.replace("./assets/"+path.name,u)
    js=js.replace("./assets/"+path.name,u)

def do(browser, phone=False, consent=True, network=False, network_response=False):
    context=browser.new_context(viewport={'width':390,'height':844} if phone else {'width':1440,'height':900}, device_scale_factor=1, is_mobile=phone, has_touch=phone)
    p=context.new_page()
    p.set_default_timeout(5000)
    print("START", "mobile" if phone else "desktop",flush=True)
    errors=[];external=[]
    p.on('pageerror',lambda e:errors.append(str(e)))
    p.on('request',lambda r:external.append(r.url) if 'ipwho.is' in r.url else None)
    if network_response:
        p.route('https://ipwho.is/', lambda route:route.fulfill(status=200, content_type='application/json', headers={'Access-Control-Allow-Origin':'*'}, body=json.dumps({'success':True,'country':'Taiwan','city':'Taichung','connection':{'isp':'Chunghwa Telecom Co., Ltd.'}})))
    p.set_content(html,wait_until='load');p.add_style_tag(content=css);p.add_script_tag(content=js);print('PHASE entry',flush=True);p.locator('#approachMirror').click()
    assert p.locator('#entryTitle').is_visible()
    p.locator('#readNotice').check()
    if consent:p.locator('#profileNotice').check()
    if network:p.locator('#networkNotice').check()
    p.locator('#acceptNotice').click()
    assert p.locator('.ledger-paper').is_visible()
    if network_response:
        p.wait_for_timeout(300)
        assert '台中' in p.locator('#ledgerRows').inner_text(),p.locator('#ledgerRows').inner_text()
        assert '中華電信' in p.locator('#ledgerRows').inner_text()
    p.screenshot(path=str(ROOT/'tests'/('ledger_mobile.png' if phone else 'ledger_desktop.png')))
    print('PHASE ledger',flush=True);p.locator('#ledgerNext').click();assert '口供' in p.locator('h1').inner_text()
    p.locator('.witness[data-lie="1"]').click();assert '真正的謊言' in p.locator('#witnessAnswer').inner_text()
    print('PHASE witness',flush=True);p.locator('#witnessNext').click();assert '錯向' in p.locator('h1').inner_text() or '回廊' in p.locator('h1').inner_text()
    print('PHASE corridor',flush=True);p.locator('#corridorForward').click();assert p.locator('.ledger-paper').is_visible()
    p.locator('#ledgerNext').click();p.locator('#witnessSkip').click();assert '再試著往前' in p.locator('#corridorForward').inner_text()
    p.locator('#corridorForward').click();assert p.locator('#envelope').is_visible()
    p.locator('#letterOpen').click();assert '這不是第一封' in p.locator('#letterBody').inner_text()
    print('PHASE letter',flush=True);p.locator('#letterNext').click();assert p.locator('#effigyFrame img.base-face').is_visible()
    assert p.locator('#effigyFrame img.base-face').evaluate('(e)=>e.complete&&e.naturalWidth>0')
    p.screenshot(path=str(ROOT/'tests'/('effigy_mobile.png' if phone else 'effigy_desktop.png')))
    p.locator('#dollAsk').click();assert '它恰好沒有動' in p.locator('#faceWhisper').inner_text()
    print('PHASE effigy',flush=True);p.locator('#dollNext').click();assert p.locator('.relic').count()==4
    p.locator('.relic[data-relic="sound"]').click()
    print('PHASE market',flush=True);p.locator('#marketNext').click();p.locator('#radioReveal').click();assert '頻道' not in p.locator('#radioText').inner_text() or len(p.locator('#radioText').inner_text())>3
    p.locator('#radioNext').click();p.locator('#oracleTrace').click()
    message=p.locator('#oraclePersonal').inner_text();assert '廣告' in message or '側寫' in message
    if consent:assert '聲音設備' in message, message
    else:assert '沒有資格' in message,message
    print('PHASE oracle',flush=True);p.locator('#oracleNext').click();assert p.locator('#mirrorImage').is_visible()
    p.locator('#mirrorNext').click();assert p.locator('#burnPile').is_visible()
    print('PHASE gate',flush=True);p.locator('#burnNow').click();p.wait_for_timeout(2000)
    assert '卷宗' not in p.locator('#burnPile').inner_text()
    assert p.locator('#restartExhibition').is_visible()
    p.locator('#restartExhibition').click();assert p.locator('#approachMirror').is_visible()
    # no persistent data stored
    assert not re.search(r'(?:localStorage|sessionStorage)\s*(?:\.|\[|\()', js)  # no API access
    if not network:assert not any('ipwho.is' in x for x in external),external
    assert not errors,errors
    if phone:assert p.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(p.evaluate('document.documentElement.scrollWidth'),p.evaluate('innerWidth'))
    result={'device':'mobile' if phone else 'desktop','consent':consent,'network':network,'runtime_errors':len(errors),'outside_requests':external,'pass':True}
    context.close();return result

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
    checks=[do(browser,phone=True,consent=False,network=False)]
    browser.close()
    print(json.dumps(checks,ensure_ascii=False,indent=2))
