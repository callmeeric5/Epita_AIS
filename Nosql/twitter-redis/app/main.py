from redis import Redis
from typing import Union

from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import bcrypt
import time

# TODO:
# [x]: Add Get user followers
# [x]TODO: Add Get user following
# [x]TODO: Add Unfollow user
# [x]TODO: Add Create a post
# [x]TODO: Add Get user posts
# [x]TODO: Add Authenticate a user
# [x]TODO: Add Find a user by username
# [x]FIXME: order of followers


redis = Redis(host="redis", port=6379, decode_responses=True)


class NewUser(BaseModel):
    username: str
    password: Union[str, None] = None


class User(BaseModel):
    id: int
    username: str
    follower_count: int
    following_count: int
    following: list[int]
    followers: list[int]


class Post(BaseModel):
    id: int
    text: str
    user_id: int
    timestamp: int


tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

# API Endpoints


## Users
### Create User
@app.post("/user/", tags=["Users"])
async def create_user(user: NewUser):
    user_id = redis.incr("seq:user")
    hashed_password = get_hashed_password(user.password.encode())
    user_info = {
        "id": user_id,
        "username": user.username,
        "password": hashed_password,
        "follower_count": 0,
        "following_count": 0,
    }
    redis.hmset(f"user:{user_id}", user_info)
    return {"success": True, user_id: user_id}


"""
The correction is to make sure everytime when using zadd(), we only add new elements rahter than updating them.
"""


@app.post("/user/follow", tags=["Users"])
async def follow_user(follower_id: int, followed_id: int):
    timestamp = int(time.time())
    if not redis.hgetall(f"user:{follower_id}"):
        return {"success": False, "message": "Follower user does not exist"}
    if not redis.hgetall(f"user:{followed_id}"):
        return {"success": False, "message": "Followed user does not exist"}
    if redis.zadd(f"followers:{followed_id}", {follower_id: timestamp}, nx=True):
        redis.hincrby(f"user:{followed_id}", "follower_count", 1)
        redis.zadd(f"following:{follower_id}", {followed_id: timestamp})
        redis.hincrby(f"user:{follower_id}", "following_count", 1)
        return {"success": True}
    else:
        return {"success": False, "message": "User is already followed"}


"""
Unfollows a user.

Args:
    follower_id (int): The ID of the user who is unfollowing.
    followed_id (int): The ID of the user who is being unfollowed.

Returns:
    dict: A dictionary indicating the success of the unfollow operation.

Raises:
    None
"""


@app.post("/user/unfollow", tags=["Users"])
async def unfollow_user(follower_id: int, followed_id: int):
    timestamp = int(time.time())
    if not redis.hgetall(f"user:{follower_id}"):
        return {"success": False, "message": "Follower user does not exist"}
    if not redis.hgetall(f"user:{followed_id}"):
        return {"success": False, "message": "Followed user does not exist"}
    if redis.zrem(f"followers:{followed_id}", follower_id) == 0:
        return {"success": False, "message": "User is not followed"}
    redis.zrem(f"following:{follower_id}", followed_id)
    redis.hincrby(f"user:{follower_id}", "following_count", -1)
    redis.hincrby(f"user:{followed_id}", "follower_count", -1)
    return {"success": True, "timestamp": timestamp}


### Get User


"""
Get user information by ID.

Args:
    id (int): The ID of the user.
    response (Response): The HTTP response object.

Returns:
    User
"""


@app.get("/user/{id}", tags=["Users"])
async def get_user(id: int, response: Response) -> User:
    # Get User from DB
    if redis.exists(f"user:{id}") == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    user_info = redis.hmget(
        f"user:{id}", ["username", "following_count", "follower_count"]
    )
    return User(
        id=id,
        username=user_info[0],
        following_count=int(user_info[1]),
        follower_count=int(user_info[2]),
        following=redis.zrange(f"following:{id}", 0, -1),
        followers=redis.zrange(f"followers:{id}", 0, -1),
    )


"""
Get user followers.

Args:
    id (int): The ID of the user.
    response (Response): The HTTP response object.
    threshold (int, optional): The number of rows returned in one page. Defaults to 4.

Returns:
    list: A list of followers of the user.

Example:
    Threshod = 2, Followers = [1,2,3]
    [
        [{
            "id": 1,
        },
        {
            "id": 2,
        }],
        [{
            "id": 3,
        }],
    ]
"""


