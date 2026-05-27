import os
import json

F_NAME = "books.json"

class Book:
    """書籍資料模型，負責封裝書籍屬性與格式轉換"""
    def __init__(self, title: str, isbn: str, status: str):
        self.t = title   # 內部沿用代號以保持 cmd show 輸出簡潔
        self.i = isbn
        self.s = status

    def to_dict(self) -> dict:
        """轉換為標準 JSON 所需的字典格式"""
        return {
            "title": self.t,
            "isbn": self.i,
            "status": self.s
        }


class LibraryManager:
    """圖書管理核心系統，消除全域變數，強化錯誤處理與效能"""
    def __init__(self):
        self.d2 = []  # 物件獨立屬性，拒絕全域污染
        self.load_proc()

    def load_proc(self):
        """讀取標準 JSON 格式檔案（含防損毀例外處理）"""
        if os.path.exists(F_NAME):
            try:
                with open(F_NAME, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        # 確保即便是髒資料也不會導致整台系統壞掉
                        if "title" in item and "isbn" in item and "status" in item:
                            self.d2.append(Book(item["title"], item["isbn"], item["status"]))
            except (IOError, json.JSONDecodeError):
                # 檔案損毀或編碼錯誤時，優雅跳過，防止崩潰
                pass

    def c_res(self, v: str) -> bool:
        """檢查 ISBN 是否重複"""
        for b in self.d2:
            if b.i == v:
                return True
        return False

    def save_and_exit(self):
        """【效能優化】直到 exit 時才一次性寫入磁碟，大幅降低記憶體與硬碟 I/O 負擔"""
        try:
            with open(F_NAME, "w", encoding="utf-8") as f:
                json_data = [b.to_dict() for b in self.d2]
                json.dump(json_data, f, ensure_ascii=False, indent=2)
        except IOError:
            pass
        print("系統關閉")

    def add_book(self, cmd_args: str):
        """安全解析使用者輸入並加入記憶體"""
        raw = cmd_args.split("/")
        if len(raw) == 3:
            title, isbn, status = raw[0].strip(), raw[1].strip(), raw[2].strip()
            if not self.c_res(isbn):
                self.d2.append(Book(title, isbn, status)) # 僅更新記憶體
                print("Success")
            else:
                print("ISBN Exist")
        else:
            print("Format Error")

    def show_books(self):
        """保持與 v0.1 完全一致的 CMD 輸出風格"""
        for b in self.d2:
            print(f"書名: {b.t}, ISBN: {b.i}, 狀態: {b.s}")

    def borrow_book(self, target_isbn: str):
        """借閱邏輯更新"""
        target_isbn = target_isbn.strip()
        for b in self.d2:
            if b.i == target_isbn:
                b.s = "borrowed"
                print("Updated")


def main():
    manager = LibraryManager()
    print("=== 圖書管理系統 v0.1 (Legacy) ===")
    
    while True:
        try:
            op = input("> ").strip()
            if not op:
                continue
            
            if op == "exit":
                manager.save_and_exit()
                break
                
            elif op.startswith("add "):
                manager.add_book(op[4:])
                
            elif op == "show":
                manager.show_books()
                
            elif op.startswith("borrow "):
                manager.borrow_book(op[7:])
                
            else:
                print("Unknown Command")
                
        except Exception:
            # 萬用頂層保護，確保 cmd 視窗在任何極端狀況下都不會閃退
            print("Unknown Command")


if __name__ == "__main__":
    main()