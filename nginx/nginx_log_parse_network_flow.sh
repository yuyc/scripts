#!/bin/bash
logfile=/data/nginx_logs/access.log

function feng() {
	read -p "请输入开始时间(10:30:00)秒数不输入默认为00: " a
	read -p "请输入结束时间(10:35:00)秒数不输入默认为00: " b
	if [[ "$a" =~ ^[0-9]{2}:[0-9]{2}:[0-9]{2}$ ]]
	then
		time_qing=`date +'['%d/%b/%Y:`$a
	else
		time_qing=`date +'['%d/%b/%Y:`$a":00"
	fi

	if [[ "$b" =~ ^[0-9]{2}:[0-9]{2}:[0-9]{2}$ ]]
	then    
		time_hou=`date +'['%d/%b/%Y:`$b
	else
		time_hou=`date +'['%d/%b/%Y:`$b":00"
	fi
	awk_value=`awk -v a=$time_qing -v b=$time_hou 'BEGIN{if (a>b) print "yes"}'`
}
feng
awk -v a=$time_qian -v b=$time_hou  '{if ($13>a && $13<b && $2 ~ /(www.boqii.com|bbs.boqii.com|s.boqii.com|shop.boqii.com|shopapi.boqii.com|vet.boqii.com|zhuanti.boqii.com|a.boqiicdn.com)/) print $0}'  $logfile |awk -F\" '{if($(NF-3) != "-")print $(NF-3),$(NF-1)}' | awk '{a[$1]=a[$(NF-1)]+$NF}END{for(i in a)print a[i]/1024/1024"MB",i}' | sort -rn -k 1 | head -10
