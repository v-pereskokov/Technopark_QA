# -*- coding: utf-8 -*-

from like_tests.elements.page import Page
from like_tests.elements.photo.components import *

import time


class AlbumPage(Page):

    def __init__(self, driver):
        super(AlbumPage, self).__init__(driver)
        self.photo = None

    def load_photo(self, path):
        PhotoUploadButton(self.driver).load_photo(path)
        UserAlbumButton(self.driver).click()
        self.photo = Photo(self.driver)
        return self


class PhotoPage(Page):

    def __init__(self, driver, photo_url):
        super(PhotoPage, self).__init__(driver)
        self.PATH = photo_url

    def delete_photo(self):
        PhotoDeleteButton(self.driver).click()
        time.sleep(5)