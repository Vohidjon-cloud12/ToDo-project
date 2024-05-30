import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_params = {
    'database': os.getenv('database'),
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'port': os.getenv('port'),
}
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    status VARCHAR(30) NOT NULL,
    login_try_count INT NOT NULL
);
"""

create_todos_table = """
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    todo_type VARCHAR(15) NOT NULL,
    user_id INT REFERENCES users(id)
);
"""

def create_table():
    cur.execute(create_users_table)
    cur.execute(create_todos_table)
    conn.commit()

def migrate():
    insert_into_users = """
    INSERT INTO users (username, password, role, status, login_try_count)
    VALUES ('admin', '123', 'SUPERADMIN', 'ACTIVE', 0)
    ON CONFLICT (username) DO NOTHING;
    """
    cur.execute(insert_into_users)
    conn.commit()

def init():
    create_table()
    migrate()
