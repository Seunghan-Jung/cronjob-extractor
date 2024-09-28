import unittest
from collections import defaultdict
from typing import Set, DefaultDict
from cronjob_extractor import extract_user2cmd, User, Command

class TestCronjobExtractor(unittest.TestCase):
    def setUp(self):
        self.test_log_content = """
        Jan 1 00:00:01 myhost CRON[12345]: (user1) CMD (echo "Hello World")
        Jan 1 00:00:02 myhost CRON[12346]: (user2) CMD (ls -la)
        Jan 1 00:00:03 myhost CRON[12347]: (user1) CMD (date)
        """
        self.test_log_file = 'test_syslog'
        with open(self.test_log_file, 'w') as f:
            f.write(self.test_log_content)

    def tearDown(self):
        import os
        os.remove(self.test_log_file)

    def test_extract_user2cmd(self):
        expected_result: DefaultDict[User, Set[Command]] = defaultdict(set)
        expected_result[User('user1')].add(Command('echo "Hello World"'))
        expected_result[User('user1')].add(Command('date'))
        expected_result[User('user2')].add(Command('ls -la'))

        result = extract_user2cmd(self.test_log_file)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()