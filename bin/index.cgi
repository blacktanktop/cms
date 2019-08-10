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
cat << FIN > $tmp-meta.yaml
---
created_time: '$(date -f - < "$datadir/$dir/created_time")'
modified_time: '$(date -f - < "$datadir/$dir/modified_time")'
title: '$(grep '^# ' "$md" | sed 's/^# *//')'
nav: '$(cat "$datadir/$dir/nav")'
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
sed "s;/$dir/#;#;g"
