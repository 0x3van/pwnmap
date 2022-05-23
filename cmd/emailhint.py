import os

from cumware.command import Command
from cumware.logger import Logger
from cumware.type import Email


class EmailHintCommand(Command):
    name = 'emailhint'
    description = 'Guess domain of censored email'

    @Command.execute
    def run(self, email: Email):
        email_name, email_domain = email.split('@')

        with open(os.path.join('data', 'domains.txt')) as f:
            domains = [x.strip() for x in f.readlines() if len(x.strip()) > 0]

        def __guess_domain(email_domain: str, domain: str) -> bool:
            """ Guess censored domain of email """
            if len(email_domain) != len(domain):
                return False

            char_poses = []

            for char_pos, char in enumerate(email_domain):
                if char != '*':
                    char_poses.append((char_pos, char))

            for char_pos, char in char_poses:
                if domain[char_pos] != char:
                    return False

            return True

        valid_domains = [domain for domain in domains if __guess_domain(email_domain, domain) is True]

        if len(valid_domains) == 0:
            raise Exception('Failed to guess email domain')

        for domain in valid_domains:
            Logger.success(f'{email} => {email_name}@{domain}')
