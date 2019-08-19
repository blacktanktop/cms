#!/bin/bash -euxv
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

word=$(nkf --url-input <<< ${QUERY_STRING} | sed 's/^key=//')

# 降順に並べる
tac "$datadir/keyword_list"     |
# リストから同じkeywordの行を抽出
grep -F ",$word,"               |
# pathを抽出
awk '{print $1}'                |
# リンク化
xargs -I@ cat "$datadir/@/link" |
# pandocでリスト化
# 先頭に*つける
sed 's/^/* /'                   |
# 先頭行に Keyword: $wordをつける
sed "1i# Keyword: $word"        |
pandoc --template="$viewdir/template.html" 
