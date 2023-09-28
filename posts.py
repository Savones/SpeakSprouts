from sqlalchemy.sql import text
from db import db

def get_post_info(id):
    sql = text("SELECT cp.*, u.username FROM community_posts cp JOIN users u ON cp.author_id = u.id WHERE cp.id = :id")
    post_info = db.session.execute(sql, {"id": id}).fetchone()

    post = {}
    post["id"] = post_info[0]
    post["title"] = post_info[1]
    post["content"] = post_info[2]
    post["author_username"] = post_info[5]
    post["created"] = post_info[4]

    return post

def get_posts():
    all_posts = []
    sql = text("SELECT id FROM community_posts ORDER BY id DESC")
    all_posts_ids = db.session.execute(sql).fetchall()
    for id in all_posts_ids:
        all_posts.append(get_post_info(id[0]))
    return all_posts

def add_post(author, title, content):
    sql = text("SELECT id FROM users WHERE username = :username")
    author_id = db.session.execute(sql, {"username": author}).scalar()

    sql = text("INSERT INTO community_posts (title, content, author_id) VALUES (:title, :content, :author_id)")
    db.session.execute(sql, {"title": title, "content": content, "author_id": author_id})

    db.session.commit()