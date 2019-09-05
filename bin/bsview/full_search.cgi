#!/bin/bash -xv

source "$(dirname $0)/../conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

word=$(nkf --url-input <<< ${QUERY_STRING} | sed 's/^word=//' )
numchar=$(nkf -w16B0 <<< "$word" | xxd -plain | tr -d '\n' | sed 's/..../\&#x&;/g')

# ヘッダー
# タイトル
# 検索ボックス
# 送信ボタン
cat << FIN
Content-Type: text/html

<h1>検索結果: $numchar</h1>
FIN

# -n:文字列長が 0 より大なら真
[ -n "$word" ] &&
# 逆順
tac "$datadir/all_markdown"             |
# path側を検索から外すために半角スペースを入れている
# grep以外には$wordは使わない！！
grep " .*$word"                         |
awk '{print $1}'                        |
uniq                                    |
# 100行に限定
head -n 100                             | 
xargs -I@ cat "$datadir/@/link_date"    |
sed 's;$;<br/>;'
