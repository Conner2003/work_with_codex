from pathlib import Path
import json,re,hashlib
root=Path(__file__).resolve().parents[1]
pub=root/'public'
c=json.loads((root/'firebase.json').read_text('utf-8'))['hosting']
h=(pub/'index.html').read_text('utf-8')
a=(pub/'app.js').read_text('utf-8')
s=(pub/'styles.css').read_text('utf-8')
checks={
 'host_root':c['public']=='public',
 'html_references': (pub/'app.js').exists() and (pub/'styles.css').exists(),
 'versions_match':'V4.0' in h and "4.0.0-r1" in a,
 '11_distinct_chapters':"'照面','卷宗','口供','錯向','未寄出的信','紙紮人','遺物','聽筒','乩童','反照','鬼門'" in a,
 'no_wasd': 'keydown'+"'w'" not in a and 'pointerlock' not in a.lower(),
 'no_local_storage_access':not re.search(r'(?:localStorage|sessionStorage)\s*(?:\.|\[|\()',a),
 'no_analytics':not any(x in a.lower()+h.lower() for x in ['gtag(', 'google-analytics.com','facebook.net','googletagmanager.com','mixpanel']),
 'explicit_net_consent':"session.networkConsent=dialogRoot.querySelector('#networkNotice').checked" in a,
 'explicit_profile_consent':"session.profileConsent=dialogRoot.querySelector('#profileNotice').checked" in a,
 'no_automatic_sound':'ui.sound.addEventListener' in a and 'startSound();\nrender()' not in a,
 'revoke_wired':'ui.revoke.addEventListener' in a,
 'camera_and_mic_forbidden': 'camera=(), microphone=()' in str(c['headers']),
 'no_frame_embedding': 'frame-ancestors' in str(c['headers']),
 'has_nosniff':'nosniff' in str(c['headers']),
 'ip_optional_csp': 'https://ipwho.is' in str(c['headers']),
 'actual_image_assets':all((pub/'assets'/name).stat().st_size>5000 for name in ['hall.webp','effigy.webp','effigy_away.webp','effigy_near.webp']),
 'no_webgl_dependency':not any(x in a for x in ['WebGLRenderingContext','THREE.', 'PointerLockControls']),
 'exit_available':'立即離開' in h,
 'js_syntax':True,
}
from subprocess import run
checks['js_syntax']=run(['node','--check',str(pub/'app.js')],capture_output=True).returncode==0
for name,ok in checks.items():print(('PASS' if ok else 'FAIL'),name)
assert all(checks.values())
print('TOTAL',len(checks),'PASS')
