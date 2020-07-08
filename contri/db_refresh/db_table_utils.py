import sqlite3
from sqlite3 import Error


def create_connection(db_file,timeout=5):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    x = timeout
    try:
        conn = sqlite3.connect(db_file,timeout=x)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def drop_table(conn, db_table):
    """ drop a table of mentioned schema and table from db_table
    :param conn: Connection object
    :param db_table: db_name.table_name or simply table_name
    :return:
    """
    try:
        c = conn.cursor()
        c.execute("""DROP TABLE IF EXISTS {}""".format(db_table))
    except Error as e:
        print(e)


def create_db_tables(database = "db/facebook_github.db"):

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS public_repos (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        full_name text NOT NULL,
                                        begin_date text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS public_repos_commits (
                                    commit_id text PRIMARY KEY,
                                    repo_id integer,
                                    author_name text,
                                    commit_dt text,
                                    FOREIGN KEY (repo_id) REFERENCES public_repos (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")
    return conn

