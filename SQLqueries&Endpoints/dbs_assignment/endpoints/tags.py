from fastapi import APIRouter, HTTPException
import psycopg2
from datetime import timezone
from dbs_assignment.database_url import DATABASE_URL


router = APIRouter()

# Creates a new database connection based on the provided URL
conn = psycopg2.connect(DATABASE_URL)


# Function to retrieve users who commented on a specific post
@router.get("/v2/tags/{tagname}/stats", response_model=dict)
async def get_tag_stats(tagname: str):
    try:
        cur = conn.cursor() # is used to execute SQL queries on the database.

        sql_query = """
            (SELECT DISTINCT EXTRACT(dow FROM p.creationdate) AS day_of_week,
                COUNT(DISTINCT p.id) AS total_posts,
                SUM(CASE WHEN t.tagname = %s THEN 1 ELSE 0 END) AS tag_posts
                FROM posts p
            JOIN post_tags pt ON p.id = pt.post_id
            JOIN tags t ON pt.tag_id = t.id
            GROUP BY day_of_week
            ORDER BY day_of_week)
        """

        cur.execute(sql_query, (tagname,)) # Executes the SQL query, passing the post_id as a parameter to the query.

        rows = cur.fetchall() # Fetches all the rows returned by the query

        # Calculate percentage representation for each day of the week
        tag_stats = {}
        for row in rows:
            day_of_week = int(row[0])
            total_posts = row[1]
            tag_posts = row[2]
            if total_posts == 0:
                percentage = 0.0
            else:
                percentage = round((tag_posts / total_posts) * 100, 2)
            tag_stats[day_of_week] = percentage

        cur.close()

        result = {
            "monday": tag_stats.get(1, 0.0),
            "tuesday": tag_stats.get(2, 0.0),
            "wednesday": tag_stats.get(3, 0.0),
            "thursday": tag_stats.get(4, 0.0),
            "friday": tag_stats.get(5, 0.0),
            "saturday": tag_stats.get(6, 0.0),
            "sunday": tag_stats.get(0, 0.0)
        }
        return {"result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/v3/tags/{tagname}/comments/", response_model=dict)
async def get_tags_count(tagname: str, count: int = None):
    try:
        cur = conn.cursor()
        sql_query = """
                    (
                    SELECT formatted.postid,
                           formatted.title,
                           formatted.displayname,
                           formatted.text,
                           formatted.post_created_at,
                           formatted.creationdate,
                           CONCAT(
                                CASE WHEN EXTRACT(days FROM time_difference) > 0 THEN
                                        CASE
                                            WHEN EXTRACT(days FROM time_difference) = 1 THEN CONCAT(EXTRACT(days FROM time_difference), ' day ')
                                            ELSE CONCAT(EXTRACT(days FROM time_difference), ' days ')
                                        END
                                    ELSE ''
                                END,
                                TO_CHAR(time_difference, 'HH24:MI:SS.US')
                            ) AS formatted_time_difference,
                           CONCAT(
                                CASE
                                    WHEN EXTRACT(days FROM avg) > 0 THEN
                                        CASE
                                            WHEN EXTRACT(days FROM avg) = 1 THEN CONCAT(EXTRACT(days FROM avg), ' day ')
                                            ELSE CONCAT(EXTRACT(days FROM avg), ' days ')
                                        END
                                    ELSE ''
                                END,
                                TO_CHAR(avg, 'HH24:MI:SS.US')
                            ) AS formatted_avg

                    FROM (SELECT difference_table.postid,
                                 difference_table.title,
                                 difference_table.displayname,
                                 difference_table.text,
                                 difference_table.post_created_at,
                                 difference_table.creationdate,
                                 time_difference,
                                 AVG(time_difference) OVER (PARTITION BY difference_table.postid ORDER BY difference_table.creationdate) AS avg
                        FROM
                            (SELECT comments.postid,
                                    posts.title,
                                    users.displayname,
                                    comments.text,
                                    posts.creationdate AS post_created_at,
                                    comments.creationdate,
                                    (comments.creationdate - LAG(comments.creationdate, 1, posts.creationdate) OVER (PARTITION BY comments.postid ORDER BY comments.creationdate)) AS time_difference
                                FROM comments
                                JOIN posts ON comments.postid = posts.id
                                FULL JOIN users ON comments.userid = users.id
                                JOIN post_tags ON comments.postid = post_tags.post_id
                                JOIN tags ON post_tags.tag_id = tags.id
                                WHERE posts.parentid IS NULL AND tags.tagname = 'networking'
                                ORDER BY comments.postid, comments.creationdate) AS difference_table

                        JOIN (SELECT postid, COUNT(*) AS total_comments
                                FROM comments
                                GROUP BY postid
                                HAVING COUNT(*) > 40) sub_table_limited ON difference_table.postid = sub_table_limited.postid) AS formatted
                    )
                    """
        cur.execute(sql_query, (tagname, count))
        rows = cur.fetchall()
        tags_comments = []
        for row in rows:
            json = {
                "post_id": row[0],
                "title": row[1],
                "displayname": row[2],
                "text": row[3],
                "post_created_at": row[4].astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00',
                "created_at": row[5].astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00',
                "diff": row[6][:10] + row[6][10:].rstrip("0"),
                "avg": row[7][:10] + row[7][10:].rstrip("0"),
            }
            tags_comments.append(json)

        cur.close()
        return {"items": tags_comments}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/v3/tags/{tagname}/comments/{position}", response_model=dict)
async def get_posts_comment(tagname: str, position: int = None, limit: int = None):
    try:
        cur = conn.cursor()
        sql_query = """
                    (
                    SELECT * FROM
                                 (SELECT comments.id,
                                         users.displayname,
                                         posts.body,
                                         comments.text,
                                         comments.score,
                                         ROW_NUMBER() OVER (PARTITION BY comments.postid ORDER BY comments.creationdate) AS position
                                    FROM comments
                                    JOIN posts ON comments.postid = posts.id
                                    FULL JOIN users ON comments.userid = users.id
                                    JOIN post_tags ON comments.postid = post_tags.post_id
                                    JOIN tags ON post_tags.tag_id = tags.id
                                    WHERE posts.parentid IS NULL AND tags.tagname = %s
                                    ORDER BY posts.creationdate) AS ordered_table
                    WHERE position = %s
                    LIMIT %s
                    )
                    """

        cur.execute(sql_query, (tagname, position, limit))
        rows = cur.fetchall()
        tags_comments = []
        for row in rows:
            json = {
                "id": row[0],
                "displayname": row[1],
                "body": row[2],
                "text": row[3],
                "score": row[4],
                "position": row[5]
            }
            tags_comments.append(json)

        cur.close()
        return {"items": tags_comments}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


