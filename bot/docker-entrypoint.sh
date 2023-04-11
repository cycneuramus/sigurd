#!/bin/sh -e

case $1 in
	bot)
		exec python sigurd.py
		;;
	cron)
		exec supercronic -passthrough-logs tasks/cron
		;;
esac
