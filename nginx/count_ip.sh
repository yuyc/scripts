#!/bin/bash
function core(){
    for i in `ls /data/nginx_logs/*$1*`;do
        awk '{print $10}' $i >>request_ip_count_$1.log
    done
    count_ip=`sort -u request_ip_count_$1.log|wc -l`
    echo "每天的IP访问量:$count_ip"
}

function menu(){
    echo "本脚本用来分析某天的IP访问量"
    read -p "请输入日期,如20160331:" count_date
    core $count_date
}
menu

