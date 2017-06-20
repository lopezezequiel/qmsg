psql -c "DROP DATABASE IF EXISTS name $DATABASE_NAME;" -U postgres

psql -c "CREATE DATABASE $DATABASE_NAME;" -U postgres

psql -c "CREATE USER $DATABASE_USER WITH PASSWORD '$DATABASE_PASSWORD';" -U postgres

psql -c "ALTER ROLE $DATABASE_USER SET client_encoding TO 'utf8';" -U postgres
psql -c "ALTER ROLE $DATABASE_USER SET default_transaction_isolation TO 'read committed';" -U postgres
psql -c "ALTER ROLE $DATABASE_USER SET timezone TO 'UTC';" -U postgres

psql -c "GRANT ALL PRIVILEGES ON DATABASE $DATABASE_NAME TO $DATABASE_USER;" -U postgres

psql -c "ALTER USER $DATABASE_USER CREATEDB;" -U postgres
