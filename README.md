# Test task
## Social network
This is the simple social network where users can create, view, like and dislike posts
### Django models used
+ User(standard django model)
+ Post(text, author, publication date, views, likes)
### What users can do
+ Create account
+ Edit account
+ Delete account
+ Log in
+ Create post
+ Edit post
+ Delete post
+ View post
+ Like post
+ Dislike post(remove like)

To know how to send these request open `API_docs.md` file
### Technologies used
+ Django
+ Django Rest Framework
+ Django's build in DB sqlite3
### How to install
+ Download all requirements with `pip install -r requirements.txt`
+ Perform migrations to DB with `python manage.py runserver migrate` (In Backend folder)
### How to run
+ Run command `python manage.py runserver` in Backend folder
### How to test
+ Run command `python manage.py test` in Backend folder
## Bot
This is bot which, with the help of API requests, perform several manipulations with users and posts
### Work algorithm
+ Read `number_of_users`, `max_posts_per_user` and `max_likes_per_user` from `bot_configs`
+ Create `number_of_users` users
+ Log in every user
+ Create from 1 to `max_posts_per_user` posts for every user
+ Like posts according to the next principles:
  1. The next user who likes a post is the user with the most posts created by him 
  and this user does not reach the maximum number of likes (`max_likes_per_user`).
  2. The user likes posts until he gets the maximum number of likes.
  3. The user likes random posts of users who have at least one post without likes.
  4. If there are no posts with 0 likes at all, the bot ends its work
  5. Users cannot like their own posts
  6. Posts can be liked multiple times, but the user can like a particular post only once
+ Delete all created users
### How to run
+ Run Django(you can specify not localhost in .env file + you need to add it to ALLOWED_HOSTS in settings.py )
+ Just run bot.py file with `python3 bot.py` in bot directory
### Logs
Every action is logged to console and `bot.log` file
### Technologies used:
+ Django, DRF
+ requests module to send API requests
## Docker
### How to install
+ Run `docker-compose build` in project directory
### How to run
+ Run `docker-compose up backend` in project directory to run backend
+ In another terminal run `docker-compose up bot` in project directory to run bot
### How to test
+ Run `docker-compose up test` in project directory