@app.get("/user/followers/{id}", tags=["Users"])
async def get_user_followers(id: int, response: Response, threshold: int = 4) -> list:
    if not redis.exists(f"user:{id}"):
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    followers = redis.zrange(f"followers:{id}", 0, -1)
    res = [followers[i : i + threshold] for i in range(0, len(followers), threshold)]
    return res


"""
Retrieve the list of users that the specified user is following.

Args:
    id (int): The ID of the user.
    response (Response): The HTTP response object.
    threshold (int, optional): The number of rows returned in one page. Defaults to 4.

Returns:
    list: A list of followings of the user.

Example:
    Threshod = 2, Followings = [1,2,3]
    [
        [{
            "id": 1,
        },
        {
            "id": 2,
        }],
        [{
            "id": 3,
        }],
    ]
"""


@app.get("/user/following/{id}", tags=["Users"])
async def get_user_following(id: int, response: Response, threshold: int = 4) -> list:
    if not redis.exists(f"user:{id}"):
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    following = redis.zrange(f"following:{id}", 0, -1)
    res = [following[i : i + threshold] for i in range(0, len(following), threshold)]
    return res


### Authenticate a user

"""
Authenticates a user by checking if the provided password matches the stored password for the given user ID.

Args:
    user_id (int): The ID of the user to authenticate.
    password (str): The password to check against the stored password.

Returns:
    dict: A dictionary indicating the success of the authentication. If the authentication is successful, 
    the dictionary will have the following structure:
"""


@app.post("/user/authenticate", tags=["Users"])
async def authenticate_user(user_id: int, password: str):
    if not redis.exists(f"user:{user_id}"):
        return {"success": False, "message": "User does not exist"}
    user_password = redis.hget(f"user:{user_id}", "password")
    res = check_password(password.encode(), user_password.encode())

    if res == True:
        return {"success": True}
    else:
        return {"success": False, "message": "Incorrect password"}


### Get User by username

"""
Get user information by username.

Args:
    username (str): The username of the user.

Returns:
    User

Comments:
    An ugly way to get user information by username. 
    If the datasize is huge, buy yourself a cup of coffee.
"""


@app.get("/user/username/{username}", tags=["Users"])
async def get_user_by_username(username: str) -> User:
    users = []
    keys = redis.keys("user:*")
    for key in keys:
        if not key.endswith(":posts"):
            stored_username = redis.hmget(key, "username")[0]
            if stored_username == username:
                user_info = redis.hgetall(key)
                users.append(user_info)

    if not users:
        return {"success": False, "message": "User not found"}
    return users


## Posts
### Create Post

"""
Creates a new post.

Args:
    post (Post): The post object containing post details.
    user_id (int): The ID of the user creating the post.
    text (str): The text content of the post.

Returns:
    dict: A dictionary indicating the success of the post creation operation, including the post ID and user ID.
"""


@app.post("/post/", tags=["Posts"])
async def create_post(user_id: int, text: str):
    timestamp = int(time.time())
    post_id = redis.incr("seq:post")
    post_info = {
        "id": post_id,
        "text": text,
        "user_id": user_id,
        "timestamp": timestamp,
    }
    redis.hmset(f"post:{post_id}", post_info)
    redis.zadd(f"user:{user_id}:posts", {post_id: timestamp})
    return {"success": True, "post_id": post_id, "user_id": user_id}


### Get Posts

"""
Get posts for a given user.

Args:
    user_id (int): The ID of the user.
    response (Response): The HTTP response object.
    threshold (int, optional): The number of posts to return per page. Defaults to 4.

Returns:
    list: A list of posts sorted by timestamp in descending order. Each post is represented as a dictionary with the following keys:
        - "id" (int): The ID of the post.
        - "text" (str): The text content of the post.
        - "user_id" (int): The ID of the user who created the post.
        - "timestamp" (int): The timestamp of the post.

Raises:
    HTTPException: If the user does not exist.

Example:
    Threshod = 2, Post_id = [1,2,3]
    [
        [{
            "id": 1,
        },
        {
            "id": 2,
        }],
        [{
            "id": 3,
        }],
    ]

"""


@app.get("/post/", tags=["Posts"])
async def get_posts(user_id: int, response: Response, threshold: int = 4) -> list:
    if not redis.exists(f"user:{user_id}"):
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    post_ids = redis.zrevrange(f"user:{user_id}:posts", 0, -1)
    posts = []
    for post_id in post_ids:
        post_info = redis.hgetall(f"post:{post_id}")
        posts.append(post_info)
    res = [posts[i : i + threshold] for i in range(0, len(posts), threshold)]
    return res


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)
