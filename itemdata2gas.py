#!/usr/bin/env python3

import argparse
import os
import re

from google.oauth2.service_account import Credentials
import gspread

parser = argparse.ArgumentParser(description="")

# https://drive.google.com/drive/folders/1QPCxW-dJ1OJ4nCpfE4AZ1m_kMc9P-wRC

parser.add_argument("--import-path",
                    action="store",
                    default="./export_grf",
                    type=str,
                    help="import path")

parser.add_argument("--drive_folder_id",
                    action="store",
                    default="1QPCxW-dJ1OJ4nCpfE4AZ1m_kMc9P-wRC",
                    type=str,
                    help="google driver folder id")

args = parser.parse_args()

def main(args:dict):
    if os.path.isdir(args.import_path) == False:
        raise ValueError("Illigal import path")

    items = {}

    filename = "idnum2itemdisplaynametable.txt"
    print("import", filename)
    with open("{:}/{:}".format(args.import_path, filename), "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip()
            if re.match(r"^//.*", line):
                continue

            matches = re.match(r"^(\d+)#(.+)#$", line)
            if matches:
                item_id = int(matches[1])
                items[item_id] = {
                    "id"         : item_id,
                    "displayname": matches[2],
                    "description": "",
                    "type"       : None,
                    "slot"       : None,
                }

    filename = "idnum2itemdesctable.txt"
    print("import", filename)
    item_id = None
    with open("{:}/{:}".format(args.import_path, filename), "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip()
            if re.match(r"^//.*", line):
                continue
            if re.match(r"^#.*", line):
                item_id = None
                continue

            matches = re.match("^(\d+)#$", line)
            if matches and int(matches[1]) in items:
                item_id = int(matches[1])
                continue

            if item_id is not None:
                line = re.sub(r"\^000000", "", line)
                line = re.sub(r"\^([0-9a-fA-F]{6})", "", line)
                items[item_id]["description"] = items[item_id]["description"] + line + "\n"

    # item判定
    pattern_type      = re.compile(r"系列\s*:\s*([^\s]+)")
    pattern_slot      = re.compile(r"スロット\s*:\s*([0-9]+?)\s*")
    for item in items.values():
        matches = pattern_type.search(item["description"])
        if matches:
            item["type"] = matches.group(1).strip()

        matches = pattern_slot.search(item["description"])
        if matches:
            item["slot"] = int(matches.group(1))

    #/////////////////////////////////////////////////////////////////////////

    if len(items) > 0:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials = Credentials.from_service_account_file(
            filename="service_account.json",
            scopes=scopes
        )

        gc = gspread.authorize(credentials)

        files = gc.list_spreadsheet_files(folder_id=args.drive_folder_id)
        wb_name: str = "ragnarok_online_items"
        ws_name: str = "items"

        wb: gspread.Spreadsheet = None
        ws: gspread.Worksheet = None

        existing_spreadsheet = [file["name"] for file in files]
        if wb_name in existing_spreadsheet:
            print("[INFO]", f"Open workbook {wb_name}...")
            wb = gc.open(wb_name)
        else:
            print("[INFO]", f"Create sheet {wb_name}...")
            wb = gc.create(wb_name, folder_id=args.drive_folder_id)

        existing_spreadsheet = [sheet.title for sheet in wb.worksheets()]
        if f"{ws_name}.new" in existing_spreadsheet:
            # .new があれば削除
            wb.del_worksheet(wb.worksheet(f"{ws_name}.new"))

        rows: list = list(items.values())
        keys: list = list(rows[0].keys())
        rows = list([list(row.values()) for row in rows])

        count_row: int = len(rows) + 1 #+1=header
        count_col: int = len(keys)

        # 毎回.newを作る
        print("[INFO]", f"Create sheet {ws_name}.new ...")
        ws = wb.add_worksheet(title=f"{ws_name}.new", rows=count_row, cols=count_col)

        ws.append_row(keys)
        ws.append_rows(rows)

        if "Sheet1" in existing_spreadsheet:
            # Sheet1 があれば削除
            wb.del_worksheet(wb.worksheet("Sheet1"))

        try:
            # 過去分を削除
            wb.del_worksheet(wb.worksheet(f"{ws_name}"))
        except gspread.exceptions.WorksheetNotFound:
            # ignore
            pass

        try:
            # .newをrename
            wb.worksheet(f"{ws_name}.new").update_title(ws_name)
        except gspread.exceptions.WorksheetNotFound:
            # ignore
            pass

if __name__ == "__main__":
    main(args)
