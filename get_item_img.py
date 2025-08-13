#!/usr/bin/env python3

# pip3 install pyquery aiohttp Pillow

import argparse
import io
import os
import traceback

import yaml
import requests
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser(description='')

parser.add_argument('--import-item',
                    action='store',
                    nargs='?',
                    default='./item.yaml',
                    type=str,
                    help='import item.yaml')

parser.add_argument('--export-path-org',
                    action='store',
                    nargs='?',
                    default='./images_org',
                    type=str,
                    help='export path')

parser.add_argument('--export-path',
                    action='store',
                    nargs='?',
                    default='./images',
                    type=str,
                    help='export path')

parser.add_argument('--icon-url',
                    action='store',
                    nargs='?',
                    default='https://rotool.gungho.jp/icon/',
                    type=str,
                    help='icon url')

parser.add_argument('--font',
                    action='store',
                    nargs='?',
                    default='./SourceCodePro-Light.ttf',
                    type=str,
                    help='Font(TTF) file path')

args = parser.parse_args()

def download(args: dict, key: int, font: ImageFont):
    org_image_filepath = "{:s}/{:d}.png".format(args.export_path_org, key)
    image_filepath = "{:s}/{:d}.png".format(args.export_path, key)
    download_flag: bool = False

    try:
        if os.path.isfile(org_image_filepath) == False:
            download_flag = True
        else:
            response = requests.head("{:s}/{:d}.png".format(args.icon_url, key), allow_redirects=False)
            file_size: int = -1
            if (response.status_code == 200):
                file_size = response.headers.get("content-length", -1)

            if file_size != os.path.getsize(org_image_filepath):
                print("[INFO]", "item_id:", key, "exists")
                return
            else:
                download_flag = True

        if download_flag == True:
            response = requests.get("{:s}/{:d}.png".format(args.icon_url, key), allow_redirects=False)
            if response.status_code != 200:
                ex = Exception("HTTP status: ", response.status_code, key)
                raise ex

            content_type = response.headers["content-type"]
            if "image" not in content_type:
                ex = Exception("Content-Type: ", content_type, key)
                raise ex

            with open(org_image_filepath, "wb") as fp:
                fp.write(response.content)

            # Pillowのイメージ化
            image = Image.open(org_image_filepath)
            # 横幅、高さ
            _, height = image.size
            draw = ImageDraw.Draw(image)
            draw.text((4,height-36), "(c)Gravity Co., Ltd. & LeeMyoungJin(studio DTDS) All rights reserved.\n(c)GungHo Online Entertainment, Inc. All Rights Reserved.", font=font)
            # 保存
            image.save(image_filepath, format="PNG", quality=100, optimize=True)
            print("[INFO]", "item_id:", key, "download success")
    except Exception as ex:
        print("[ERROR]", "item_id:", key, ex)
        #print(traceback.format_exc())

def main(args: dict):
    items = {}
    with open(args.import_item, "r", encoding="utf-8") as fp:
        items = yaml.safe_load(fp)

    if os.path.isdir(args.export_path_org) == False:
        os.mkdir(args.export_path_org)

    if os.path.isdir(args.export_path) == False:
        os.mkdir(args.export_path)

    font = ImageFont.truetype(args.font, size=10)
    for key in items:
        download(args, int(key), font)

if __name__ == '__main__':
    main(args)
