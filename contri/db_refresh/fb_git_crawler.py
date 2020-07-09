from github import Github
from github.GithubException import GithubException
from multiprocessing import Pool
import sys, json, os
from datetime import datetime
from contri.db_refresh.db_table_utils import *


def crawl_and_insert(org,param,conn):
    print(param)
    if param['type'] == 'login':
        git = Github(param['user'], param['password'])
    else:
        git = Github(client_id=param['client_id'],client_secret=param['client_secret'])
    cur = conn.cursor()
    print('Starting Fetching data')
    try:
        repos = git.get_organization(org).get_repos()
        for i in repos:
            try:
                # print(i.name,i.created_at,i.full_name,i.id)
                cur.execute("INSERT OR IGNORE into public_repos (id,name,full_name,begin_date) values (?,?,?,?)",
                                (i.id,i.name,i.full_name,str(i.created_at)))
                conn.commit()

                # here it can be done better but i am fetching  the max(commit_date) from child table of that repo.
                # So  that i can perform incremental load on child table,  when next refresh happens
                cur.execute("select max(commit_dt) as last_commit_dt from public_repos_commits where repo_id = {}".format(i.id))
                result = cur.fetchone()[0]
                if result is None:
                    last_commit_date = datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
                else:
                    last_commit_date = datetime.strptime(result, '%Y-%m-%d %H:%M:%S')

                for j in i.get_commits(sha='master',since=last_commit_date):
                    # print(j.sha,j.commit.author.name,j.commit.author.date,j.committer.id,j.committer.name,j.committer.login)
                    cur.execute("INSERT OR IGNORE into public_repos_commits (commit_id,repo_id,author_name,commit_dt) values (?,?,?,?)",
                                    (j.sha,i.id,j.commit.author.name,j.commit.author.date))
                    conn.commit()

            except GithubException as e:
                # I can USE LOGGER for LOGGING
                print(e)
            except Exception as e:
                print(e)
        cur.close()
        conn.close()
        print('DATABASE TABLE REFRESHED')
        return 'DATABASE TABLE REFRESHED'
    except Exception as e:
        print('EXCEPTION OCCURED :- '+str(e))
        return 'EXCEPTION OCCURED :- '+str(e)


# Below is just for testing  ,if i want to run this program from shell
'''
if __name__ == "__main__":
    #pool = Pool(os.cpu_count())
    # get connection to db
    try:

        user = 'My Github Username'
        password = 'My Github Password'
        org_name = 'facebook'

        Client_ID = 'Github OAuth Client Id'
        Client_Secret = 'Github OAuth Client Secret Key'
       
        user_credentials = {'user':user,'password':password,'type':'login'}
        user_app_token = {'client_id': Client_ID, 'client_secret': Client_Secret, 'type': 'token'}
        conn = create_db_tables()
        response = crawl_and_insert(org_name, user_credentials,conn)
        print(response)
    except Exception as e:
        print(str(e))
'''

