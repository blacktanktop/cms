#!/bin/bash
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

# 数字以外は消去
num=$(tr -dc '0-9' <<< ${QUERY_STRING})
[ -z "$num" ] && num=10

echo -e "Content-Type: text/html\n\n<h1>直近記事</h1>"
# 逆順 tail -r
tac "$datadir/post_list"             |
head -n "$num"                       |
awk '{print $3}'                     |
xargs -I@ cat "$datadir/@/link_date" |
sed 's;$;<br />;'
