import unittest

from metrics.edu_mails import is_edu_mail
import subprocess


class TestMetrics(unittest.TestCase):
    def test_is_edu_mail(self):
        self.assertTrue(is_edu_mail('mbornste@uni-potsdam.de'))
        self.assertTrue(is_edu_mail('marvin.bornstein@student.hpi.uni-potsdam.de'))
        self.assertFalse(is_edu_mail('mail@mbornstein.de'))

    def test_edu_mail_metric(self):
        result = subprocess.check_output('git shortlog -sne | grep "<"', shell=True).decode('utf-8')
        self.assertTrue('marvin' in result)

if __name__ == '__main__':
    unittest.main()
