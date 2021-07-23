
Requirements
1. Airflow 2.1.0
2. Postgres
3. Docker 

This code provides data pipeline scenarios and dag solutions.

1. A person X wants to track every rocket launch that is happening around the world. To being with he wants to collect images of rockets that were launched from here [https://ll.thespacedevs.com/2.0.0/launch/upcoming]

- Tasks
-- Download launches JSON to a location /tmp/launches.json
-- Get pictures by parsing the JSON and downloading the image
-- Notify user using via logs, a simple echo using BASH.

- Operators used
-- BashOperator to curl the API and get JSON
-- PythonOperator to parse JSON and generate a URL list, and download the images to /tmp/images/<image>
-- BashOperator to notify Airflow user.


2. A company wants to collect users data from a website  on daily basis for marketting purposes and store it locally.

- Tasks
-- Fetch JSON from here[http:/ /localhost:5000/events]
-- Calculate statistics for single file
-- Use @daily, start date, execution date & end-date, Jinja template syntax to specify dates
-- Partition data
-- Update Calculate statistics method multiple files from a directory using Python's KeyWorded Arguments

-Operators
-- BashOperator to curl and get the required JSON
-- PythonOperator to calculate statistics using Pandas

- Scheduler
-- Using Airflow's scheduler options like @daily, start_date, end_date, execution_date and {{ ds }}
-- Partion data by writing different files that are recoreded everyday by using file name as date

References and thanks to:
- Data Pipelines with Apache Airflow by Bas Harenslak, Julien de Ruiter
- Github repo by puckel - https://github.com/puckel/docker-airflow
- Github repo by neylsoncrepalde - https://github.com/neylsoncrepalde/docker-airflow

3. A wikipedia page is queried often to get page view counts of 5 companies(FB, Microsoft, Google, Apple and Amazon). A gzip file is available from wikipedia which can be downloaded and queried for page counts.

To Do:
1. Download a gzip file for page from wikipedia
2. Unzip the downloaded file
3. Fetch page counts for the given 5 companies
4. Write data to postgres database  

Operators
1. A python operator that uses Jinja templating to define dates in the Python callable function.
2. A bash operator to unzip the downloaded the file located in tmp/wikipageviews.gz
3. A python operator to parse input data, get counts and write a /tmp/postgres_query.sql file that can be   used for a database operation. This is to keep tasks atomic.
4. An external postgres database can be used, but for sake of simplicity I've write the results to Airflow's database(this can be arguably avoided in production environments). wikipedia_postgres_hook.py to understand the connections and setup required.
