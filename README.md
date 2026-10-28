# 《陰間戶政事務所》Yin Registry V4.0 — Psychological Rebuild

**專案性質：** 可獨立部署到 Firebase Hosting 的原創、固定視角、心理恐怖與數位隱私教育互動網站。版本標識 `4.0.0-r1`，**不是 V3.0 的 FPS 改版**。

## 核心體驗

- **入口「照面」：** 真實攝影風格的廢樓、遠端鏡面、跟隨游標的低幅視差。**沒有 WASD、虛擬搖桿、偽 3D 牆面。** 對鏡子互動才展開入境告示。
- **卷宗：** 文字、螢幕、時間等瀏覽器資訊以自然繁體中文呈現。城市／電信商僅在訪客另行同意且第三方回覆有證據時才出現。
- **口供：** 指認三則說法中的不可能能力，逐步揭露一般網站不能任意讀取 Instagram 搜尋紀錄。
- **錯向回廊：** 第一次選擇往前，故意回到卷宗；第二次可順利通過。保留明確跳過途徑，不能困住訪客。
- **未寄出的信：** 可用觸控／滑鼠拖曳揭開，亦可按「直接攤開」。信件能響應先前的回廊行為。
- **紙紮人：** 寫實攝影人偶、分層眼部、微幅跟隨滑鼠、低頻隨機不一致的表情及視線錯位。尊重 reduced-motion。
- **遺物：** 觀眾可用停留或選擇留下本網站內的興趣訊號，**僅在事前同意後**記錄興趣；不送去廣告平台。
- **收音機：** 類比 FM 調頻，環境聲會隨頻率改變；結合已發生的站內行為回應。
- **乩童：** 以真人常遇到的精準廣告現象為題，先推理再顯示基於**本站行為**的模擬投放。拒絕分析即不個人化。
- **反照與鬼門：** 回放當次可用的線索、揭露哪些屬事實／推論、真正清除本頁 JS 記憶體。會說明伺服器或 IP 查詢供應商的存取日誌不在可刪範圍。

全站共 **11 個段落（入口加十室）**，故事與素材為原創，參考心理恐怖／不可靠敘事手法，不直接搬用他人作品。

## 部署到 Firebase Hosting

ZIP 完整解壓後，在本目錄執行（Windows CMD）：

```cmd
firebase.cmd login
firebase.cmd projects:list
firebase.cmd deploy --only hosting --project "你實際存在的FirebaseProjectID"
```

也可使用 `deploy-windows.cmd 專案ID`。請確保目前目錄含 `firebase.json`；不要使用先前範例專案 ID。若專案已有網站，部署會更新該 Hosting 站台。**部署成功後，頂端應顯示 `SESSION / V4.0`，首頁「無須填寫。」；若不是，請檢查目錄、Firebase 專案與快取。**

本網站不需要 Node.js runtime、Firebase Auth、Firestore、Cloud Functions 或外部 JavaScript CDN。`public` 可直接以任意靜態伺服器託管，HTTPS 對網路查詢較合適。使用者同意記錄存在於瀏覽器頁面的執行期間，不跨頁保存。

## 隱私界線

- 「本頁互動側寫」為獨立選填同意；不同意仍可走完整段故事，乩童不可使用個人化遺物結果。
- 「IP 大略城市／ISP」亦為獨立選填同意；只有勾選才會送出 `https://ipwho.is/` 請求。該供應商將接收到用戶的對外 IP；結果可能不準、資料庫可能失效，不能當 GPS 或真實所在地。
- 本站不讀取其他站的 Cookie／跨站搜尋歷史、不索取攝影機或麥克風，不寫 localStorage／sessionStorage／識別 Cookie，不整合網站流量分析。
- 撤回同意會清除當次已記錄的選擇、停留、推論與查詢結果，並阻止後續側寫；不可撤回第三方**已收到**的 HTTP 請求或代為清除 Hosting／CDN 網路存取日誌。
- 在「鬼門」焚毀或按「立即離開」後清除瀏覽器此頁的相關狀態。這是虛構展覽，不是測試訪客電腦是否被監控。

## 使用與無障礙

滑鼠、觸控、鍵盤皆可互動。可以隨時點擊「立即離開」。背景聲以 Web Audio 合成，必須由使用者主動按「啟用環境聲」開始；預設靜音。遵守 `prefers-reduced-motion`，亦可手動降低動態。拖曳信封有點擊與鍵盤替代方式，謎題都可跳過，避免強迫訪客完成恐怖環節。

## 驗證

執行以下本地測試：

```
node --check public/app.js
python tests/static_checks.py
python tests/desktop_e2e.py
python tests/mobile_e2e.py
python tests/privacy_controls.py
python tests/visual_smoke.py
```

注意：目前測試環境 Chromium 被政策封鎖了 `localhost`、`file://` 甚至 `data:` 網頁導覽，E2E 使用瀏覽器 DevTools 在 `about:blank` 注入**相同的正式版** HTML/CSS/JS 與本地圖片，這能驗證 DOM、程式與版型，但不是 Firebase 網路部署／CSP 真實驗收。詳細結果在 `VALIDATION.md`。

另須在用戶實際 Firebase HTTPS 站台驗證手機瀏覽器的 Web Audio 音量、端對端第三方 IP 查詢、Cookie／網路政策設定（目前並未寫 Cookie）及使用者的心理體驗。**無法用單元測試保證「恐懼」已達成**。
