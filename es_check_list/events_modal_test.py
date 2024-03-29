# -*- coding: utf-8 -*-

from page import USERNAME_SECOND, USERNAME_FIRST, Page, PersonPage
from BasicTest import BasicTest


class HasNewEventTest(BasicTest):
    def test(self):
        mark_value = 5
        marks = [mark_value]

        photos = self.upload_photo(USERNAME_SECOND)
        self.photos = photos
        name = self.get_name(USERNAME_FIRST)
        self.set_marks(None, photos, marks)

        self.login(USERNAME_SECOND)

        page = Page(self.driver)
        events_modal = page.top_menu.events_modal
        events_modal.open()

        self.assertTrue(events_modal.check_mark(name, marks[0]))


class CheckMarksEventTest(BasicTest):
    def test(self):
        mark_value = 5
        marks = [mark_value]

        photos = self.upload_photo(USERNAME_SECOND)
        self.photos = photos
        name = self.get_name(USERNAME_FIRST)
        self.set_marks(None, photos, marks)

        self.login(USERNAME_SECOND)
        person_page = PersonPage(self.driver, '')
        events_modal = person_page.top_menu.events_modal
        events_modal.open()

        marks_modal = events_modal.marks_modal
        self.assertTrue(marks_modal.open(True))
        result = marks_modal.check_mark(marks[0], name)

        self.assertTrue(result)


class RemoveMarkEventTest(BasicTest):
    def test(self):
        mark_value = 5
        marks = [mark_value]

        photos = self.upload_photo(USERNAME_SECOND)
        self.photos = photos
        name = self.get_name(USERNAME_FIRST)
        self.set_marks(None, photos, marks)

        self.login(USERNAME_SECOND)

        page = Page(self.driver)
        events_modal = page.top_menu.events_modal
        events_modal.open()

        photo = events_modal.get_photo()

        marks_modal = events_modal.marks_modal
        marks_modal.open(True)

        marks_modal.remove(name)

        page.open()
        events_modal.open()

        self.assertNotEqual(photo, events_modal.get_photo())


class CancelRemoveMarkEventTest(BasicTest):
    def test(self):
        mark_value = 5
        marks = [mark_value]

        photos = self.upload_photo(USERNAME_SECOND)
        self.photos = photos
        name = self.get_name(USERNAME_FIRST)
        self.set_marks(None, photos, marks)

        self.login(USERNAME_SECOND)

        page = Page(self.driver)
        events_modal = page.top_menu.events_modal
        events_modal.open()

        marks_modal = events_modal.marks_modal

        self.assertTrue(marks_modal.open(True))

        marks_modal.remove(name)
        marks_modal.cancel_remove()
        result = self.check_marks(None, photos, marks, name, False)

        self.assertTrue(result)
