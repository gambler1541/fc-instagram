from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

from .exceptions import RelationNotExist, DuplicateRelationException

User = get_user_model()


class RelationTestCase(TransactionTestCase):
    def create_dummy_user(self, num):
        # num에 주어진 개수만큼 유저를 생성 및 리턴
        return [User.objects.create_user(username=f'u{x + 1}') for x in range(num)]

    def test_follow(self):
        """
        특정 User가 다른 User를 follow했을 경우, 정상 작동하는지 확인
        :return:
        """
        # 임의의 유저 2명 생성 (u1, u2)
        u1 = User.objects.create_user(username='u1')
        u2 = User.objects.create_user(username='u2')

        # u1이 u2를 follow하도록 함
        relation = u1.follow(u2)
        # relation = u1.relations_by_from_user.create(to_user=u2, relation_type='f')

        # u1의 following에 u2가 포함되어 있는지 확인
        self.assertIn(u2, u1.following)

        # u1의 following_relations에서 to_user가 u2인 Relation이 존재하는지 확인
        self.assertTrue(u1.following_relations.filter(to_user=u2).exists())

        # relation이 u1.following_relations에 포함되어있는지
        self.assertIn(relation, u1.following_relations)

    def test_follow_only_once(self):
        u1 = User.objects.create_user(username='u1')
        u2 = User.objects.create_user(username='u2')

        # u2로의 follow를 실행
        u1.follow(u2)

        # 두 번째 실행에서는 IntegrityError가 발생할 것이다
        # with transaction.atomic():
        with self.assertRaises(DuplicateRelationException):
            u1.follow(u2)

        # u1의 following이 하나인지 확인
        self.assertEqual(u1.following.count(), 1)

    def test_unfollow_if_follow_exist(self):
        u1, u2 = self.create_dummy_user(2)

        # u1이 u2를 follow후 unfollow실행
        u1.follow(u2)
        u1.unfollow(u2)

        # u1의 following에 u2가 없어야 함
        self.assertNotIn(u2, u1.following)

    def test_unfollow_fail_if_follow_not_exist(self):
        u1, u2 = self.create_dummy_user(2)

        # 아래 코드는 올바르지 않아야 함 (Exception이 발생해야 함)
        with self.assertRaises(RelationNotExist):
            u1.unfollow(u2)
