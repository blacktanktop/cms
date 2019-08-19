#!/bin/bash
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

num=$(tr -dc '0-9' <<< ${QUERY_STRING})
[ -z "$num" ] && num=10

# -U:ソートしない出力
ls -lU "$datadir/counters"  |
tail -n +2                  |
# $NF:最終列
awk '{print $5,$NF}'        |
# _を/へ置換
sed 's;_;/;'                |
# -s:同順ならそのまま
# -n:数字順で小さい順
# -k1,1:1列目から1列目まで
# r:逆順
sort -s -k1,1nr             |
# 指定数
head -n "$num"              |
while read pv d ; do
    sed "s;</a>;($pv views)&<br />;" "$datadir/$d/link"
done |
sed '1iContent-Type: text/html\n\n<h1>PV Ranking</h1>'
