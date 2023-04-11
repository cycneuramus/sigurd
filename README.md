# Sigurd

Sigurd is an example chatbot for Signal built on the [`signalbot`](https://github.com/filipre/signalbot) framework. Features:

+ Responds quite rudely, especially to negative feedback.
+ Caches responses so as never to repeat himself.
+ Keeps quiet unless his name is mentioned, or unless he receives a `!` prefixed command.
+ Quotes random song lyrics on demand (e.g. `!lyrics Symphony X`).
+ Notifies you of new releases from [artists that you wish to track](bot/utils/spotify_data.py).
+ Performs tasks according to a [`cron`](bot/tasks/cron) schedule.

<p>
	<img src="screenshots/chat.png" width=250 />
	<img src="screenshots/lyrics.png" width=250 />
	<img src="screenshots/release-radar.png" width=250 />
</p>

## Installation

+ Register a Signal account for Sigurd (you will need a dedicated phone number for this).

+ Install and configure [`signal-cli`](https://github.com/AsamK/signal-cli/).

+ Clone this repo:
	- ```
	git clone https://github.com/cycneuramus/sigurd
	```

+ Populate the `.env` file:
	- `BOT_PHONE`: Phone number for Sigurd's Signal account.
	- `SELF_PHONE`: Phone number for your own Signal account, or any other phone number that Sigurd should respond to.
	- `GROUP_ID`: Signal group for Sigurd to participate in, if any.
	- `GENIUS_ACCESS_TOKEN`: Required for the [`!lyrics`](bot/commands/lyrics.py) command. See the [Genius API docs](https://docs.genius.com/).
	- `NTFY_URL`: [ntfy](https://ntfy.sh) server to use. Required for the [`release_radar`](bot/tasks/release_radar/release_radar.py) task to send notifications.
	- `SPOTIFY_CLIENT_*`: Required for the [`release_radar`](bot/tasks/release_radar/release_radar.py) task. See the [Spotify API docs](https://developer.spotify.com/documentation/web-api).
	- `SIGNAL_SERVICE`: Hostname for the `signal-cli` REST API service in `docker-compose.yml`.

+ Spin up the Docker containers:
	- `docker compose up -d`
