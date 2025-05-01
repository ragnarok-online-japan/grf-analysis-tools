#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser(description="")

parser.add_argument("--grftool",
                    action="store",
                    nargs=1,
                    default="./pygrf/grftool.py",
                    type=str,
                    help="grftool.py path")

parser.add_argument("--grf-path",
                    action="store",
                    default="./data.grf",
                    type=str,
                    help="data.grf path")

parser.add_argument("--export-path",
                    action="store",
                    default="./export_grf",
                    type=str,
                    help="export path")

args = parser.parse_args()

def main(args:dict):
    export_datas = {
        "carditemnametable.txt": {
            "path":"data/carditemnametable.txt",
            "decoding":"cp932"
        },
        "cardpostfixnametable.txt": {
            "path":"data/cardpostfixnametable.txt",
            "decoding":"cp932"
        },
        "cardprefixnametable.txt": {
            "path":"data/cardprefixnametable.txt",
            "decoding":"cp932"
        },
        "idnum2itemdesctable.txt": {
            "path":"data/idnum2itemdesctable.txt",
            "decoding":"cp932"
        },
        "idnum2itemdisplaynametable.txt": {
            "path":"data/idnum2itemdisplaynametable.txt",
            "decoding":"cp932"
        },
        "idnum2itemresnametable.txt": {
            "path":"data/idnum2itemresnametable.txt",
            "decoding":"euc-kr"
        },
        "num2itemresnametable.txt": {
            "path":"data/num2itemresnametable.txt",
            "decoding":"euc-kr"
        },
        "num2cardillustnametable.txt": {
            "path":"data/num2cardillustnametable.txt",
            "decoding":"euc-kr"
        },
        "itemparamtable.txt": {
            "path":"data/itemparamtable.txt",
            "decoding":"cp932"
        },
        "itemslotcounttable.txt": {
            "path":"data/itemslotcounttable.txt",
            "decoding":"cp932"
        },
        "itemslottable.txt": {
            "path":"data/itemslottable.txt",
            "decoding":"cp932"
        }
    }

    if os.path.isdir(args.export_path) == False:
        os.mkdir(args.export_path)

    for file in export_datas.keys():
        print("[INFO]", "export:", file)
        filename = export_datas[file]["path"]
        binary: bool = False
        if "binary" in export_datas[file]:
            binary = True

        cmd: list[str] = [
            args.grftool,
            os.path.abspath(args.grf_path),
            filename
        ]

        mode = "w"
        if binary == False:
            subp1 = subprocess.run(cmd, capture_output=True)
            data = subp1.stdout.decode(export_datas[file]['decoding'], errors="replace")
            stdrr = subp1.stderr.decode()
            if stdrr != "":
                print(stdrr, file=sys.stderr)
                continue

            mode = "w"
        else:
            # binary
            subp1 = subprocess.run(cmd, capture_output=True)
            data = subp1.stdout
            mode = "wb"

        with open("{:}/{:}".format(args.export_path, file), mode) as fp:
            fp.write(data)

if __name__ == "__main__":
    main(args)
