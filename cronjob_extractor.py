import re
import gzip
import glob
from collections import defaultdict
from typing import NewType, Set, DefaultDict

User = NewType('User', str)
Command = NewType('Command', str)

CRON_LOG_PATTERN = r'.*CRON\[\d+\]: \((\w+)\) CMD \((.*)\)'

def insert_escape_char(_cmd: Command) -> Command:
    chars = ['\\', '"', '|', '*', '%', '!', '(', ')', '[', ']', '{', '}', ';', '?', '~', '#', '@', '=', ':', ',', '^']
    for char in chars:
        _cmd = _cmd.replace(char, f'\\{char}')
    return _cmd


def extract_user2cmd(file_path_: str) -> DefaultDict[User, Set[Command]]:
    open_func = gzip.open if file_path_.endswith('.gz') else open
    result: DefaultDict[User, Set[Command]] = defaultdict(set)

    with open_func(file_path_, 'rt') as file:
        for line in file:
            match = re.search(CRON_LOG_PATTERN, line)
            if match:
                user_ = User(match.group(1))
                cmd_ = Command(match.group(2))
                result[user_].add(cmd_)

    return result

if __name__ == "__main__":
    user2cmd: DefaultDict[User, Set[Command]] = defaultdict(set)
    log_files = glob.glob('/var/log/syslog*')

    for file_path in log_files:
        temp_user2cmd = extract_user2cmd(file_path)
        for user, cmds in temp_user2cmd.items():
            user2cmd[user].update(cmds)

    for user, cmds in user2cmd.items():
        print(f"User: {user}")
        for cmd in cmds:
            print(f"  Command: {cmd}")