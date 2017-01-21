import unittest

from metrics.edu_mails import is_edu_mail
import subprocess
from metrics.repoMetrics import count_file_with_ending


class TestMetrics(unittest.TestCase):
    def test_is_edu_mail(self):
        self.assertTrue(is_edu_mail('mbornste@uni-potsdam.de'))
        self.assertTrue(is_edu_mail('marvin.bornstein@student.hpi.uni-potsdam.de'))
        self.assertFalse(is_edu_mail('mail@mbornstein.de'))

    def test_edu_mail_metric(self):
        result = subprocess.check_output('git shortlog -sne | grep "<"', shell=True).decode('utf-8')
        self.assertTrue('marvin' in result)

    def test_ending_counter(self):
        self.assertEqual(count_file_with_ending('.', '.md', absolute=True), 1)
        self.assertTrue(count_file_with_ending('.', '.md') < 1)

if __name__ == '__main__':
    unittest.main()
