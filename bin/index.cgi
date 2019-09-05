#!/bin/bash -euvx
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"
# パイプライン中のエラーでも止まるようにする
set -o pipefail
# このシェルスクリプトが終わるときに'処理'を実行
trap 'rm -f $tmp-*' EXIT

## variables
# md="$contentsdir/posts/template/main.md"
# tr -dc:指定文字列以外は削除
# sed 's;変換前;変換後;' ;でなく/を使ってもいいがその時はエスケープ
# QUERY_STRINGにhttps://blog.blacktanktop.me?XXXXXのXXXXXが入るイメージ
# $$はプロセス番号
tmp=/tmp/$$
dir="$(tr -dc 'a-zA-Z0-9_=' <<< ${QUERY_STRING} | sed 's;=;s/;')"
# -z は文字列が長さが0なら真つまり空ならdir="pages/top"
[ -z "$dir" ] && dir="pages/top"
# 最新postのpathをdirに代入
[ "$dir" = "post" ] && dir="$(tail -n 1 "$datadir/post_list" | cut -d' ' -f 3)" 
md="$contentsdir/$dir/main.md"
#実際のファイルかどうか
[ -f "$md" ]

## make metadata
# URLに入力された場所（記事dir）に対してファイルを作成
counter="$datadir/counters/$(tr '/' '_' <<< $dir)"
# 都度1と追記。それをファイルサイズでカウントする'$(ls -l "$counter" | cut -d' ' -f 5)'
echo -n 1 >> "$counter" # increment the counter

cat << FIN | tee /tmp/hogehoge > $tmp-meta.yaml
---
created_time: '$(date -f - < "$datadir/$dir/created_time")'
modified_time: '$(date -f - < "$datadir/$dir/modified_time")'
title: '$(cat "$datadir/$dir/title")'
nav: '$(cat "$datadir/$dir/nav")'
views: '$(ls -l "$counter" | cut -d' ' -f 5)'
$(cat "$contentsdir/config.yaml" )
---
FIN

#make html
#echo -e "Content-type: text/html\n"
pandoc --template="$viewdir/template.html" \
	-f markdown_github+yaml_metadata_block "$md" "$tmp-meta.yaml"		|
# :// または"/を含まないのが対象
# <(img src|a href) は <img src="または<a href)にマッチしたら
# マッチした後ろに/$dir/をつける
sed -r "/:\/\/|=\"\//!s;<(img src|a href)=\";&/$dir/;"	            	|
# リンク内移動用の復旧
# href=#white"がhref="/$dir/#white"となるが、それを元に戻す
sed "s;/$dir/#;#;g"                                                     |
# gihub-markdownのリンク先勝手に表示しちゃう問題対策
# href="<a href="の後ろの文字列をhref=後ろの文字列という変換にする
sed 's;href="<a href="\(.*\)"[^>]*>.*</a>";href="\1";'
