#API reference
## Authentication
### Obtain token
+ method: POST  
+ url: http://127.0.0.1:8000/social_network/login/  
+ body: {
    "username": "",
    "password": ""
}  
+ response: {
    "token": ""
}
## Users
### Get all users
+ method: GET  
+ url: http://127.0.0.1:8000/social_network/users  
+ response: [
      {
        "id": ,
        "username": "",
        "first_name": "",
        "last_name": "",
        "email": "",
        "password": "",
        "posts": [],
        "liked_posts": [],
        "viewed_posts": []
      },
     ...
]
### Get user by id
+ method: GET  
+ url: http://127.0.0.1:8000/social_network/users/{id}  
+ response: {
        "id": ,
        "username": "",
        "first_name": "",
        "last_name": "",
        "email": "",
        "password": "",
        "posts": [],
        "liked_posts": [],
        "viewed_posts": []
      }
### Create user
+ method: POST  
+ url: http://127.0.0.1:8000/social_network/users/  
+ body: {
        "username": "",
        "first_name": "",
        "last_name": "",
        "email": "",
        "password": ""
    }  
+ response: {
        "id": ,
        "username": "",
        "first_name": "",
        "last_name": "",
        "email": "",
        "password": "",
        "posts": [],
        "liked_posts": [],
        "viewed_posts": []
      }
### Update user
+ method: PUT  
+ url: http://127.0.0.1:8000/social_network/users/{id}/  
+ header: {"Authorization": "Token "}  
+ body: {
        "first_name": "",
        "last_name": "",
        "email": "",
        "username": "" (not required),
        "password": "" (not required)
    }  
+ response: {
        "id": ,
        "username": "",
        "first_name": "",
        "last_name": "",
        "email": "",
        "password": "",
        "posts": [],
        "liked_posts": [],
        "viewed_posts": []
      }
### Delete user
+ method: DELETE  
+ url: http://127.0.0.1:8000/social_network/users/{id}  
+ header: {"Authorization": "Token "}  
+ response: {
        "id": ,
        "username": "",
        "first_name": "",
        "last_name": "",
        "email": "",
        "password": "",
        "posts": [],
        "liked_posts": [],
        "viewed_posts": []
      }
## Posts
### Get all posts
+ method: GET  
+ url: http://127.0.0.1:8000/social_network/posts  
+ response: [
    {
        "id": ,
        "publication_date": "",
        "text": "",
        "author": 1,
        "views": [],
        "likes": []
    },
    ...
]  
### Get post by id
+ method: GET  
+ url: http://127.0.0.1:8000/social_network/posts/{id}  
+ response: {
    "id": ,
    "publication_date": "",
    "text": "",
    "author": ,
    "views": [],
    "likes": []
}
### Create post
+ method: POST  
+ url: http://127.0.0.1:8000/social_network/posts/  
+ header: {"Authorization": "Token "}  
+ body: {
        "text": ""
    }  
+ response: {
    "id": ,
    "publication_date": "",
    "text": "",
    "author": ,
    "views": [],
    "likes": []
}
      
### Update post
+ method: PUT  
+ url: http://127.0.0.1:8000/social_network/posts/{id}/ 
+ header: {"Authorization": "Token "}  
+ body: {
        "text": ""
    }  
+ response: {
    "id": ,
    "publication_date": "",
    "text": "",
    "author": ,
    "views": [],
    "likes": []
}
### Delete post
+ method: DELETE  
+ url: http://127.0.0.1:8000/social_network/posts/{id}  
+ header: {"Authorization": "Token "}  
+ response: {
    "id": ,
    "publication_date": "",
    "text": "",
    "author": ,
    "views": [],
    "likes": []
}
### View post
+ method: PATCH  
+ url: http://127.0.0.1:8000/social_network/users/view_post/  
+ header: {"Authorization": "Token "}  
+ body: {
    "post_id": 
}  
+ response: {
    "username": "",
    "viewed_posts": [], 
    "success": "true"
}
### Like post
+ method: PATCH  
+ url: http://127.0.0.1:8000/social_network/users/like_post/  
+ header: {"Authorization": "Token "}  
+ body: {
    "post_id": 
}  
+ response: {
    "username": "",
    "liked_posts": [], 
    "success": "true"
}
### Dislike post
+ method: PATCH  
+ url: http://127.0.0.1:8000/social_network/users/dislike_post/  
+ header: {"Authorization": "Token "}  
+ body: {
    "post_id": 
}  
+ response: {
    "username": "",
    "liked_posts": [], 
    "success": "true"
}