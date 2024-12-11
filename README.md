# Documentation for the REST API Project Based on PostgreSQL
## Project Description
The project is a REST API designed to work with a PostgreSQL database based on the dataset from Stack Exchange. The API allows executing SQL queries on the database and retrieving results in JSON format via HTTP endpoints.
* The program is available at the following link:
[SQLqueries & Endpoints](https://github.com/DariiaSira/SQLqueries__DatabaseModeling--STU-FIIT/tree/main/SQLqueries%26Endpoints)
* Documentation and a detailed description of the assignment can be found here:
[Documentations & Assignment](https://github.com/DariiaSira/SQLqueries__DatabaseModeling--STU-FIIT/tree/main/SQLqueries%26Endpoints/Documentations%26Assignment)



## Main Requirements
* **SQL Queries:** Only raw SQL queries are used for data processing. ORMs are prohibited.
* **JSON Responses:** Query results are returned in JSON format, structured according to a specified schema. Dates and times are formatted in ISO8601 (UTC).
* **REST API:** Each task is implemented as an HTTP endpoint that processes requests and returns data.
* **Database Connection:** Connection parameters are set via environment variables.

---
  
# Museum Database Design Documentation
## Overview
This project delivers a comprehensive database for managing museum operations. It includes entities with their relationships clearly defined in an ER diagram. The database is designed for PostgreSQL and supports efficient data organization and integrity.

* The complete project, including all files, SQL scripts, and documentation, is available at the following link:
[MuseumDatabaseModel](https://github.com/DariiaSira/SQLqueries-DatabaseModeling--STU-FIIT/tree/main/MuseumDatabaseModel)

The project is designed with scalability and adaptability in mind, ensuring it can evolve with potential future needs in museum management systems. It offers a reliable foundation for organizing and accessing critical museum-related information.

## Features
**1. Entity-Relationship Diagram:**
  * Clearly identifies entities and their relationships.
  * Defines cardinality and connection between entities such as "Museum hosts Exhibitions" and "Exhibitions include Artifacts."
    
**2. Relational Model:**
  * Normalized database schema with tables for each entity.
  * Includes essential attributes, primary keys, and foreign keys to represent real-world relationships.
  * Implements constraints like NOT NULL and UNIQUE for data consistency and accuracy.
    
**3. SQL Script:**
  * Creates the database structure, implementing all relationships and constraints as defined in the relational model.
  * Provides a robust and efficient foundation for querying and managing data.

**4. Use Cases:**
  * Practical scenarios supported by the design include retrieving exhibitions for a specific museum or listing artifacts associated with an exhibition.

**5. Documentation:**
  * Accompanied by a detailed PDF that explains the design choices, attributes, and relationships.
  * Includes examples of queries for interacting with the database.


  

