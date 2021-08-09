#print("Running")
import subprocess
import os
from dotenv import load_dotenv
load_dotenv()
postgresql_uri = os.environ.get("POSTGRES_URI")
#subprocess.run('ls')

os.system("pg_dump --dbname={uri} > /home/jdreeder1/backup.txt".format(uri = postgresql_uri))

