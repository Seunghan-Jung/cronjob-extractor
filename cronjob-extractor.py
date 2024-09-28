import re
import gzip
import glob
from collections import defaultdict
from typing import NewType, Set


User = NewType('User', str)
Command = NewType('Command', str)

CRON_LOG_PATTERN = r'.*CRON\[\d+\]: \((\w+)\) CMD \((.*)\)'


def insert_escape_char(_cmd: Command) -> Command:
    chars = ['\\', '"', '|', '*', '%', '!', '(', ')', '[', ']', '{', '}', ';', '?', '~', '#', '@', '=', ':', ',', '^']
    for char in chars:
        _cmd = _cmd.replace(char, f'\\{char}')
    return _cmd


def extract_user2cmd(file_path: str, user2cmd: defaultdict[User, Set[Command]]):
    open_func = gzip.open if file_path.endswith('.gz') else open

    with open_func(file_path, 'rt') as file:
        for line in file:
            match = re.search(CRON_LOG_PATTERN, line)
            if match:
                user = match.group(1)
                cmd = match.group(2)
                user2cmd[user].add(cmd)

if __name__ == "__main__":
    user2cmd: defaultdict[User, Set[Command]] = defaultdict(set)
    log_files = glob.glob('/var/log/syslog*')

    for file_path in log_files:
        extract_user2cmd(file_path, user2cmd)

    for user, cmds in user2cmd.items():
        print(f"User: {user}")
        for cmd in cmds:
            print(f"  Command: {cmd}")
