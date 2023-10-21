from sqlalchemy.sql import text
from db import db
from services.mod import get_id


def get_post_info(post_id):
    sql = text("""SELECT cp.*, u.username 
               FROM community_posts cp 
               JOIN users u ON cp.author_id = u.id 
               WHERE cp.id = :id""")
    post_info = db.session.execute(sql, {"id": post_id}).fetchone()

    return {
        "id": post_info[0],
        "title": post_info[1],
        "content": post_info[2],
        "created": post_info[4],
        "author_username": post_info[5]
    }


def get_posts(author=None):
    all_posts = []
    if not author:
        sql = text("SELECT id FROM community_posts ORDER BY created_at DESC")
        all_posts_ids = db.session.execute(sql).fetchall()
    else:
        sql = text(
            "SELECT id FROM community_posts WHERE author_id = :author_id ORDER BY created_at DESC")
        all_posts_ids = db.session.execute(
            sql, {"author_id": get_id(author)}).fetchall()
    for id in all_posts_ids:
        all_posts.append(get_post_info(id[0]))
    return all_posts


def add_post(author, title, content):
    sql = text(
        """
        INSERT INTO community_posts (title, content, author_id)
        VALUES (:title, :content, :author_id)
        """
    )
    db.session.execute(
        sql, {
            "title": title,
            "content": content,
            "author_id": get_id(author)
        }
    )
    db.session.commit()


def add_comment(post_id, author, content):
    sql = text(
        """
        INSERT INTO post_comments (post_id, author_id, content)
        VALUES (:post_id, :author_id, :content)
        """
    )
    db.session.execute(
        sql, {
            "post_id": post_id,
            "content": content,
            "author_id": get_id(author)
        }
    )
    db.session.commit()


def get_comments(post_id):
    all_comments = []
    sql = text(
        "SELECT id FROM post_comments WHERE post_id = :post_id ORDER BY timestamp DESC")
    all_comment_ids = db.session.execute(sql, {"post_id": post_id}).fetchall()
    for comment_id in all_comment_ids:
        all_comments.append(get_comment_info(comment_id[0]))
    return all_comments


def get_comment_info(comment_id):
    sql = text(
        """
        SELECT pc.id, pc.post_id, pc.timestamp, pc.content, u.username
        FROM post_comments pc JOIN users u ON pc.author_id = u.id
        WHERE pc.id = :id
        """
    )
    comment_info = db.session.execute(sql, {"id": comment_id}).fetchone()
    return {
        "id": comment_info[0],
        "post_id": comment_info[1],
        "created": comment_info[2],
        "content": comment_info[3],
        "author_username": comment_info[4]
    }
