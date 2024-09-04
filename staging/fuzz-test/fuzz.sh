#!/bin/bash
WLR_RENDER_DRM_DEVICE=/dev/dri/renderD128 WLR_BACKENDS=headless wayfire -c wayfire.ini &>/tmp/outerlog &
sleep 1
display=$(cat /tmp/outerlog | grep "Using socket name" | cut -d ' ' -f 9)

while true; do
	WAYLAND_DISPLAY=$display python fuzz.py
done
