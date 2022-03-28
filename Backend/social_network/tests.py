import json

from django.test import TestCase
from rest_framework.test import APIClient


class SocialNetworkTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user1_data = {
            "username": "user1",
            "first_name": "First name 1",
            "last_name": "Last name 1",
            "email": "email1@gmail.com",
            "password": "password1",
            "access_token": "",
        }
        self.user2_data = {
            "username": "user2",
            "first_name": "First name 2",
            "last_name": "Last name 2",
            "email": "email1@gmail.com",
            "password": "password1",
            "access_token": "",
        }

    def create_user(self, user_data):
        return self.client.post(
            "/social_network/users/", user_data, format="json"
        )

    def assert_users_data_equal(self, user1_data, user2_data):
        self.assertEqual(user1_data["username"], user2_data["username"])
        self.assertEqual(user1_data["first_name"], user2_data["first_name"])
        self.assertEqual(user1_data["last_name"], user2_data["last_name"])
        self.assertEqual(user1_data["email"], user2_data["email"])

    def authenticate_user(self, user_data):
        user_auth_data = {
            "username": user_data["username"],
            "password": user_data["password"],
        }
        response = self.client.post(
            "/social_network/login/", user_auth_data, format="json"
        )
        response_data = json.loads(response.content)
        user_data["access_token"] = response_data["token"]
        return response

    def create_post(self, user_data, post_text):
        return self.client.post(
            "/social_network/posts/",
            {"text": post_text},
            HTTP_AUTHORIZATION=f"Token {user_data['access_token']}",
            format="json",
        )

    def like_post(self, user_data, post_id):
        return self.client.patch(
            "/social_network/users/like_post/",
            {"post_id": post_id},
            HTTP_AUTHORIZATION=f"Token {user_data['access_token']}",
            format="json",
        )

    def test_user_creation(self):
        create_user_1_response = self.create_user(self.user1_data)
        create_user_1_response_data = json.loads(
            create_user_1_response.content
        )
        self.assertEqual(create_user_1_response.status_code, 201)
        self.assert_users_data_equal(
            self.user1_data, create_user_1_response_data
        )

        create_user_2_response = self.create_user(self.user2_data)
        create_user_2_response_data = json.loads(
            create_user_2_response.content
        )
        self.assertEqual(create_user_2_response.status_code, 201)
        self.assert_users_data_equal(
            self.user2_data, create_user_2_response_data
        )

    def test_user_authentication(self):
        self.create_user(self.user1_data)
        self.create_user(self.user2_data)

        authenticate_user_1_response = self.authenticate_user(self.user1_data)
        self.assertEqual(authenticate_user_1_response.status_code, 200)

        authenticate_user_2_response = self.authenticate_user(self.user2_data)
        self.assertEqual(authenticate_user_2_response.status_code, 200)

    def test_posts_creating(self):
        self.create_user(self.user1_data)
        self.create_user(self.user2_data)

        self.authenticate_user(self.user1_data)
        self.authenticate_user(self.user2_data)

        post_1_text = "post 1 text"
        post_2_text = "post 2 text"

        create_1_post_response = self.create_post(self.user1_data, post_1_text)
        create_1_post_response_data = json.loads(
            create_1_post_response.content
        )
        self.assertEqual(create_1_post_response.status_code, 201)
        self.assertEqual(post_1_text, create_1_post_response_data["text"])

        create_2_post_response = self.create_post(self.user2_data, post_2_text)
        create_2_post_response_data = json.loads(
            create_2_post_response.content
        )
        self.assertEqual(create_2_post_response.status_code, 201)
        self.assertEqual(post_2_text, create_2_post_response_data["text"])

    def test_posts_liking(self):
        self.create_user(self.user1_data)
        self.create_user(self.user2_data)

        self.authenticate_user(self.user1_data)
        self.authenticate_user(self.user2_data)

        self.create_post(self.user1_data, "post 1")
        self.create_post(self.user2_data, "post 2")

        user1_like_post1_response = self.like_post(self.user1_data, 1)
        user1_like_post1_response_data = json.loads(
            user1_like_post1_response.content
        )
        self.assertEqual(user1_like_post1_response.status_code, 200)
        self.assertIn(1, user1_like_post1_response_data["liked_posts"])

        user1_like_post2_response = self.like_post(self.user1_data, 2)
        user1_like_post2_response_data = json.loads(
            user1_like_post2_response.content
        )
        self.assertEqual(user1_like_post2_response.status_code, 200)
        self.assertIn(2, user1_like_post2_response_data["liked_posts"])

        user2_like_post1_response = self.like_post(self.user2_data, 1)
        user2_like_post1_response_data = json.loads(
            user2_like_post1_response.content
        )
        self.assertEqual(user2_like_post1_response.status_code, 200)
        self.assertIn(1, user2_like_post1_response_data["liked_posts"])

        user2_like_post2_response = self.like_post(self.user2_data, 2)
        user2_like_post2_response_data = json.loads(
            user2_like_post2_response.content
        )
        self.assertEqual(user2_like_post2_response.status_code, 200)
        self.assertIn(2, user2_like_post2_response_data["liked_posts"])
