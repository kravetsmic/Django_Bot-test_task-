from models import User
import random
import logging


class Engine:
    @staticmethod
    def log_users_in(users: list):
        logging.info("Authorizing users...")
        for user in users:
            user.login()
        logging.info("Users authorized")

    @staticmethod
    def delete_users(users: list):
        logging.info("Deleting users...")
        for user in users:
            user.delete_self()
        logging.info("Users deleted")

    def __init__(
        self,
        number_of_users: int,
        max_posts_per_user: int,
        max_likes_per_user: int,
    ):
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user

    def create_users(self, users: list):
        logging.info("Creating users...")
        for i in range(self.number_of_users):
            user_data = {
                "username": f"user{i}",
                "first_name": f"First name #{i}",
                "last_name": f"Last name #{i}",
                "email": f"email#{i}@gmail.com",
                "password": f"password#{i}",
            }
            user = User(**user_data)
            users.append(user)
        logging.info("Users created")

    def create_posts(self, users: list, posts: list):
        logging.info("Creating posts...")
        for user in users:
            posts_amount = random.randint(1, self.max_posts_per_user)
            for i in range(posts_amount):
                post = user.create_post(f"{user.username}'s post text #{i}")
                posts.append(post)
        logging.info("Posts created")

    def like_posts(self, users: list, posts: list):
        logging.info("Liking posts...")
        users.sort(key=lambda user: len(user.posts))
        all_possible_to_like_posts = set(posts)

        for liking_user in users:
            if len(all_possible_to_like_posts) == 0:
                break

            possible_to_like_posts_for_liking_user = (
                all_possible_to_like_posts.difference(set(liking_user.posts))
            )
            likes_counter = 0

            while (
                likes_counter <= self.max_likes_per_user
                and len(possible_to_like_posts_for_liking_user) != 0
            ):
                post_to_like = random.choice(
                    tuple(possible_to_like_posts_for_liking_user)
                )
                liking_user.like_post(post_to_like)

                if post_to_like.author.are_all_posts_liked():
                    possible_to_like_posts_for_liking_user.difference_update(
                        set(post_to_like.author.posts)
                    )
                    all_possible_to_like_posts.difference_update(
                        set(post_to_like.author.posts)
                    )
                else:
                    possible_to_like_posts_for_liking_user.difference_update(
                        {post_to_like}
                    )

                likes_counter += 1

        logging.info("Posts liked")
