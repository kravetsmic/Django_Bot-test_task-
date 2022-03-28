import logging

from storage import Storage
from engine import Engine


class Bot:
    def __init__(
        self,
        number_of_users: int,
        max_posts_per_user: int,
        max_likes_per_user: int,
    ):
        logging.info("Initializing Bot...")
        self._engine = Engine(
            number_of_users, max_posts_per_user, max_likes_per_user
        )
        self._storage = Storage()
        logging.info("Bot initialized")

    def run(self):
        self._engine.create_users(self._storage.users)
        self._engine.log_users_in(self._storage.users)
        self._engine.create_posts(self._storage.users, self._storage.posts)
        self._engine.like_posts(self._storage.users, self._storage.posts)
        self._engine.delete_users(self._storage.users)


if __name__ == "__main__":
    logging.basicConfig(
        filename="bot.log",
        filemode="w",
        level=logging.INFO,
        format="[%(asctime)s]:%(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console = logging.StreamHandler()
    console_formatter = logging.Formatter(
        fmt="[%(asctime)s]:%(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console.setLevel(logging.INFO)
    console.setFormatter(console_formatter)
    logging.getLogger().addHandler(console)

    logging.info("Bot test started")
    bot_configs = {}
    with open("bot_configs.txt", "r") as configs_file:
        for line in configs_file:
            key, value = line.split("=")
            value = int(value)
            bot_configs[key] = value
    bot = Bot(**bot_configs)
    bot.run()
    logging.info("Bot test finished")
