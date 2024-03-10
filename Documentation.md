Sira Dariia -- 119436

#### **ASSIGNMENT 2 DOCUMENTATION**

---

**Endpoint 1**

**GET /v2/posts/:post id/users**

Return a list of all the users (users) of the post with ID: post id, and sort them according to based on when the comment was made, starting with the newest and ending with the oldest.

**SQL Request:**
```
    SELECT u.*
    FROM users u
    JOIN comments c ON u.id = c.userid
    WHERE c.postid = {post_id}
    ORDER BY c.creationdate DESC
```
**HTTP end-point call example**
```
{
  "items": [
    {
      "id": 1866388,
      "reputation": 1,
      "creationdate": "2023-11-30T23:05:24.337000+00:00",
      "displayname": "TomR.",
      "lastaccessdate": "2023-12-03T05:18:19.607000+00:00",
      "websiteurl": null,
      "location": null,
      "aboutme": null,
      "views": 1,
      "upvotes": 0,
      "downvotes": 0,
      "profileimageurl": null,
      "age": null,
      "accountid": 30035903
    }
  ]
}
```
This SQL query returns a list of all users who have commented on a particular post with the specified post id. The user records are returned in order, starting with the newest comments and ending with the oldest.

1. First selected the data from the users table.
2. Then merged the users and comments tables by user id.
3. After, filtered only those comments that are related to the post with the specified id (_postid = {post_id}_).
4. Arranged the results by _creationdate_ in descending order (DESC) so that the newest comments are the first in the list.


**Endpoint 2**

**GET /v2/users/:user id/friends**

Produce a list of discussants for the user_id, containing the users who have commented on the posts,  that the user has posted or commented on. Arrange the users according to the date of their registration, starting with those who registered first.

**SQL Request:**
```
SELECT u.* FROM users u
JOIN comments c ON u.id = c.userid
    WHERE c.postid IN (
        SELECT postid FROM comments WHERE userid = {user_id}
        UNION
        SELECT id FROM posts WHERE owneruserid = {user_id}
    )
ORDER BY u.creationdate ASC
```
**HTTP end-point call example**
```
{
  "items": [
    {
      "id": 482362,
      "reputation": 10581,
      "creationdate": "2015-08-11T15:42:36.267000+00:00",
      "displayname": "DrZoo",
      "lastaccessdate": "2023-12-03T05:41:11.750000+00:00",
      "websiteurl": null,
      "location": null,
      "aboutme": null,
      "views": 1442,
      "upvotes": 555,
      "downvotes": 46,
      "profileimageurl": null,
      "age": null,
      "accountid": 2968677
    },
    {
      "id": 1076348,
      "reputation": 1,
      "creationdate": "2019-08-15T14:00:28.473000+00:00",
      "displayname": "Richard",
      "lastaccessdate": "2019-09-10T14:57:48.527000+00:00",
      "websiteurl": null,
      "location": null,
      "aboutme": null,
      "views": 0,
      "upvotes": 0,
      "downvotes": 0,
      "profileimageurl": null,
      "age": null,
      "accountid": 16514661
    }
  ]
}
```

This SQL query returns a list of users who have commented on posts published or commented on by the specified user, and sorts them by their registration date, starting with those who registered first.

1. First, I selected the data from the users table and merge the users and comments tables by user id to get information about the users who have left comments.
2. After I filtered comments related to posts that have been published or commented by the specified user. To do this, firstly select all the _postid_ from the comments where the specified _user_id_ was mentioned, and then add to this list the _postid_ from the posts table where _owneruserid_ is equal to the specified _user_id_.
3. Organized the results by _creationdate_ in ascending order (ASC) so that users who registered earlier are first in the list.

**Endpoint 3**

**GET /v2/tags/:tagname/stats**

Determine the percentage of posts with a particular tag in the total number of posts published on each day of the week (e.g. Monday, Tuesday), for each day of the week. The results of the show on a scale from 0-100 and round to two decimal places.

**SQL Request:**
```
SELECT DISTINCT EXTRACT(dow FROM p.creationdate) AS day_of_week,
    COUNT(DISTINCT p.id) AS total_posts,
    SUM(CASE WHEN t.tagname = {tagname} THEN 1 ELSE 0 END) AS tag_posts
FROM posts p
JOIN post_tags pt ON p.id = pt.post_id
JOIN tags t ON pt.tag_id = t.id
GROUP BY day_of_week
ORDER BY day_of_week
```
**HTTP end-point call example**
```
{
  "result": {
    "monday": 11.53,
    "tuesday": 11.62,
    "wednesday": 11.52,
    "thursday": 11.35,
    "friday": 11.68,
    "saturday": 12.04,
    "sunday": 11.82
  }
}
```
This SQL query determines the percentage of posts with a particular tag relative to the total number of posts.

1. Selected unique days of the week by extracting them from the post creation date.
2. The EXTRACT function in `EXTRACT(dow FROM p.creationdate)` is used to extract the day of the week from the post creation date (creationdate). The result will be represented as a number where 0 corresponds to Sunday, 1 corresponds to Monday, 2 corresponds to Tuesday, etc.
3. Counted the total number of unique posts published on each day of the week `COUNT(DISTINCT p.id)`.
4. On the `SUM(CASE WHEN t.tagname = {tagname} THEN 1 ELSE 0 END)` line, I summarize the number of posts that have a particular tag.
5. Merged the posts, _post_tags_ and tags tables.
6. Grouped the results by day of the week to calculate the total number of posts and posts with the specified tag for each day of the week.
7. Organized the results by day of the week.

