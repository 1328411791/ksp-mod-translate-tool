import unittest

from tools.Youdao import Youdao


class MyTestCase(unittest.TestCase):
    def test_youdao(self):
        client = Youdao(app_key="2ce26d4129c75fa0", app_secret="DFuJTn264xHGmuZatejL8j2c1553axfP");
        word = client.translate_word("hello")


if __name__ == '__main__':
    unittest.main()
