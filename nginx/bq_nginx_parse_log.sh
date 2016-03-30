#/bin/bash
incre_log=`logtail2 -f /data/nginx_logs/access.log`

echo "域名访问记录信息"

echo "$incre_log" | awk '{s[$2]++} END{for(i in s) print s[i],i}' | sort -k1nr

echo "HTTP响应码分析"

echo "$incre_log" | awk '{s[$9]++} END{for(i in s) print s[i],i}' | sort -k1nr

echo "客户端IP统计信息"
echo "$incre_log" | awk '{s[$10]++} END{for(i in s) print s[i],i}' | sort -k1nr | head -15

echo "慢响应时间统计分析"

rt=`echo "$incre_log" | awk '{print $7}' | sort -k1nr | head -15`

echo "$rt" | while read t
do
    echo "$incre_log" | awk '$7 ~ nt {print "响应时间: " nt  " 域名: "$2 " url: " $16}' nt=$t
done

