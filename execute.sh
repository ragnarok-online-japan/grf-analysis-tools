#!/bin/bash
cd /opt/grf-analysis-tools

cp items.json items.bak.json
cp skill_data.json skill_data.bak.json

./export_grf.py
./export_grf2itemimg.py --export-path-imgdir /var/www/html_rodb/ROOD/items/
./itemdata2json.py
./itemdata2gas.py

#/usr/local/bin/grftool data.grf "data\\lua files\\skillinfoz\\skilldescript.lub" > ./export_grf/skilldescript.lub
#/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/skilldescript.lub \
# | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
# | /usr/bin/sed "s/¥//g" \
# > ./export_grf/skilldescript.lua

#/usr/local/bin/grftool data.grf "data\\lua files\\skillinfoz\\skillid.lub" > ./export_grf/skillid.lub
#/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/skillid.lub \
# | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
# | /usr/bin/sed "s/¥//g" \
# > ./export_grf/skillid.lua

/usr/local/bin/grftool data.grf "data\\lua files\\skillinfoz\\skillinfolist.lub" > ./export_grf/skillinfolist.lub
#/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/skillinfolist.lub \
# | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
# | /usr/bin/sed "s/¥//g" \
# > ./export_grf/skillinfolist.lua

/usr/local/bin/grftool data.grf "data\\lua files\\skillinfoz\\skillnamelist.lub" > ./export_grf/skillnamelist.lub
/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/skillnamelist.lub \
 | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
 | /usr/bin/sed "s/¥//g" \
 > ./export_grf/skillnamelist.lua

./lua_skilldata2json.py
cp -p skill_data.json /var/www/html/ROOD/

#cat items.json | jq '.[] | select(.is_enchant == true)' \
#> /var/www/html/ROOD/enchants.json
