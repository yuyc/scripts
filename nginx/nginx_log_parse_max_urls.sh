#!/bin/bash
logfile=/data/nginx_logs/access.log
function judge(){
	site=`awk -v u=$2 '$16 = $u {print $2,$10}' $logfile`
	counts=`echo "$site"| sort -u |wc -l`
	echo ""
	echo ""
	echo ""
	echo "-------------------------------------------------"
	echo "该url的访问ip数量为:"$counts
	echo "-------------------------------------------------"
	echo ""
	echo ""
	echo ""
}
function list(){
	clear 
	cat -n url_top30.log
	read -p "请输入url编号：" urlid
	url=`sed -n ${urlid}p url_top30.log|awk '{print $2}'`
	judge $url
	}
function menu(){
    echo -e "******************\033[34;7m 功能选择\033[0m******************"
    echo "*            1、根据最多访问的url进行排序   *"
    echo "*            2、exit                        *"
    echo "*********************************************"
    read -p "请输入您要选择的编号： " select
    case $select in 
	1)
	list;;
	2)
	exit;;
	*)
	exit;;
    esac
}
awk '{print $16}' $logfile |sort| uniq -c | sort -nr | head -30 >url_top30.log
while true
do
	menu	
done

