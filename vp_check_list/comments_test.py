# -*- coding: utf-8 -*-

from vp_check_list.base_test import BaseTest


class SimpleActionsWithCommentsTest(BaseTest):
	TEST_COMMENT = 'Test comment'

	def test_add_comment(self):
		avatar = self.user_avatar.get_avatar()
		self.user_avatar.open_avatar(avatar)
		avatar_footer = self.user_avatar.comments

		avatar_footer.add_comment_to_avatar(self.TEST_COMMENT)

		comment = avatar_footer.get_last_comment_text()
		self.assertEqual(comment, self.TEST_COMMENT)

	def test_delete_comment(self):
		avatar = self.user_avatar.get_avatar()
		self.user_avatar.open_avatar(avatar)

		avatar_footer = self.user_avatar.comments
		comment_before_delete = avatar_footer.get_last_comment_text()

		avatar_footer.delete_comment_from_avatar()

		comment_after_delete = avatar_footer.get_last_comment_text()
		self.assertNotEqual(comment_before_delete, comment_after_delete)
