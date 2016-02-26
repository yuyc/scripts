logfile=./nginx_20160225.log.10
function list(){
	clear 
	cat -n top20.log
	read -p "请输入ip编号：" ipid
	ip=`sed -n ${ipid}p top20.log|awk '{print $2}'`
	grep $ip sql.log
	echo ----------------------------------------------------------------
	echo 
	echo 
	}
function menu(){
    echo -e "******************\033[34;7m 功能选择\033[0m******************"
    echo "*            1、根据活跃ip查看注入日志      *"
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
echo ------------------------SQL注入攻击sql.log----------------
echo "开始分析存在SQL注入的攻击行为，并将结果保存在当前目录下"
more $logfile |egrep "%20select%20|%20and%201=1|%20and%201=2|%20exec|%27exec| information_schema.tables|%20information_schema.tables|%20where%20|%20union%20|%20SELECT%20|%2ctable_name%20|cmdshell|%20table_schema|sleep" >sql.log
echo "分析结束"
awk '{print "共检测到SQL注入攻击" NR"次"}' sql.log|tail -n1
echo "开始统计SQL注入攻击事件中，出现频率最多的前20个IP地址"
cat sql.log |awk  '{print $10}' |sort |uniq -c |sort -rn |head -20 >top20.log
echo ----------------------------------------------------------
while true
do
	menu	
done
echo ----------------------------------------------------------

echo "统计结束"
