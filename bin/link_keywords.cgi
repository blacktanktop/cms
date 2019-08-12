#!/bin/bash -xv
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

echo -e 'Content-Type: text/html\n'
# ブラウザーがURLエンコードしたものを変換しまくる
# %2Cは,のことなので,をキーに改行
sed 's/%2C/\n/g' <<< ${QUERY_STRING}                       |
# 一旦デコード
nkf --url-input                                            |
# keywords=と半角空白除去
sed -e '1s/keywords=//' -e 's/^[ 　]*//' -e 's/[ 　]*$//'  |
# BOMなしビックエンディアンUTF-16
nkf -w16B0                                                 |
# バイナリを 16進数へ
xxd -plain                                                 |
# 適当な改行除去
tr -d '\n'                                                 |
# 2バイトずつ区切ってから000aで改行
sed 's/..../\&#x&;/g'                                      |
sed 's/\&#x000a;/\n/g'                                     |
# リンク化
awk '{print "<a href=\"/key.cgi?key="$1 "\">" $1 "</a>" }' 

