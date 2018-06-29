from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class RelationTestCase(TestCase):
    def test_follow(self):
        """
        특정 User가 다른 User를 follow했을 경우, 정상 작동하는지 확인
        :return:
        """
        # 임의의 유저 2명 생성 (u1, u2)
        u1 = User.objects.create_user(username='u1')
        u2 = User.objects.create_user(username='u2')

        # u1이 u2를 follow하도록 함
        relation = u1.relations_by_from_user.create(to_user=u2, relation_type='f')

        # u1의 following에 u2가 포함되어 있는지 확인
        self.assertIn(u2, u1.following)

        # u1의 following_relations에서 to_user가 u2인 Relation이 존재하는지 확인
        self.assertTrue(u1.following_relations.filter(to_user=u2).exists())

        # relation이 u1.following_relations에 포함되어있는지
        self.assertIn(relation, u1.following_relations)
