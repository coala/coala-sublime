import unittest

from Utils import log, retrieve_stdout


class UtilsTest(unittest.TestCase):

    def test_retrieve_stdout(self):
        with retrieve_stdout() as sio:
            print("test")
            self.assertEqual(sio.getvalue(), "test\n")

    def test_log(self):
        with retrieve_stdout() as sio:
            log("test")
            self.assertEqual(sio.getvalue(), " COALA - test\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)
