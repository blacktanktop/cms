#!/bin/bash -eux
source "$(dirname $0)/bin/conf"

[ "$USER" = "root" ]

rm -rf "${contentsdir:?}"
cd "$wwwdir"
git clone "https://github.com/$contents_owner/$contents"
chown www-data:www-data "$contentsdir" -R
