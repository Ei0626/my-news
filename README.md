# 每日全球快覽

每天自動抓取 AI、台海、科技、總經新聞，部署在 GitHub Pages。

## 📁 檔案結構

```
/
├── index.html              # 主頁面
├── data/
│   └── news.json           # 自動產生的新聞資料
├── scripts/
│   └── fetch_news.py       # 抓取 RSS 的 Python 腳本
└── .github/
    └── workflows/
        └── update.yml      # GitHub Actions 排程
```

## 🚀 部署步驟

### 1. 建立 GitHub Repo
在 GitHub 新建一個 public repo（例如 `my-news`）。

### 2. 上傳檔案
把所有檔案推上去：
```bash
git init
git add .
git commit -m "init"
git remote add origin https://github.com/你的帳號/my-news.git
git push -u origin main
```

### 3. 開啟 GitHub Pages
- 進入 repo → Settings → Pages
- Source 選 **Deploy from a branch**
- Branch 選 **main**，資料夾選 **/ (root)**
- 儲存後等 1～2 分鐘，就會有網址

### 4. 確認 Actions 權限
- 進入 repo → Settings → Actions → General
- 往下找 **Workflow permissions**
- 選 **Read and write permissions** → 儲存

### 5. 手動跑一次確認
- 進入 repo → Actions → Daily News Update
- 點 **Run workflow** → Run workflow
- 等約 30 秒，看到綠色勾勾就成功

之後每天早上 9 點（台灣時間）會自動執行。

## 🛠 自訂新聞來源

編輯 `scripts/fetch_news.py` 裡的 `FEEDS` 清單：
```python
{
    "category": "自訂分類名稱",
    "sources": [
        {"name": "來源名稱", "url": "RSS_URL"},
    ]
}
```

## 📌 注意事項
- 新聞資料每天更新一次，非即時
- 行情由 TradingView widget 提供
- 跑馬燈行情為靜態示範數字，請以實際行情為準
