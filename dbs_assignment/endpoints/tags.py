from fastapi import APIRouter, HTTPException
import psycopg2
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
        SELECT DISTINCT EXTRACT(dow FROM p.creationdate) AS day_of_week,
            COUNT(DISTINCT p.id) AS total_posts,
            SUM(CASE WHEN t.tagname = %s THEN 1 ELSE 0 END) AS tag_posts
            FROM posts p
        JOIN post_tags pt ON p.id = pt.post_id
        JOIN tags t ON pt.tag_id = t.id
        GROUP BY day_of_week
        ORDER BY day_of_week
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

