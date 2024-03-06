from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2
import json
from datetime import datetime, timedelta
from dbs_assignment.database_url import DATABASE_URL


router = APIRouter()

# Creates a new database connection based on the provided URL.
conn = psycopg2.connect(DATABASE_URL)


# Define a function to retrieve users who commented on a specific post
@router.get("/v2/posts/{post_id}/users", response_model=List[dict])
async def get_post_users(post_id: int):
    try:
        # Create a cursor object using the cursor() method
        cur = conn.cursor() # is used to execute SQL queries on the database.

        # Define the SQL query to retrieve users who commented on the specified post
        sql_query = """
            SELECT u.* FROM users u
            JOIN comments c ON u.id = c.userid
            WHERE c.postid = %s
            ORDER BY c.creationdate DESC
        """

        # Execute the SQL query
        cur.execute(sql_query, (post_id,)) # executes the SQL query, passing the post_id as a parameter to the query.

        # Fetch all the rows from the query result
        rows = cur.fetchall() # fetches all the rows returned by the query

        # Convert the fetched data to JSON format
        users_json = []
        for row in rows:
            user = {
                "id": row[0],
                "reputation": row[1],
                "creationdate": row[2].isoformat(),
                "displayname": row[3],
                "lastaccessdate": row[4].isoformat(),
                "websiteurl": row[5],
                "location": row[6],
                "aboutme": row[7],
                "views": row[8],
                "upvotes": row[9],
                "downvotes": row[10],
                "profileimageurl": row[11],
                "age": row[12],
                "accountid": row[13]
            }
            users_json.append(user)

        # Close communication with the PostgreSQL database
        cur.close()

        # Return the JSON response
        return users_json

    except Exception as e:
        # Handle exceptions, e.g., database connection error
        raise HTTPException(status_code=500, detail=str(e))


# Define a function to retrieve the most recent resolved posts with a duration less than or equal to the specified duration
@router.get("/v2/posts/", response_model=dict)
async def get_recent_resolved_posts(duration: int, limit: int):
    try:
        # Calculate the datetime duration ago from the current time
        duration_ago = datetime.now() - timedelta(minutes=duration)
        print(duration_ago, datetime.now(), timedelta(minutes=duration))

        # Create a cursor object using the cursor() method
        cur = conn.cursor()

        # Define the SQL query to retrieve recent resolved posts with a duration less than or equal to the specified duration
        sql_query = """
            SELECT id, creationdate, viewcount, lasteditdate, lastactivitydate, title, closeddate,
                ROUND(EXTRACT(EPOCH FROM (closeddate - creationdate))/60, 2) AS duration
                FROM posts
            WHERE closeddate IS NOT NULL
            AND CAST(ROUND(EXTRACT(EPOCH FROM (closeddate - creationdate))/60, 2) AS numeric) <= %s
            ORDER BY closeddate DESC
            LIMIT %s
        """

        # Execute the SQL query
        cur.execute(sql_query, (duration, limit))

        # Fetch all the rows from the query result
        rows = cur.fetchall()

        # Convert the fetched data to JSON format
        posts_json = []
        for row in rows:
            post = {
                "id": row[0],
                "creationdate": row[1].isoformat(),
                "viewcount": row[2],
                "lasteditdate": row[3].isoformat() if row[3] else None,
                "lastactivitydate": row[4].isoformat(),
                "title": row[5],
                "closeddate": row[6].isoformat(),
                "duration": float(row[7])
            }
            posts_json.append(post)

        # Close communication with the PostgreSQL database
        cur.close()

        # Return the JSON response
        return {"items": posts_json}

    except Exception as e:
        # Handle exceptions, e.g., database connection error
        raise HTTPException(status_code=500, detail=str(e))


# Define a function to retrieve posts based on query parameters
@router.get("/v2/posts", response_model=dict)
async def get_posts(limit: int, query: str):
    try:
        # Create a cursor object using the cursor() method
        cur = conn.cursor()

        # Define the SQL query to retrieve posts sorted by creation date and filtered by the query string
        sql_query = """
            SELECT p.id, p.creationdate, p.viewcount, p.lasteditdate, p.lastactivitydate,
                p.title, p.body, p.answercount, p.closeddate,
                ARRAY_AGG(t.tagname) AS tags
                FROM posts p
            FULL JOIN post_tags pt ON p.id = pt.post_id
            FULL JOIN tags t ON pt.tag_id = t.id
            WHERE LOWER(p.title) LIKE LOWER(%s) OR LOWER(p.body) LIKE LOWER(%s)
                AND t.tagname = %s
            GROUP BY
                p.id, p.creationdate, p.viewcount, p.lasteditdate, p.lastactivitydate,
                p.title, p.body, p.answercount, p.closeddate
            ORDER BY p.creationdate DESC
            LIMIT %s
        """

        # Execute the SQL query
        cur.execute(sql_query, (f"%{query}%", f"%{query}%", query, limit))

        # Fetch all the rows from the query result
        rows = cur.fetchall()

        # Convert the fetched data to JSON format
        posts_json = []
        for row in rows:
            post = {
                "id": row[0],
                "creationdate": row[1].isoformat(),
                "viewcount": row[2],
                "lasteditdate": row[3].isoformat() if row[3] else None,
                "lastactivitydate": row[4].isoformat(),
                "title": row[5],
                "body": row[6],
                "answercount": row[7],
                "closeddate": row[8].isoformat() if row[8] else None,
                "tags": row[9]
            }
            posts_json.append(post)

        # Close communication with the PostgreSQL database
        cur.close()

        # Return the JSON response
        return {"items": posts_json}

    except Exception as e:
        # Handle exceptions, e.g., database connection error
        raise HTTPException(status_code=500, detail=str(e))


