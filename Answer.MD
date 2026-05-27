# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B1109047
**系級：** 資管系大四 
**姓名：** 潘宇航

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| Q1 l1 (in load_proc) |從檔案讀取出來的原始文字行資料列表（Lines） |file_lines |
| Q2 d2 (in main) | 系統核心：儲存所有書籍資料的清單/資料庫（Database）| book_list|
| Q3 c_res (in check) | 檢查 ISBN 是否已經存在 的邏輯判斷（Check Response）|is_isbn_exists |

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

Q1：缺乏例外處理機制（Exception Handling）

為什麼不好： 在 load_proc 和 exit 進行檔案讀寫，以及 add 拆解字串時，完全沒有使用 try...except。如果 lib_data.txt 檔案被權限鎖定、損毀，或是使用者輸入 add a/b（格式不符）導致 raw[2] 索引溢位，程式會直接崩潰（Crash）斷線。

Q2：濫用全域變數（Global Variable）與緊密耦合

為什麼不好： 核心資料 d2 被宣告為全域變數，且被多個函式（load_proc, c_res, main）直接存取與修改。這破壞了函式的封裝性，當專案變大時，你很難追蹤是誰偷偷改了資料，也非常不利於進行單元測試（Unit Test）。

Q3：資源未妥善釋放（Resource Leak）

為什麼不好： 程式在 load_proc 和 exit 中使用傳統的 f = open(...) 搭配 f.close()。如果在 open 之後、close 之前程式發生錯誤中途跳出，檔案控制代碼（File Handle）就不會被釋放，可能導致檔案遭到鎖定。

Q4：神祕的硬編碼分隔符（Magic Strings / Hardcoded Delimiters）

為什麼不好： 程式碼中到處充斥著 "@@"、"##"、"borrowed"、"/" 等魔術字串，甚至連鍵值（Key）都用 b['t']、b['i']、b['s'] 這種極短的縮寫。如果未來想將分隔符改成 CSV 的 ,，或是修改欄位名稱，就必須改動全程式多處地方，極易漏掉。

Q5：缺乏資料封裝與魔術索引（Magic Indexes）

為什麼不好： 書籍資料直接用字典（Dictionary）搭配硬編碼的索引（如 p2[0]、raw[1]）來處理。這導致商業邏輯（例如「什麼是書籍？」、「如何驗證 ISBN 格式？」）散落在各個角落。正確的做法應該是定義一個 Book 類別（Class），將屬性與行為封裝起來。

---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A： 原本代碼未標示清楚的變數建議修正名稱和代表意義，並請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

Prompt B： 請根據以下需求撰寫程式碼

      模組化： 將功能拆解為類別 (Class) 或多個函式 (Function)。
    - 格式升級： 捨棄原本的 `txt` 混亂分割格式，改用標準 `json` 格式儲存。
    - 強健性： 增加對使用者輸入與檔案讀取的錯誤處理 (Try-Except)。
    - 優化： 修正原程式每次新增資料都要開啟磁碟寫入的低效率行為。

Prompt C：根據上述分析重構程式
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？（例如：漏寫了某個功能、語法錯誤）你是如何發現並請它修正的？在cmd print出來的內容跟原本的程式碼輸出的不太一樣，我跟他說我在cmd看到的格式要與原本的代碼一模一樣，他就又給我修正好的代碼，測試一切順利

2. 發現的問題： 輸出格式與原來不太一樣

3. 修正的對話： 我在cmd看到的格式要與原本的代碼一模一樣
---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
=== 圖書管理系統 v0.1 (Legacy) ===
> add 深入淺出Python/978001/available
Success
> add 資料結構理論/978002/available
Success
> add 演算法實作/978003/available
Success
> add 重複測試書/978001/available
ISBN Exist
> borrow 978002
Updated
> show
書名: 深入淺出Python, ISBN: 978001, 狀態: available
書名: 資料結構理論, ISBN: 978002, 狀態: borrowed
書名: 演算法實作, ISBN: 978003, 狀態: available
> exit
系統關閉
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
  {
    "title": "深入淺出Python",
    "isbn": "978001",
    "status": "available"
  },
  {
    "title": "資料結構理論",
    "isbn": "978002",
    "status": "borrowed"
  },
  {
    "title": "演算法實作",
    "isbn": "978003",
    "status": "available"
  }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)


```log
# 請在此處貼上 git log 內容
2a2fda8 (HEAD -> main, origin/main) second commit
14f8ba0 first commit
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
https://github.com/yhpan-b11009047/B11009047-0527-Final.git
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
