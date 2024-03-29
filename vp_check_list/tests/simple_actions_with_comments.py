# -*- coding: utf-8 -*-

from selenium.webdriver.support.wait import WebDriverWait

from vp_check_list.elements.avatar import LastCommentUserAvatar
from vp_check_list.tests.base_test import BaseTest


class SimpleActionsWithCommentsTest(BaseTest):
	TEST_COMMENT = 'Test comment'

	@classmethod
	def setUpClass(cls):
		super(SimpleActionsWithCommentsTest, cls).setUpClass()
		cls.user_avatar.open_avatar()

	def setUp(self):
		self.avatar_footer = self.user_avatar.comments

		self.avatar_footer.add_comment_to_avatar(self.TEST_COMMENT)

	def tearDown(self):
		self.avatar_footer.delete_comment_from_avatar()

	def test_like_comment(self):
		last_comment = self.avatar_footer.last_comment
		like_before = self.avatar_footer.last_comment.is_like()

		self.avatar_footer.last_comment.like()

		WebDriverWait(self.avatar_footer.last_comment, 15, 0.1).until(
			lambda d: like_before != d.is_like()
		)
		like_after = self.avatar_footer.last_comment.is_like()

		self.assertNotEqual(like_before, like_after)

	def test_repost_comment(self):
		repost_before = self.avatar_footer.last_comment.repost_count()
		self.avatar_footer.last_comment.repost()

		WebDriverWait(self.avatar_footer.last_comment, 15, 0.1).until(
			lambda d: repost_before != d.repost_count()
		)
		repost_after = self.avatar_footer.last_comment.repost_count()

		self.assertNotEqual(repost_before, repost_after)
