from string import Template
from flask import Flask, request, jsonify
from flask import render_template
import sqlite3
import os
import contri.db_refresh.fb_git_crawler as fb_db_refresh

curr_path = os.getcwd()
db_path = os.path.join(os.path.split(curr_path)[0], "db_refresh", "db", "facebook_github.db")
templateFileloc = os.path.join(curr_path, "templates")

app = Flask(__name__)


@app.route('/stats',methods=['GET'])
def get_stats():
    sql = """
    select 
    repo.name as repo_name,
    strftime('%Y-%m',commit_dt) as year_month,
    count(*) as monthly_contri
    from
    (
    select repo_id,author_name,min(commit_dt) as commit_dt
    from public_repos_commits
    group by repo_id,author_name
    ) commits inner join public_repos repo
    on repo.id = commits.repo_id
    group by repo.name,strftime('%Y-%m',commit_dt)
    order by repo.name,strftime('%Y-%m',commit_dt)
    """
    c.execute(sql)
    rows = c.fetchall()
    column_names = [i[0] for i in c.description]
    str_table_header_tag = ''.join(['''<th>{}</th>'''.format(col) for col in column_names])
    str_table_data_taf = ''.join(['<td>{{item[' + str(i) + ']}}</td>' for i in range(len(column_names))])
    template_tags_json = {'HEADER':str_table_header_tag,'DETAILS':str_table_data_taf}
    #c.close()
    monthly_data_template = os.path.join(templateFileloc, "monthly_contri.html")
    temp_template = tmpl_file_to_text(monthly_data_template,template_tags_json)
    if 'type' in request.args:
        type = str(request.args['type'])
        if type == 'table':
            return render_template(temp_template, data=rows, str_table_header_tag=str_table_header_tag, str_table_data_taf=str_table_data_taf)
        else:
            return 'Error: valid Type is only table'
    return jsonify(rows)


@app.route('/refreshdb',methods=['GET'])
def refresh_db_tables():
    org_name = 'facebook'
    if 'git_user' in request.args and 'git_pass' in request.args:
        try:
            git_user = str(request.args['git_user'])
            git_pass = str(request.args['git_pass'])
            user_credentials = {'user': git_user, 'password': git_pass, 'type': 'login'}
            conn_new = fb_db_refresh.create_db_tables(database=db_path)
            response = fb_db_refresh.crawl_and_insert(org_name, user_credentials,conn_new)
            print(response)
            return response
        except Exception as e:
            print('Error:-',str(e))
            return 'Error :- '+str(e)

    elif 'client_id' in request.args and 'client_secret' in request.args:
        try:
            Client_ID = str(request.args['client_id'])
            Client_Secret = str(request.args['client_secret'])
            user_app_token = {'client_id': Client_ID, 'client_secret': Client_Secret, 'type': 'token'}
            conn_new = fb_db_refresh.create_db_tables(database=db_path)
            response = fb_db_refresh.crawl_and_insert(org_name, user_app_token,conn_new)
            print(response)
            return response
        except Exception as e:
            print('Error:-',str(e))
            return 'Error :-'+str(e)
    else:
        return 'Please Provide Valid Github User/Password OR  App Oth -Client_ID/Client_Secret token combo.'


def tmpl_file_to_text(templateFile, values):
    try:
        os.remove(os.path.join(templateFileloc, "monthly_contri_temp.html"))
    except:
        print('Jussst Deleting  the temporary templates ..just deleting!!')
        pass
    inputFile = open(templateFile, 'r')
    mailTemplate = Template(inputFile.read())
    mailText = mailTemplate.substitute(values)
    temp_template_file = os.path.join(templateFileloc,"monthly_contri_temp.html")
    with open(temp_template_file, 'w') as file:
        file.write(mailText)
    return "monthly_contri_temp.html"


if __name__ == '__main__':
    conn = sqlite3.connect(db_path,check_same_thread=False)
    c = conn.cursor()
    app.run(debug=True)

