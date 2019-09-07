import asyncio
import re
import requests
from aiosmtpd.controller import Controller
import os
import logging

logging.basicConfig(level=logging.INFO)

_logger = logging.getLogger(__name__)

class CustomHandler:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = os.getenv('MAIL_DOMAIN', 'localhost')
        self.ping_url = os.getenv('PING_URL', 'https://healthcheck.io/ping/')
        _logger.debug('Mail domain: %s', self.domain)
        _logger.debug('Mail ping url: %s', self.ping_url)

    async def handle_DATA(self, server, session, envelope):
        peer = session.peer
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos
        data = envelope.content         # type: bytes
        for rcpt in rcpt_tos:
            _logger.debug('Cecking to address: %s', rcpt)
            match = re.match(f'([a-zA-Z-_0-9]+)@{self.domain}', rcpt)
            if match is not None:
                _logger.debug('match found: %s', rcpt)
                found = match
                break
        else:
            _logger.debug('no match found')
            return '500 Could not process your message'
        headers= { 'User-Agent': 'EmailPing from ' + mail_from }
        url = f'{self.ping_url}{match.group(1)}'
        _logger.info('Calling Ping url: %s for address: %s', url, mail_from)
        requests.get(url, headers=headers)
        return '250 OK'

async def health_check():
    ping_url = os.getenv('PING_URL', 'https://healthcheck.io/ping/')
    ping_id = os.getenv('PING_ID', '101fcaa8-32c5-4281-936f-330412b7afa4')
    ping_timeout = int(os.getenv('PING_TIMEOUT', '60'))
    _logger.info('Reporting own health to: %s', f'{ping_url}{ping_id}')
    while True:
        requests.get(f'{ping_url}{ping_id}')
        await asyncio.sleep(ping_timeout)

if __name__ == '__main__':
    handler = CustomHandler()
    controller = Controller(handler, hostname='127.0.0.1', port=10025)
    # Run the event loop in a separate thread.
    controller.start()
    # Wait for the user to press Return.
    loop = asyncio.get_event_loop()
    loop.create_task(health_check())
    loop.run_forever()
