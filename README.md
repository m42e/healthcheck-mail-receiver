# Mail Receiver for Healthcheck

This is a simple docker container which acts as SMTP backend and forwards pings from mail to healthchecks.

I made this up, because the docker container I use for healthchecks does not include smtp, and I did not want do maintain this container on my own.

## Usage:

Basically run the docker container with the following environment variables set:

- `PING_URL`: The base url for the ping to healthchecks in the format `https://yourinstance.com/ping/` please do not remove the trailing slash.
- `PING_ID`: The ID to track the health of this script/container itself.
- `PING_TIMEOUT`: The time between pings for the script should be done.
- `MAIL_DOMAIN`: The domain name to accept messages for.