**Endpoint 4**

**GET /v2/posts?duration=:duration in minutes&limit=:limit**

The output is a :limit list of the most recently resolved posts that have been opened for the maximum: duration in minutes (the number of minutes between creationdate and closeddate). Round the duration to two decimal places .

**SQL Request:**
```
SELECT id, creationdate, viewcount, lasteditdate, lastactivitydate, title, closeddate,
    ROUND(EXTRACT(EPOCH FROM (closeddate - creationdate))/60, 2) AS duration
FROM posts
WHERE closeddate IS NOT NULL
    AND CAST(ROUND(EXTRACT(EPOCH FROM (closeddate - creationdate))/60, 2) AS numeric) <= {duration}
ORDER BY closeddate DESC
LIMIT {limit}
```
**HTTP end-point call example**
```
{
  "items": [
    {
      "id": 1818849,
      "creationdate": "2023-11-30T15:55:32.137000+00:00",
      "viewcount": 22924,
      "lasteditdate": null,
      "lastactivitydate": "2023-11-30T15:55:32.137000+00:00",
      "title": "Why is my home router address is 10.x.x.x and not 100.x.x.x which is properly reserved and widely accepted for CGNAT?",
      "closeddate": "2023-11-30T15:59:23.560000+00:00",
      "duration": 3.86
    },
    {
      "id": 1818386,
      "creationdate": "2023-11-27T17:26:57.617000+00:00",
      "viewcount": 19,
      "lasteditdate": null,
      "lastactivitydate": "2023-11-27T17:26:57.617000+00:00",
      "title": "Are there any libraries for parsing DWG files with LGPL, MIT, Apache, BSD?",
      "closeddate": "2023-11-27T17:29:18.947000+00:00",
      "duration": 2.36
    }
  ]
}
```

This SQL query returns a list of the last solved posts that were opened within a certain time specified in minutes.

1. First, selected the columns we want, as well as the calculated duration, which is defined as the difference between _closeddate_ and _creationdate_ rounded to two decimal places from the posts table.
2. After filtering the records so that _closeddate_ is not empty (IS NOT NULL), and _duration_ is less than or equal to the specified maximum time duration.
3. Organized the results by _closeddate_ in descending order (DESC) so that the most recently solved posts are first in the list.
4. And limited the number of results returned to a specified number.

**Endpoint 5**

**GET /v2/posts?limit=:limit&query=:query**

Design an endpoint that provides a list of posts ordered from newest to oldest.
A complete list of associated tags is also included with the response. This endpoint supports two parameters:
- limit: the maximum number of posts in the response,
- query: a query string to query over posts.title and posts.body.

Matching is not sensitive to diacritics and lowercase/uppercase characters.

**SQL Request:**
```
SELECT p.id, p.creationdate, p.viewcount, p.lasteditdate, p.lastactivitydate,
    p.title, p.body, p.answercount, p.closeddate,
    ARRAY_AGG(t.tagname) AS tags
FROM posts p
JOIN post_tags pt ON p.id = pt.post_id
JOIN tags t ON pt.tag_id = t.id
WHERE LOWER(p.title) LIKE LOWER({query}) OR LOWER(p.body) LIKE LOWER({query})
GROUP BY p.id, p.creationdate, p.viewcount, p.lasteditdate, p.lastactivitydate,
    p.title, p.body, p.answercount, p.closeddate
ORDER BY p.creationdate DESC
LIMIT {limit}
```
**HTTP end-point call example**
```
{
  "items": [
    {
      "id": 1819160,
      "creationdate": "2023-12-03T04:22:43.587000+00:00",
      "viewcount": 7,
      "lasteditdate": null,
      "lastactivitydate": "2023-12-03T04:22:43.587000+00:00",
      "title": "Keyboard not working on khali linux",
      "body": "<p>I have recently installed virtualbox on my windows 10 and trying to run Linux Ubuntu and Kali. Everything working on Ubuntu without any issue but when I am running kali it is not taking keyboard(Samsung bluetooth 500) input. Please can anyone help me out here.\nMany thanks in advance!!</p>\n",
      "answercount": 0,
      "closeddate": null,
      "tags": [
        "virtual-machine"
      ]
    }
  ]
}
```

This query provides a complete list of related tags for each post.

1. Firstly, I selected the required fields from the posts table, and use the ARRAY_AGG function to aggregate all the tags associated with each post into an array of tags.
2. Merged the _posts_, _post_tags_ and _tags_tables_ by their respective identifiers to get information about the associated tags for each post.
3. Filtered the posts that match the query, which can be contained in either the title or the content of the post. The LOWER function is used to ignore letter case when searching.
4. Grouped the results by _post_id_ so that each post has its own list of tags.
5. Organized the results by post creation date in descending order so that the newest posts are first in the list.
6. Finally, limited the number of results returned by the limit parameter.
