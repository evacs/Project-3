## Setting up Hosted Database in pgAdmin

Install psycopg2 Module
This is needed for SQLAlchemy to connect with the hosted database.
1. Open gitbash or terminal.
2. Run "pip install psycopg2".

Create server and database in pgAdmin
1. Right click on Server under Object Explore, then Register, then Server.
2. On the General tab, enter a name (I did "Render PostgreSQL 15" as it's hosted by Render).
3. On the Connection tab, enter the following information:
   - Host name/address: dpg-ck56k66ru70s738p5s4g-a.oregon-postgres.render.com
   - Port: 5432 (that should be the default)
   - Password: fRFTp6MgD7AgfQYMYmyM5jaR8KAfKyXV
4. Click on Save

Notes:
- pgAdmin will occasion lose the connection to the db. Usually, running a simply query (like a select to view all records in a table) will fix this but you may have to close and restart pgAdmin. You can also disconnect and reconnect from the server (right click on server name to do this)