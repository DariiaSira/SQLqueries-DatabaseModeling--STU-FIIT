from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2
import json
from dbs_assignment.database_url import DATABASE_URL


router = APIRouter()

# Creates a new database connection based on the provided URL
conn = psycopg2.connect(DATABASE_URL)


# Define a function to retrieve users who commented on a specific post
@router.get("/v2/users/{user_id}/friends", response_model=List[dict])
async def get_users_friends(user_id: int):
    try:
        cur = conn.cursor() # is used to execute SQL queries on the database.

        print(user_id)
        sql_query = """
            SELECT u.* FROM users u
            JOIN comments c ON u.id = c.userid
            WHERE c.postid IN (
                SELECT postid FROM comments WHERE userid = %s
                UNION
                SELECT id FROM posts WHERE owneruserid = %s
            )
            ORDER BY u.creationdate ASC
        """

        cur.execute(sql_query, (user_id, user_id)) # executes the SQL query, passing the post_id as a parameter to the query.

        rows = cur.fetchall() # fetches all the rows returned by the query

        # Convert the fetched data to JSON format
        friends_json = []
        for row in rows:
            friend = {
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
            friends_json.append(friend)

        # Close communication with the PostgreSQL database
        cur.close()

        # Return the JSON response
        return friends_json

    except Exception as e:
        # Handle exceptions, e.g., database connection error
        raise HTTPException(status_code=500, detail=str(e))
