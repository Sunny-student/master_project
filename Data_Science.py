import pydicom, glob, os
from pydicom.errors import InvalidDicomError
from collections import defaultdict

dicom_dir = "C:/Users/robotic/Downloads/TPMIC01065/T1"

# 搜索 .dcm / .IMA（大小寫都抓），以及保底的 "全部檔案"
patterns = ["**/*.dcm", "**/*.DCM", "**/*.IMA", "**/*.ima", "**/*"]
files = []
seen = set()
for pat in patterns:
    for fp in glob.glob(os.path.join(dicom_dir, pat), recursive=True):
        if os.path.isfile(fp) and fp not in seen:
            files.append(fp)
            seen.add(fp)

def safe_get(ds, tag):
    e = ds.get(tag, None)
    return None if e is None else e.value

candidates = []
for fp in files:
    try:
        ds = pydicom.dcmread(fp, stop_before_pixels=True, force=True)
    except InvalidDicomError:
        continue
    except Exception:
        continue

    # 先抓幾個描述欄位，方便辨識系列
    sd = str(safe_get(ds, (0x0008,0x103E)) or "").lower()   # SeriesDescription
    pn = str(safe_get(ds, (0x0018,0x1030)) or "").lower()   # ProtocolName
    sn = str(safe_get(ds, (0x0018,0x0024)) or "").lower()   # SequenceName
    text = " ".join([sd, pn, sn])

    # 關鍵字（你可依實際字串微調，如 "t1", "mpr", "mprage", "sag"）
    if ("mprage" in text or "mpr" in text) and ("sag" in text or "sagittal" in text):
        rows = safe_get(ds, (0x0028,0x0010))
        cols = safe_get(ds, (0x0028,0x0011))
        candidates.append((fp, rows, cols, sd or pn or sn))

# 若一個都沒抓到，印幾個檔案的描述讓你調整關鍵字
if not candidates:
    print("尚未匹配到含 mprage + sag 的檔案，以下列出前 8 個可讀檔的描述，請依實際字串調整關鍵字：\n")
    shown = 0
    for fp in files:
        if shown >= 8: break
        try:
            ds = pydicom.dcmread(fp, stop_before_pixels=True, force=True)
        except Exception:
            continue
        sd = safe_get(ds, (0x0008,0x103E))
        pn = safe_get(ds, (0x0018,0x1030))
        sn = safe_get(ds, (0x0018,0x0024))
        print(f"- {fp}\n  SeriesDescription: {sd}\n  ProtocolName     : {pn}\n  SequenceName     : {sn}\n")
        shown += 1
else:
    # 彙總該系列的 Rows x Columns
    size_count = defaultdict(int)
    for _, r, c, _ in candidates:
        size_count[(r, c)] += 1

    print("偵測到疑似 T1 3D_mprage_SAG 系列的切片矩陣大小（Rows x Columns）：")
    for (r, c), n in sorted(size_count.items()):
        print(f"- {r} x {c}  （出現 {n} 張）")

    # 顯示一個代表檔案的細節
    fp, r, c, desc = candidates[0]
    print("\n範例檔案：", fp)
    print("描述字串 ：", desc)
    print("Rows (0028,0010)：", r)
    print("Cols (0028,0011)：", c)
