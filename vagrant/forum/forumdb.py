#
# Database access functions for the web forum.
# 

import time, psycopg2, bleach

## Database connection

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.
    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    QUERY ="select time, content from posts order by time DESC"
    c.execute(QUERY)
    posts = ({'content': str(bleach.clean(row[1])), 'time': str(row[0])}
             for row in c.fetchall()))
    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.
    Args:
      content: The text content of the new post.
    '''
    #t = time.strftime('%c', time.localtime())
    #DB.append((t, content))
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    content = bleach.clean(content, strip = True)
    c.execute("INSERT INTO posts (content) VALUES (%s)",  (content,))
    DB.commit()
    DB.close()