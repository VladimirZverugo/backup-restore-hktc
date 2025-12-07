# backup_restore
## How-to

1. 
    cp .env.example .env

2. Put your token into `.env`:
    ACCESS_TOKEN={token_from_task}
    [if you need my one - ping me via linkedin]

3. Start everything:
   docker-compose up --build


/////
docker exec -it backup_pg psql -U postgres -d backup_restore

\dt