# Cheat Meal Picker Spec

## 1. Product Summary

### Product Name
Cheat Meal Picker

### One-line Pitch
輸入今天想放縱的熱量額度，快速得到幾組合理又有爽感的 cheat meal 建議。

### Problem
正在減脂或控制飲食的人，常常會安排每週一次 cheat meal，但真正要吃的時候很容易陷入選擇障礙：

- 不知道吃什麼最爽
- 不知道怎麼抓熱量
- 想吃得開心，但又不想完全失控

### Target User

- 有在減脂、控制熱量或計算飲食的人
- 每週想安排 1 次 cheat meal 的人
- 想要快速決定「今天到底要吃什麼」的人

## 2. Product Goal

讓使用者在 30 秒內，根據指定熱量與偏好，選到一組今天想吃的 cheat meal。

## 3. Non-goals

第一版不做以下內容：

- 不做精準營養師等級分析
- 不串接外送平台或真實下單
- 不做登入會員
- 不做定位找附近店家
- 不做完整飲食追蹤系統
- 不做個人化減脂課表

## 4. MVP Scope

### User Input

使用者可以輸入或選擇：

- 目標熱量，例如 `1500 kcal`
- 餐點類型，例如 `速食 / 超商 / 日式 / 台式 / 甜點混搭`
- 可選偏好，例如：
  - 想吃炸的
  - 想喝飲料
  - 想吃甜的
  - 不吃牛

### System Output

系統回傳 3 到 5 組 cheat meal 建議，每組包含：

- 餐點組合名稱
- 品項清單
- 預估總熱量
- 預估總價格
- 簡短推薦理由

### Example Output

1. 大麥克 + 6 塊麥克雞塊 + 中薯 + 中杯可樂
   - 約 `1370 kcal`
   - 爽感高，適合想吃經典速食的人

2. 三片披薩 + 兩塊炸雞 + 可樂
   - 約 `1560 kcal`
   - 更接近重口味派對餐，適合真的想放飛一天

3. 鮭魚生魚片拼盤 + 鮪魚鮭魚丼 + 麻糬冰淇淋
   - 約 `1180 kcal`
   - 偏日式、滿足感高，也比較有「吃好料」的感覺

## 5. Success Criteria

### User Success

- 使用者能在 30 秒內選到想吃的組合
- 推薦結果看起來合理，不會太瞎
- 推薦內容有明顯差異，不是 3 組都長很像

### Demo Success

- 可以在影片中清楚展示「輸入熱量 -> 產生推薦」
- 推薦結果有畫面感，適合截圖與講解
- 足以展示資料、邏輯、前端介面與部署流程

## 6. Data Model

目前以 [foods.json](/Users/johnny/Desktop/claude%20code/foods.json) 作為第一版資料來源。

每筆資料欄位：

- `id`
- `name`
- `brand`
- `category`
- `cuisine`
- `meal_role`
- `calories`
- `protein_g`
- `price_twd`
- `tags`

### Current Food Data Strategy

- 先使用固定資料集，提升 demo 穩定度
- 熱量與價格以「可展示的估算值」為主
- 後續若要接 PostgreSQL，再把 `foods.json` 匯入資料表

## 7. Recommendation Logic

第一版不完全依賴 AI 生成，而是採用「資料 + 規則 + AI 包裝」：

### Step 1
依據使用者選擇的 `cuisine`、`tags`、限制條件，先過濾食物候選清單。

### Step 2
根據 `meal_role` 組合出合理的餐：

- 至少 1 個 `main`
- 可搭配 0 到 2 個 `side`
- 可搭配 0 到 1 個 `drink`
- 可搭配 0 到 1 個 `dessert`

### Step 3
計算總熱量，優先挑選接近目標熱量的組合。

建議容許範圍：

- 優先：距離目標 `+- 150 kcal`
- 可接受：距離目標 `+- 250 kcal`

### Step 4
避免結果重複：

- 不要 3 組都只差一杯飲料
- 優先選出不同品牌、不同風格的組合

### Step 5
用 AI 或模板文案補上：

- 組合名稱
- 簡短推薦理由
- 口語化描述

## 8. Tech Approach

### Phase 1: Local MVP

- 使用 `foods.json`
- 先做一個簡單推薦函式
- 回傳靜態 JSON 結果或簡單 API

### Phase 2: Product UI

- 做輸入表單
- 做結果卡片
- 加上重新推薦按鈕

### Phase 3: Zeabur Demo

- 部署前端
- 部署後端 API
- 可選擇接 PostgreSQL
- 可選擇接 AI Hub 生成更自然的推薦文案
- 可選擇接 Email 做每週 cheat meal 推薦

## 9. Zeabur Fit

這個題目可自然展示以下能力：

- 前端部署
- 後端部署
- 資料庫
- AI Hub
- 網域
- Email

### Suggested Skill Mapping

- 建專案：`zeabur-project-create`
- 部署服務：`zeabur-deploy`
- 管理環境變數：`zeabur-variables`
- 綁網址：`zeabur-domain-url`
- AI 文案：`zeabur-ai-hub`
- 每週推薦信：`zeabur-email`
- 除錯：`zeabur-deployment-logs`

## 10. Design Direction

### Overall Style

- 採用偏 Google 式的簡約設計風格
- 畫面乾淨、留白明確、資訊層級清楚
- 避免過度花俏、過度擬物或太重的健身 App 風格
- 整體要有現代感、易讀性與產品感

### Typography

- 全站主要字體使用黑體
- 優先採用現代、清楚、偏中性的人文黑體或無襯線黑體
- 標題字重明確，內文保持簡潔易讀
- 熱量、價格、推薦結果等數字資訊要特別清楚

### Visual Principles

- 介面應以卡片式區塊呈現推薦結果
- 表單操作簡單直接，不要有太多干擾元素
- 配色偏克制，重點資訊用少量強調色點出
- 讓使用者感覺像在使用一個成熟、可信、輕量的工具產品

### UI Tone

- 雖然主題是 cheat meal，但畫面不走油膩或過度罪惡感風格
- 以「理性整理資訊 + 輕鬆幫你做決定」為主
- 文案可以有一點幽默，但視覺仍保持簡潔

### Design Keywords

- clean
- minimal
- structured
- modern
- calm
- product-like

## 11. Milestones

### Milestone 1
完成 spec 與資料集。

Definition of done:

- `spec.md` 完成
- `foods.json` 有可用的初始資料

### Milestone 2
完成推薦邏輯 MVP。

Definition of done:

- 可輸入目標熱量
- 可回傳至少 3 組推薦
- 每組有熱量與品項資訊

### Milestone 3
完成可 demo 的前端介面。

Definition of done:

- 使用者能從畫面輸入條件
- 可以看到推薦卡片
- 可以重新產生推薦

### Milestone 4
完成 Zeabur 部署與比賽 demo。

Definition of done:

- 前後端可公開存取
- 有一個可分享網址
- 有清楚的 demo 流程

## 12. Open Questions

這些可以稍後再決定，不阻礙現在開發：

- 第一版要不要支援「避免食材」以外的更多飲食限制
- 第一版要不要顯示蛋白質或罪惡值
- 第一版要不要做收藏功能
- 第一版要不要加入價格上限

## 13. Immediate Next Steps

1. 寫第一版推薦函式，從 `foods.json` 產生 3 組結果
2. 定義輸入格式，例如 `targetCalories`, `cuisine`, `includeDrink`, `excludeTags`
3. 寫一個本機可測的 API 或 CLI
4. 再開始做前端畫面
