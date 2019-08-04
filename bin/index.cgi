#!/bin/bash -euvx
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

# Variables
# md="$contentsdir/posts/template/main.md"
# tr -dc:指定文字列以外は削除
# sed 's;変換前;変換後;' ;でなく/を使ってもいいがその時はエスケープ
# QUERY_STRINGにhttps://blog.blacktanktop.me?XXXXXのXXXXXが入るイメージ

dir="$(tr -dc 'a-zA-Z0-9_=' <<< ${QUERY_STRING} | sed 's;=;s/;')"
md="$contentsdir/$dir/main.md"
#実際のファイルかどうか
[ -f "$md" ] 

#make html
echo -e "Content-type: text/html\n"
pandoc --template="$viewdir/template.html" \
	-f markdown_github+yaml_metadata_block "$md"		|
# :// または"/を含まないのが対象
# <(img src|a href) は <img src="または<a href)にマッチしたら
# マッチした後ろに/$dir/をつける
sed -r "/:\/\/|=\"\//!s;<(img src|a href)=\";&/$dir/;"		|
# リンク内移動用の復旧
# href=#white"がhref="/$dir/#white"となるが、それを元に戻す
sed "s;/$dir/#;#;g"
