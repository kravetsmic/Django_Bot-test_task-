import json
import os
from datetime import datetime
import logging
import requests
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("DJANGO_HOST")


class User:
    def __init__(
        self,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
    ):
        request_data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        }
        response = requests.post(
            f"{HOST}:8000/social_network/users/", json=request_data
        )

        if response.status_code == 201:
            response_data = json.loads(response.text)
            self.id = response_data["id"]
            self.username = response_data["username"]
            self.first_name = response_data["first_name"]
            self.last_name = response_data["last_name"]
            self.email = response_data["email"]
            self.password = password
            self.posts = []
            self.access_token = None

            logging.info(f"User {self.username} created: {str(self)}")

        else:
            raise requests.exceptions.HTTPError(
                response.status_code, response.reason, response.text
            )

    def __str__(self):
        return (
            f"Id: {self.id}; "
            f"Username: {self.username}; "
            f"First Name: {self.first_name}; "
            f"Last Name: {self.last_name}; "
            f"Email: {self.email}; "
            f"Password: {self.password}; "
            f"Posts: {[post.id for post in self.posts]}; "
            f"Access token: {self.access_token}"
        )

    def login(self):
        request_data = {"username": self.username, "password": self.password}
        response = requests.post(
            f"{HOST}:8000/social_network/login/", json=request_data
        )

        if response.status_code == 200:
            self.access_token = json.loads(response.text)["token"]
            logging.info(
                f"User {self.username} authorized. access token: {self.access_token}"
            )

        else:
            raise requests.exceptions.HTTPError(
                response.status_code, response.reason, response.text
            )

    def create_post(self, post_text: str):
        request_data = {"text": post_text}
        response = requests.post(
            f"{HOST}:8000/social_network/posts/",
            json=request_data,
            headers={"Authorization": f"Token {self.access_token}"},
        )

        if response.status_code == 201:
            response_data = json.loads(response.text)
            post = Post(
                id=response_data["id"],
                author=self,
                text=response_data["text"],
                publication_date=response_data["publication_date"],
                likes=response_data["likes"],
            )
            self.posts.append(post)

            logging.info(f"{self.username} creates post: {str(post)}")
            return post

        else:
            raise requests.exceptions.HTTPError(
                response.status_code, response.reason, response.text
            )

    def like_post(self, post):
        request_data = {"post_id": post.id}
        response = requests.patch(
            f"{HOST}:8000/social_network/users/like_post/",
            json=request_data,
            headers={"Authorization": f"Token {self.access_token}"},
        )

        if response.status_code == 200:
            post.likes.append(self)
            logging.info(
                f"{self.username}(id {self.id}) likes post with id {post.id} and author id {post.author.id}"
            )

        else:
            raise requests.exceptions.HTTPError(
                response.status_code, response.reason, response.text
            )

    def delete_self(self):
        response = requests.delete(
            f"{HOST}:8000/social_network/users/{self.id}",
            headers={"Authorization": f"Token {self.access_token}"},
        )

        if response.status_code in (204, 301):
            logging.info(f"User {self.username} deleted")

    def are_all_posts_liked(self):
        return all([post.is_liked() for post in self.posts])


class Post:
    def __init__(
        self,
        id: int,
        author: User,
        text: str,
        publication_date: str,
        likes: list,
    ):
        self.id = id
        self.author = author
        self.text = text
        self.publication_date = datetime.strptime(
            publication_date, "%Y-%m-%d %H:%M:%S"
        )
        self.likes = likes

    def __str__(self):
        return (
            f"Id: {self.id}; "
            f"Author id: {self.author.id}; "
            f"Text: {self.text}; "
            f"Publication date: {self.publication_date}; "
            f"Likes: {self.likes}"
        )

    def is_liked(self):
        return len(self.likes) != 0
