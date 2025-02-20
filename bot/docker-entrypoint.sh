#!/bin/sh -e

case $1 in
	bot)
		exec python sigurd.py
		;;
	cron)
		exec /usr/local/bin/supercronic -passthrough-logs tasks/cron
		;;
esac
