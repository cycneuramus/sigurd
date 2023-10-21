FROM python:3.10

ARG USER=sigurd
ARG HOME_DIR=/home/$USER
ARG BOT_DIR=$HOME_DIR/bot

ENV SUPERCRONIC_URL https://github.com/aptible/supercronic/releases/download/v0.1.12/supercronic-linux-amd64
ENV SUPERCRONIC supercronic-linux-amd64
ENV SUPERCRONIC_SHA1SUM 048b95b48b708983effb2e5c935a1ef8483d9e3e

# RUN apk add --no-cache --update \
# 	curl \
# 	tzdata

RUN curl -fsSLO "$SUPERCRONIC_URL" \
	&& echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
	&& chmod +x "$SUPERCRONIC" \
	&& mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
	&& ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

RUN adduser \
	--disabled-password \
	--uid 1000 \
	$USER

USER $USER

RUN mkdir -p $BOT_DIR
ENV PYTHONPATH=$BOT_DIR

RUN pip install --no-cache-dir \
	EdgeGPT \
	GoogleBard \
	hugchat \
	langchain \
	lyricsgenius \
	openai \
	pydub \
	revChatGPT \
	semaphore-bot \
	signalbot \
	tekore \
	tinydb

WORKDIR $BOT_DIR

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
