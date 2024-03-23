from fastapi import APIRouter, HTTPException
import psycopg2
from datetime import timezone
from dbs_assignment.database_url import DATABASE_URL


router = APIRouter()

# Creates a new database connection based on the provided URL
conn = psycopg2.connect(DATABASE_URL)


# Function to retrieve users who commented on a specific post
@router.get("/v2/users/{user_id}/friends", response_model=dict)
async def get_users_friends(user_id: int):
    try:
        cur = conn.cursor() # is used to execute SQL queries on the database.

        sql_query = """
            (SELECT u.* FROM users u
            JOIN comments c ON u.id = c.userid
            WHERE c.postid IN (
                SELECT postid FROM comments WHERE userid = %s
                UNION
                SELECT id FROM posts WHERE owneruserid = %s
            )
            ORDER BY u.creationdate ASC)
        """

        cur.execute(sql_query, (user_id, user_id)) # executes the SQL query, passing the post_id as a parameter to the query.

        rows = cur.fetchall() # fetches all the rows returned by the query

        friends_json = []
        for row in rows:
            friend = {
                "id": row[0],
                "reputation": row[1],
                "creationdate": row[2].astimezone(timezone.utc).isoformat(),
                "displayname": row[3],
                "lastaccessdate": row[4].astimezone(timezone.utc).isoformat(),
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

        cur.close()
        return {"items": friends_json}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Define a function to retrieve the user's badge history
@router.get("/v3/users/{user_id}/badge_history", response_model=dict)
async def get_user_badge_history(user_id: int):
    try:
        cur = conn.cursor()
        sql_query = """
        (
        SELECT id, title, type, date,
               CASE WHEN type = 'post' THEN ROW_NUMBER() OVER (ORDER BY date) / 2 + 1
                    WHEN prev_type = 'post' THEN ROW_NUMBER() OVER (ORDER BY date) / 2
               END AS position
        FROM
            (SELECT *,
                    LAG(type) OVER (ORDER BY date) AS prev_type,
                    LEAD(type) OVER (ORDER BY date) AS next_type
            FROM (
                    (SELECT DISTINCT posts.id,
                            posts.title,
                            'post' AS type,
                            posts.creationdate AS date
                    FROM posts
                    JOIN users ON posts.owneruserid = users.id
                    WHERE users.id = 120)
                    UNION ALL
                    (SELECT DISTINCT badges.id,
                            badges.name,
                            'badge' AS type,
                            badges.date AS date
                    FROM badges
                    WHERE badges.userid = 120)
                    ORDER BY date) AS general) AS ordered
        WHERE (type = 'post' AND next_type = 'badge') OR (type = 'badge' AND prev_type = 'post')
        )
        """

        cur.execute(sql_query, user_id)
        rows = cur.fetchall()
        badge_history_json = []
        for row in rows:
            json = {
                "id": row[0],
                "title": row[1],
                "type": row[2],
                "created_at": row[3].astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00',
                "position": row[4]
            }
            badge_history_json.append(json)
        cur.close()
        return {"items": badge_history_json}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
