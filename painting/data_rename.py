
import os

import openpyxl

# 設定你的資料夾路徑（請改成你實際的路徑）
folder_path = "C:/Users/robotic/Desktop/Luke/油漆調色_原始資料/My Documents"

# 走訪資料夾中的所有檔案
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".xlsx"):
        file_path = os.path.join(folder_path, filename)
        try:
            # 讀取工作簿與 A2 內容
            wb = openpyxl.load_workbook(file_path, data_only=True)
            sheet = wb.active
            new_name = str(sheet["A2"].value).strip()

            if not new_name:
                print(f"⚠️ 檔案 {filename} 的 A2 是空的，跳過。")
                continue

            # 新的檔案名稱
            new_file_path = os.path.join(folder_path, new_name + ".xlsx")

            # 若新檔名已存在，加上編號避免覆蓋
            counter = 1
            while os.path.exists(new_file_path):
                new_file_path = os.path.join(
                    folder_path, f"{new_name}_{counter}.xlsx")
                counter += 1

            os.rename(file_path, new_file_path)
            print(f"✅ 已將 {filename} 重新命名為 {os.path.basename(new_file_path)}")

        except Exception as e:
            print(f"❌ 無法處理 {filename}：{e}")
