#!/usr/bin/env python3

import argparse
import os
import subprocess

from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser(description="")

parser.add_argument("--grftool",
                    action="store",
                    nargs=1,
                    default="/usr/local/bin/grftool",
                    type=str,
                    help="grftool path")

parser.add_argument("--iconv",
                    action="store",
                    nargs=1,
                    default="/usr/bin/iconv",
                    type=str,
                    help="iconv path")

parser.add_argument("--grffile",
                    action="store",
                    nargs=1,
                    default="data.grf",
                    type=str,
                    help="data.grf path")

parser.add_argument("--export-path",
                    action="store",
                    nargs=1,
                    default="./export_grf",
                    type=str,
                    help="export path")

args = parser.parse_args()

def main(args:dict):
    export_datas = {
        "carditemnametable.txt"         : {
            "path":"data\\carditemnametable.txt"
        },
        "cardpostfixnametable.txt"      : {
            "path":"data\\cardpostfixnametable.txt"
        },
        "cardprefixnametable.txt"       : {
            "path":"data\\cardprefixnametable.txt"
        },
        "idnum2itemdesctable.txt"       : {
            "path":"data\\idnum2itemdesctable.txt"
        },
        "idnum2itemdisplaynametable.txt": {
            "path":"data\\idnum2itemdisplaynametable.txt"
        },
        "idnum2itemresnametable.txt"    : {
            "path":"data\\idnum2itemresnametable.txt",
            "iconv_param" : ["-c", "-f", "EUC-KR", "-t", "UTF-8"]
        },
        "num2itemresnametable.txt"    : {
            "path":"data\\num2itemresnametable.txt",
            "iconv_param" : ["-c", "-f", "EUC-KR", "-t", "UTF-8"]
        },
        "itemparamtable.txt"            : {
            "path":"data\\itemparamtable.txt"
        },
        "itemslotcounttable.txt"        : {
            "path":"data\\itemslotcounttable.txt"
        },
        "itemslottable.txt"             : {
            "path":"data\\itemslottable.txt"
        },
        "num2cardillustnametable.txt"   : {
            "path":"data\\num2cardillustnametable.txt",
            "iconv_param" : ["-c", "-f", "EUC-KR", "-t", "UTF-8"]
        }
    }

    if os.path.isdir(args.export_path) == False:
        os.mkdir(args.export_path)

    for filename in export_datas.keys():
        print("export", filename)
        path = export_datas[filename]["path"]
        binary: bool = False
        if "binary" in export_datas[filename]:
            binary = True

        grftool: list[str] = [os.getenv("GRFTOOL"), os.path.abspath(args.grffile), path]

        mode = "w"
        if binary == False:
            # ascii
            iconv: list[str] = [os.getenv("ICONV")]
            iconv_param: list[str] = ["-c", "-f", "CP932", "-t", "UTF-8"]
            if "iconv_param" in export_datas[filename]:
                iconv_param = export_datas[filename]["iconv_param"]
            iconv.extend(iconv_param)

            tr: list[str] = [os.getenv("TR")]
            tr.extend(["-d", "\\r"])

            subp1 = subprocess.run(grftool, capture_output=True)
            subp2 = subprocess.run(iconv, capture_output=True, input=subp1.stdout)
            subp3 = subprocess.run(tr, capture_output=True, input=subp2.stdout)

            data = subp3.stdout.decode("utf-8")
            mode = "w"
        else:
            # binary
            subp1 = subprocess.run(grftool, capture_output=True)
            data = subp1.stdout
            mode = "wb"

        with open("{:}/{:}".format(args.export_path, filename), mode) as fp:
            fp.write(data)

if __name__ == "__main__":
    main(args)
