# V4.0.0-r1 開發與驗證報告

## 實作與原版差異

V3 重構候選版的主要問題是畫面仍像低解析度 FPS，後續展間仍在共享簡易 3D 走廊。本版從頭以攝影式固定鏡頭、室內文件、紙張互動、事件重訪與推理為中心。不依賴 WebGL，不含 WASD、Pointer Lock、raycaster 或 FPS 移動系統。合計 11 個段落、4 個本地 WebP 圖像資產，環境聲由 Web Audio 即時合成。

## 已執行的實際檢查

- `node --check public/app.js`: **PASS**。
- `tests/static_checks.py`: **19/19 PASS**，涵蓋 Hosting、公用檔案、版本識別、場景數、外部分析、儲存與資料同意、資產、基礎安全設定。
- `tests/desktop_e2e.py`: **PASS**，1440×900，真實 Chromium DOM；完整操作鏡子、入境同意、卷宗、口供、回到上一頁且第二次通關、拆信、紙紮人、遺物、收音機、乩童、反照、焚毀及重新開始；模擬 IP 回覆台中／中華電信。JavaScript runtime errors：0。
- `tests/mobile_e2e.py`: **PASS**，390×844，真實 Chromium DOM；拒絕行為側寫、11 段全程、沒有個人化品牌廣告、螢幕無橫向捲動、網路第三方請求為 0；JS errors：0。
- `tests/privacy_controls.py`: **3/3 PASS**：同意後中途撤回且乩童不能沿用原側寫；行動裝置 reduced-motion＋主動聲音控制＋立即清除離開；IP 第三方查詢失敗時不杜撰城市和電信商。
- `tests/visual_smoke.py`: **PASS**，桌面和手機入口截圖、渲染與布局檢查，修正了 V4 首輪入口橫向溢出與過暗問題。
- ZIP CRC 完整性及 SHA-256 清單：打包階段驗證後記錄。

**測試方法限制：** 目前環境的 Chromium 由系統政策封鎖了 localhost／file://／data: 導覽，因此在 about:blank 使用 DevTools 插入正式 HTML/CSS/JS，同樣透過真實瀏覽器事件點擊與觸控路徑，不是單純 Mock JS function，但**不能確認 Firebase CDN 交付、HTTP CSP 真實行為、IP 服務實際 CORS、音效主觀聽感**。

## 尚待完成的使用者環境驗收

- 真正 Firebase HTTPS 站台部署及更新，含 Cache-Control 等 Headers。
- 不同手機型號的 Web Audio 實際聽感與聲壓適切性。
- 實際 IP 查詢結果（而非模擬資料）與失敗重試體驗。
- 真人觀展的心理恐怖強度／節奏評估。此項屬主觀使用者驗收，不能假稱自動測試通過。

## 安全限制

固定提供靜音、低動態及立即離開。故意錯向僅一次，第二次可以通關，並有繞過路徑。心理驚悚演出不可超越真實用戶對系統功能的知情同意；不宣稱能讀 IG 搜尋歷史／真實地址，不在其未同意下建立廣告興趣側寫。轉場後的 JS 記憶體可清除，但不宣稱服務提供者的日誌也已刪除。
