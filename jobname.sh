#!/bin/bash
cd /opt/grf-analysis-tools

../pygrf/grftool.py ../grf-files/data.grf "data/luafiles514/lua files/datainfo/pcjobname.lub" > ./export_grf/pcjobname.lub
/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/pcjobname.lub \
 | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
 | /usr/bin/sed "s/¥//g" \
 > ./export_grf/pcjobname.lua

../pygrf/grftool.py ../grf-files/data.grf "data/luafiles514/lua files/skillinfoz/jobinheritlist.lub" > ./export_grf/jobinheritlist.lub
/usr/bin/java -jar ./unluac/unluac.jar --rawstring ./export_grf/jobinheritlist.lub \
 | /usr/bin/iconv -f SHIFT-JIS -t UTF-8 \
 | /usr/bin/sed "s/¥//g" \
 > ./export_grf/jobinheritlist.lua

./jobname2text.py > /dev/null
