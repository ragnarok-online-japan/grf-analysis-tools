#!/bin/bash
cd /opt/grf-analysis-tools

./export_grf.py
./export_grf2itemimg.py --export-path-imgdir /var/www/html/ROOD/items/

./itemdata2text.py
cp -p items.json /var/www/html/ROOD/
cp -p items.yaml /var/www/html/ROOD/

/usr/local/bin/grftool data.grf "data\\luafiles514\\lua files\\skillinfoz\\skillinfolist.lub" > ./export_grf/skillinfolist.lub
/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/skillinfolist.lub \
 | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
 | /usr/bin/sed "s/¥//g" \
 > ./export_grf/skillinfolist.lua

/usr/local/bin/grftool data.grf "data\\luafiles514\\lua files\\skillinfoz\\skillid.lub" > ./export_grf/skillid.lub
/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/skillid.lub \
 | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
 | /usr/bin/sed "s/¥//g" \
 > ./export_grf/skillid.lua

./lua_skillinfo2text.py
cp -p skill_list.json /var/www/html/simulator/data/
cp -p skill_list.yaml /var/www/html/simulator/data/

./itemdata2gas.py

#cat items.json | jq '.[] | select(.is_enchant == true)' \
#> /var/www/html/ROOD/enchants.json
