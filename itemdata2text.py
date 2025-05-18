#!/usr/bin/env python3.13

import argparse
import json
import os
import re

import yaml
import polars as pl

parser = argparse.ArgumentParser(description="")

parser.add_argument("--import-path",
                    action="store",
                    nargs=1,
                    default="./export_grf",
                    type=str,
                    help="import path")

args = parser.parse_args()

def main(args:dict):
    if os.path.isdir(args.import_path) == False:
        raise ValueError("Illigal import path")

    items = {}

    filename = "idnum2itemdisplaynametable.txt"
    print("[INFO]", "import:", filename)
    with open("{:}/{:}".format(args.import_path, filename), "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip()
            if re.match(r"^//.*", line):
                continue

            matches = re.match(r"^([0-9]+)#(.+)#$", line)
            if matches:
                item_id = int(matches[1])
                items[item_id] = {
                    "id"         : item_id,
                    "displayname": matches[2],
                    "description": "",
                    "type"       : None,
                    "is_card"    : False,
                    "is_enchant" : False,
                    "resname"    : None
                }

    filename = "idnum2itemdesctable.txt"
    print("[INFO]", "import:", filename)
    item_id = None
    with open("{:}/{:}".format(args.import_path, filename), "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip()
            if re.match(r"^//.*", line):
                continue
            if re.match(r"^#.*", line):
                item_id = None
                continue

            matches = re.match(r"^([0-9]+)#$", line)
            if matches and int(matches[1]) in items:
                item_id = int(matches[1])
                continue

            if item_id is not None:
                line = re.sub(r"\^000000", "</span>", line)
                line = re.sub(r"\^([0-9a-fA-F]{6})", r'<span style="color:#\1">', line)
                items[item_id]["description"] = items[item_id]["description"] + f"{line}\n"

    filename = "idnum2itemresnametable.txt"
    print("[INFO]", "import:", filename)
    with open("{:}/{:}".format(args.import_path, filename), "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip()
            if re.match(r"^//.*", line):
                continue
            if re.match(r"^#.*", line):
                item_id = None
                continue

            matches = re.match(r"^([0-9]+)#([^#]+)#$", line)
            if matches and int(matches[1]) in items:
                item_id = int(matches[1])

                items[item_id]["resname"] = matches[2]

    filename = "num2cardillustnametable.txt"
    print("[INFO]", "import:", filename)
    with open("{:}/{:}".format(args.import_path, filename), "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip()
            if re.match(r"^//.*", line):
                continue
            if re.match(r"^#.*", line):
                item_id = None
                continue

            matches = re.match(r"^([0-9]+)#([^#]+)#$", line)
            if matches and int(matches[1]) in items:
                item_id = int(matches[1])

                items[item_id]["cardillustname"] = matches[2]

    filename = "cardprefixnametable.txt"
    print("[INFO]", "import:", filename)
    with open("{:}/{:}".format(args.import_path, filename), "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip()
            if re.match(r"^//.*", line):
                continue

            matches = re.match(r"^([0-9]+)#(.+)#$", line)
            if matches and int(matches[1]) in items:
                item_id = int(matches[1])

                # 末尾がカードじゃないとカード判定しない
                # -> エンチャントも何故かこのファイルに含まれる...
                if re.match("^.+カード$", items[item_id]["displayname"]):
                    items[item_id]["is_card"] = True
                else:
                    items[item_id]["is_enchant"] = True

                items[item_id]["injection_detail"] = {
                    "name": matches[2],
                    "prefix": True
                }

    filename = "cardpostfixnametable.txt"
    print("[INFO]", "import:", filename)
    with open("{:}/{:}".format(args.import_path, filename), "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip()
            if re.match(r"^//.*", line):
                continue

            matches = re.match(r"^([0-9]+)#", line)
            if matches and int(matches[1]) in items:
                item_id = int(matches[1])

                items[item_id]["injection_detail"]["prefix"] = False

    # item判定
    pattern_type      = re.compile(r"系列\s*:\s*<.+?>(.+?)</")
    pattern_equipment = re.compile(r"装備\s*:\s*<.+?>(.+?)</")
    pattern_position  = re.compile(r"位置\s*:\s*<.+?>(.+?)</")
    pattern_slot      = re.compile(r"スロット\s*:\s*<.+?>([0-9]+)</")
    for item in items.values():
        item["description"] = item["description"].rstrip()

        match = pattern_type.search(item["description"])
        if match:
            item["type"] = match.group(1)

        match = pattern_equipment.search(item["description"])
        if match:
            if item["type"] == "カード":
                item["card_postion"] = match.group(1)
                if item["is_card"] == False:
                    item["is_card"] = True
            else:
                jobs: list = match.group(1).split(" ")
                item["jobs"] = jobs

        match = pattern_position.search(item["description"])
        if match and match.group(1) != "-":
            item["position"] = match.group(1)

        match = pattern_slot.search(item["description"])
        if match:
            item["slot"] = int(match.group(1))

    #/////////////////////////////////////////////////////////////////////////

    #filename = "items.json"
    #print("export :", filename)
    #with open(os.path.abspath(filename), "w", encoding="utf-8") as fp:
    #    json.dump(items, fp, sort_keys=True, ensure_ascii=False, indent=4)

    filename = "items.jsonl"
    print("export :", filename)
    records = []
    for key, value in items.items():
        value = value.copy()
        value["id"] = int(key)
        records.append(value)
    schema: dict = {
        "id": pl.Int32,
        "displayname": pl.Utf8,
        "description": pl.Utf8,
        "is_card": pl.Boolean,
        "is_enchant": pl.Boolean,
        "resname": pl.Utf8,
        "type": pl.Utf8,  # None or str
    }
    df = pl.from_dicts(records, schema=schema).sort("id")
    df.write_ndjson(filename)

    #filename = "items.yaml"
    #print("export :", filename)
    #with open(os.path.abspath(filename), "w", encoding="utf-8") as fp:
    #    yaml.dump(items, fp, sort_keys=True, allow_unicode=True, indent=4)

if __name__ == "__main__":
    main(args)
