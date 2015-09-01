# coding: utf-8
# author: maxint <NOT_SPAM_lnychina@gmail.com>

import unittest
import downimg
import os
import logutils


class DownloadImageTest(unittest.TestCase):
    tmp_img_path = 'tmp.gif'
    test_log_path = 'test.log'

    def setUp(self):
        logutils.setup_logging('webgrab', self.test_log_path)
        self.removeTempFiles()

    def tearDown(self):
        self.removeTempFiles()

    def removeTempFiles(self):
        if os.path.exists(self.tmp_img_path):
            os.remove(self.tmp_img_path)

    def testDownloadNormal(self):
        url0 = 'https://www.baidu.com/img/baidu.gif'
        url = downimg.down_image(url=url0, dst=self.tmp_img_path)
        self.assertEqual(url0, url)
        self.assertTrue(os.path.exists(self.tmp_img_path))
        self.removeTempFiles()

    def testDownloadRetry(self):
        url0 = 'https://www.aaa.com/img/baidu.gif'
        self.assertRaises(IOError, lambda : downimg.down_image(url=url0, dst=self.tmp_img_path))
        self.assertFalse(os.path.exists(self.tmp_img_path))
        self.removeTempFiles()


if __name__ == '__main__':
    unittest.main()