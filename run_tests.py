#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import unittest
from like_tests.tests.auth import LoginTest, LogoutTest
from like_tests.tests.photo import ClassPhotoTest


if __name__ == '__main__':
    suite = unittest.TestSuite((
        # unittest.makeSuite(LoginTest),
        # unittest.makeSuite(LogoutTest)
        unittest.makeSuite(ClassPhotoTest)
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
