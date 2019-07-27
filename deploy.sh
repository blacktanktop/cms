#!/bin/bash -eux

# read variable in conf
source "$(dirname $0)/bin/conf"

[ "$USER" = "root" ]

# remove contents
rm -rf "${contentsdir:?}"
# move contents dir
cd "$wwwdir"
# clone contents
git clone "https://github.com/$contents_owner/$contents"
chown www-data:www-data "$contentsdir" -R
