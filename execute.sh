#!/bin/bash
cd /opt/grf-analysis-tools

./export_grf2text.py --grf-path ../grf-files/data.grf

./itemdata2text.py
cp -p items.json /var/www/html/ROOD/

./itemdata2gas.py

./jobname.sh

./skills.sh

./export_grf2itemimg.py --grf-path ../grf-files/data.grf --export-path-imgdir /var/www/html/ROOD/items/
