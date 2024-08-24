### Pipeline from scratch

So this is my repo for my pipeline from scratch project. I want to create pipeline from an API request (currently crypto currency) to data warehouse, and hopefully with automated orchestration. 

Example, with the api we currently getting we could create a daily crypto price table.

Current Progress:
- Adding docker-compose.yaml
- added dockerfile
- Succesfully ingest data from api and inserted into postgresql
- Successfully create volumes with docker (but when composed down data does not persist(?), only when container exited)

Next:
- add a cron job (maybe with airflow, idk)
- check if volumes can persist after compose down(?)

** english is not my first language, even in my own language I have trouble with words lol

Thank you.