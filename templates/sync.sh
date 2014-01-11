#!/bin/sh
target=/etc/tinc/unet/hosts
mkdir .sync_unet
{% for f in names%}curl 2>/dev/null http://{{host}}{{url_for('list_item',name=f)}} > .sync_unet/{{f}}
{% endfor %}
cp -f .sync_unet/* $target
rm -rf .sync_unet
