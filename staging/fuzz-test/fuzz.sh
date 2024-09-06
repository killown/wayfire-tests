#!/bin/bash
WLR_RENDER_DRM_DEVICE=/dev/dri/renderD128 WLR_BACKENDS=headless wayfire -c wayfire.ini &>/tmp/outerlog &
sleep 2
display=$(cat /tmp/outerlog | grep "Using socket name" | cut -d ' ' -f 9)

while true; do
	python fuzz.py $display
done
