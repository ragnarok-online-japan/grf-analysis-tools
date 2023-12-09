#!/usr/bin/env python3

import argparse
import io
import os
import re
import subprocess

from dotenv import load_dotenv
from PIL import Image
from PIL.PngImagePlugin import PngInfo

load_dotenv()

parser = argparse.ArgumentParser(description="")

parser.add_argument("--grffile",
                    action="store",
                    nargs=1,
                    default="data.grf",
                    type=str,
                    help="data.grf path")

parser.add_argument("--import-path",
                    action="store",
                    default="./export_grf",
                    type=str,
                    help="import path")

parser.add_argument("--export-path-imgdir",
                    action="store",
                    default="./export_img",
                    type=str,
                    help="export path")

parser.add_argument("--overwrite",
                    action="store_true",
                    default=False,
                    help="Over write")

args = parser.parse_args()

grffile = os.path.abspath(args.grffile)

def main(args:dict):
    if os.path.isdir(args.export_path_imgdir) == False:
        os.mkdir(args.export_path_imgdir)

    items = {}

    filename = "idnum2itemdisplaynametable.txt"
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
                    "resname"    : None
                }

    filename = "idnum2itemresnametable.txt"
    with open("{:}/{:}".format(args.import_path, filename), "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip()
            if re.match(r"^//.*", line):
                continue
            if re.match(r"^#.*", line):
                item_id = None
                continue

            matches = re.match(r"^(\d+)#([^#]+)#$", line)
            if matches and int(matches[1]) in items:
                item_id = int(matches[1])

                items[item_id]["resname"] = matches[2]

    filename = "num2cardillustnametable.txt"
    with open("{:}/{:}".format(args.import_path, filename), "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip()
            if re.match(r"^//.*", line):
                continue
            if re.match(r"^#.*", line):
                item_id = None
                continue

            matches = re.match(r"^(\d+)#([^#]+)#$", line)
            if matches and int(matches[1]) in items:
                item_id = int(matches[1])

                items[item_id]["cardillustname"] = matches[2]

    for item_id in items:
        resname: str = items[item_id]["resname"]
        if resname is None:
            continue
        resname = resname.lower()
        path: str = f"data\\texture\\유저인터페이스\\collection\\{resname:s}.bmp"
        export_filename = os.path.abspath(args.export_path_imgdir + f"/{item_id:d}.png")

        if os.path.isfile(export_filename) == False or args.overwrite == True:
            export_image(grffile, path, export_filename)

        if "cardillustname" in items[item_id]:
            cardillustname: str = items[item_id]["cardillustname"]
            if cardillustname is None:
                continue
            cardillustname = cardillustname.lower()
            path: str = f"data\\texture\\유저인터페이스\\cardbmp\\{cardillustname:s}.bmp"
            export_filename = os.path.abspath(args.export_path_imgdir + f"/{item_id:d}_cardillust.png")
            if os.path.isfile(export_filename) == False or args.overwrite == True:
                export_image(grffile, path, export_filename)

def export_image(grffile: str, path: str, export_filename):
    grftool: list[str] = [os.getenv("GRFTOOL"), grffile, path.encode("euc-kr", errors="ignore")]
    subp = subprocess.run(grftool, capture_output=True)
    image_bytes: bytes = subp.stdout

    if len(image_bytes) == 0:
        print("[WARNING]", "Length 0:", path)
        return

    image = Image.open(io.BytesIO(image_bytes))

    copyright: str = "(C) Gravity Co., Ltd. & LeeMyoungJin(studio DTDS) All rights reserved.\n(C) GungHo Online Entertainment, Inc. All Rights Reserved."
    metadata = PngInfo()
    metadata.add_text("Copyright", copyright)
    metadata.add_text("Exporter", "https://rodb.aws.0nyx.net/")

    image.save(export_filename, format="PNG", pnginfo=metadata)

if __name__ == "__main__":
    main(args)
