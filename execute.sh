#!/bin/bash
cd /opt/grf-analysis-tools

./export_grf2text.py --grf-path /opt/grf-files/data.grf

./itemdata2text.py 
cp -p items.json /var/www/html/ROOD/
cp -p items.jsonl /var/www/html/ROOD/
cp -p items.yaml /var/www/html/ROOD/

./itemdata2gas.py

./export_grf2itemimg.py --grf-path /opt/grf-files/data.grf --export-path-imgdir /var/www/html/ROOD/items/

#./pygrf/grftool.py ../grf-files/data.grf "data/luafiles514/lua files/skillinfoz/skillinfolist.lub" > ./export_grf/skillinfolist.lub
#/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/skillinfolist.lub \
# | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
# | /usr/bin/sed "s/¥//g" \
# > ./export_grf/skillinfolist.lua

#/usr/local/bin/grftool data.grf "data/luafiles514/lua files/skillinfoz/skillid.lub" > ./export_grf/skillid.lub
#/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/skillid.lub \
# | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
# | /usr/bin/sed "s/¥//g" \
# > ./export_grf/skillid.lua

#./lua_skillinfo2text.py
#cp -p skill_list.json /var/www/html/simulator/data/
#cp -p skill_list.yaml /var/www/html/simulator/data/

#/usr/local/bin/grftool data.grf "data/luafiles514/lua files/stateicon/efstids.lub" > ./export_grf/efstids.lub
#/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/efstids.lub \
# | /usr/bin/iconv -f EUC-KR -t UTF-8 \
# | /usr/bin/sed "s/¥//g" \
# > ./export_grf/efstids.lua

#/usr/local/bin/grftool data.grf "data/luafiles514/lua files/stateicon/stateiconimginfo.lub" > ./export_grf/stateiconimginfo.lub
#/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/stateiconimginfo.lub \
# | /usr/bin/iconv -f EUC-KR -t UTF-8 \
# | /usr/bin/sed "s/¥//g" \
# > ./export_grf/stateiconimginfo.lua
