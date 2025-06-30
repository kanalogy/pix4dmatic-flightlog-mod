#!/usr/bin/env python3
"""
Re-format flightlog.txt:

  1. Swap Longitude / Latitude.
  2. Re-order columns & rename LongitudeAccuracy → Horizontal accuracy.
  3. Drop LatitudeAccuracy.
  4. Replace each Pitch value x with (90 − x).

Result is saved as flightlog_reformatted.txt.
"""

import csv
from pathlib import Path

INFILE  = Path("flightlog.txt")
OUTFILE = Path("flightlog_reformatted.txt")

with INFILE.open(newline="", encoding="utf-8") as fin, \
     OUTFILE.open("w", newline="", encoding="utf-8") as fout:

    reader = csv.reader(fin)
    writer = csv.writer(fout)

    # ---- 1. ヘッダを解析 -------------------------------------------------
    header_raw = next(reader)
    if not header_raw or not header_raw[0].lstrip().startswith("#"):
        raise RuntimeError("First line must be a header beginning with '#'.")
    header = [h.lstrip("# ").strip() for h in header_raw]

    # 列インデックスを取得
    idx = {name: header.index(name) for name in (
        "Name", "Longitude", "Latitude", "Altitude",
        "LongitudeAccuracy", "LatitudeAccuracy", "AltitudeAccuracy",
        "Yaw", "Pitch", "Roll"
    )}

    # ---- 2. 目的のヘッダ順を定義 ----------------------------------------
    new_header = [
        "# Name",              # 先頭だけ "# " を再付与
        "Latitude",
        "Longitude",
        "Altitude",
        "Yaw",
        "Pitch",
        "Roll",
        "Horizontal accuracy",  # 改名
        "AltitudeAccuracy"
    ]
    writer.writerow(new_header)

    # ---- 3. 各行を変換して書き出す --------------------------------------
    for row in reader:
        if not row:            # 空行はスキップ
            continue

        # Pitch の数値変換と置き換え -------------------------------------
        try:
            pitch_val  = float(row[idx["Pitch"]])
            new_pitch  = 90.0 - pitch_val
            row[idx["Pitch"]] = f"{new_pitch:g}"   # 余分な 0 を付けない書式
        except ValueError:
            # 数値でなければ（例：空文字やヘッダ行など）そのまま出力
            pass

        new_row = [
            row[idx["Name"]],
            row[idx["Latitude"]],        # Longitude / Latitude を実質的に入れ替え
            row[idx["Longitude"]],
            row[idx["Altitude"]],
            row[idx["Yaw"]],
            row[idx["Pitch"]],           # 変換済み
            row[idx["Roll"]],
            row[idx["LongitudeAccuracy"]],  # Horizontal accuracy
            row[idx["AltitudeAccuracy"]]
        ]
        writer.writerow(new_row)

print(f"Done! Output written to: {OUTFILE.resolve()}")
