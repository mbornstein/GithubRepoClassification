import unittest

from metrics.edu_mails import is_edu_mail


class TestMetrics(unittest.TestCase):
    def test_is_edu_mail(self):
        self.assertTrue(is_edu_mail('mbornste@uni-potsdam.de'))
        self.assertTrue(is_edu_mail('marvin.bornstein@student.hpi.uni-potsdam.de'))
        self.assertFalse(is_edu_mail('mail@mbornstein.de'))

if __name__ == '__main__':
    unittest.main()
