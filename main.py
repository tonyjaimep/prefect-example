import requests
import json
from prefect import task, Flow
from collections import namedtuple
from contextlib import closing
import sqlite3
from prefect.tasks.database.sqlite import SQLiteScript
from prefect.schedules import IntervalSchedule

import datetime

create_tables_script = """
CREATE TABLE IF NOT EXISTS users (
    id INT,
    name TEXT,
    username TEXT,
    email TEXT,
    address TEXT CHECK (json_valid(address)),
    phone TEXT,
    website TEXT,
    company TEXT CHECK (json_valid(company)),
    PRIMARY KEY (id ASC)
);
"""

table_name = "users.db"

create_table = SQLiteScript(db=table_name, script=create_tables_script)


@task
def get_users_data():
    r = requests.get(
        "https://jsonplaceholder.cypress.io/users",
    )

    return json.loads(r.text)


@task
def parse_user_data(raw_user_data):
    users = []
    User = namedtuple(
        "user",
        ["id", "name", "username", "email", "address", "phone", "website", "company"],
    )
    for row in raw_user_data:
        this_user = User(
            id=row.get("id"),
            name=row.get("name"),
            username=row.get("username"),
            email=row.get("email"),
            address=json.dumps(row.get("address")),
            phone=row.get("phone"),
            website=row.get("website"),
            company=json.dumps(row.get("company")),
        )

        users.append(this_user)
    return users


@task
def store_users(parsed):
    insert_cmd = """
        INSERT INTO users(id, name, username, email, address, phone, website, company)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET 
            name=excluded.name,
            username=excluded.username,
            email=excluded.email,
            address=excluded.address,
            phone=excluded.phone,
            website=excluded.website,
            company=excluded.company
    """

    with closing(sqlite3.connect(table_name)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.executemany(insert_cmd, parsed)
            conn.commit()


def main():
    schedule = IntervalSchedule(interval=datetime.timedelta(minutes=1))

    with Flow("user sync flow", schedule) as f:
        db_table = create_table()
        raw_users_data = get_users_data()
        parsed_users = parse_user_data(raw_users_data)
        populated_table = store_users(parsed_users)
        populated_table.set_upstream(db_table)

    f.run()


if __name__ == "__main__":
    main()
