#!/bin/bash
# 邮件功能请参考“scripts/mail”目录中的sendmail.py脚本
usedmem=`/usr/local/bin/redis-cli info memory | awk -F: '$1 ~ /used_memory_human/{print $2}' | awk -F "G" '{print $1}'`
warnmem=8.5
title="[Redis] mem is above norm"
unit="G"
echo "userdmem:$usedmem,title:$title,unit:$unit"
if [ $(echo "$usedmem > $warnmem"|bc) -eq 1 ];
then
        python /scripts/sendmail.py "yuyc@boqii.com" "$title" "mem:$usedmem$unit"
    echo $?
fi
