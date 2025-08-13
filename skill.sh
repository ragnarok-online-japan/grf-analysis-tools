#!/bin/bash
cd /opt/grf-analysis-tools

../pygrf/grftool.py ../grf-files/data.grf "data/luafiles514/lua files/skillinfoz/skillinfolist.lub" > ./export_grf/skillinfolist.lub
/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/skillinfolist.lub \
 | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
 | /usr/bin/sed "s/¥//g" \
 > ./export_grf/skillinfolist.lua

../pygrf/grftool.py ../grf-files/data.grf "data/luafiles514/lua files/skillinfoz/skillid.lub" > ./export_grf/skillid.lub
/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/skillid.lub \
 | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
 | /usr/bin/sed "s/¥//g" \
 > ./export_grf/skillid.lua

./skillinfo2text.py > /dev/null
