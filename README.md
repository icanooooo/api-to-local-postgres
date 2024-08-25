### Pipeline from scratch

So this is my repo for my pipeline from scratch project. I want to create pipeline from an API request (currently crypto currency) to data warehouse, and hopefully with automated orchestration. 

Example, with the api we currently getting we could create a daily crypto price table.

Current Progress:
- Adding docker-compose.yaml
- added dockerfile
- Succesfully ingest data from api and inserted into postgresql
- Successfully create volumes with docker (but when composed down data does not persist(?), only when container exited)

Status:
- Currently looking into airflow.
- May add a cron job to this project or branch, we'll see

** english is not my first language, even in my own language I have trouble with words lol

Thank you.