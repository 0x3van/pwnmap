import re
import base64


DISCORD_EPOCH_START = 1420070400000


class DiscordToken(str):
    """ DiscordToken type string object """

    def __init__(self, token):
        try:
            if re.match(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}', token) is None:
                raise Exception()

            token_parts = token.split('.')

            b64snowflake = token_parts[0]

            if b64snowflake != 'mfa':
                snowflake = base64.b64decode(b64snowflake.encode()).decode()
                snowflake = int(snowflake)

                if (snowflake >> 22) + DISCORD_EPOCH_START < DISCORD_EPOCH_START:
                    raise Exception()

        except Exception:
            raise ValueError('Invalid Discord token')
