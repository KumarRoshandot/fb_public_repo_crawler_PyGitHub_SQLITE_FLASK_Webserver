# fb_public_repo_crawler_PyGitHub_SQLITE_FLASK
## This is  to crawl Data from Github  API of FB Public Repos , save it in SQLITE db and Build an WebServer Using Flask to show monthly contribution
	
	─────────────────────
	│GitHUb Facebook API│
	─────────────────────
	        │
		│
	    Crawler(PyGitHUb)
		│
		│
		↓
	 ─────────────────────────                  ────────────────────           ────────────────
	│facebook_github.db(SQLIte)│──────────────>│Webserver(Flask APP)│────────>│Browser(API URL)│
	 ──────────────────────────                 ────────────────────           ────────────────


	Okay here it buddy boy ,you hide my cloths i am wearning everything u own.(Friends Series--Jooey , chandler)

	
	well not everyting i  have  missed  out a lot of things ,  but lets see 
	
	
	1) okay  the  main thing is an API which  will show u the monthly contribution of FB public repos.
	2) when u hit that  API in browser it will display data  in 2 formats ,either  its JSON or Tabular view 
	   depending on the parameter u are passing  to an API.
	3) The Data  is residing in  database 'facebook_github.db' already and is given to u in ZIP with tables 
	    and data in it.
	4) The crawler i used took a very good  amount of time to fetch  all  data from facebook github API 
	    and insert it into database tables. 
	    THATS  WHY THE DB FILE WITH  PRE LOADED DATA HAS BEEN ATTACHED WITH  THIS FOLDER. 
	5) Now The API which calculate Monthly Data will simply hit database ,calculate and 
	    show results to browser (nothing else)
	6) There is an another API which will simply refresh the underlying database tables ,basically it will 
	   crawl Facebook github  API and look  for fresh records or commits across all its public  repositories,  
	    This  API  will take  some  good amount of time to  refresh  database tables ...
	   so if you  hit  it u  better go  get yourself  a coffeee and watch some friends series clips  .
	
			
	
	
 ## Setup before u  do anything :-

	1) I have  worked it using pycharm tool and on windows machine.
		--> Install Python (better 3+)
		--> Pip install Flask, PyGitHub
	2) Download this ZIP and Extract to 'contri' folder to one location (for e.g..  c:\contri)
	
	3) Under this folder you  will see follwing  structure 
	   ├── contri
	         ├── custom_api
	         │    ├── templates
	         │    │       ├──monthly_contri.html
	         │    ├── __init__.py
	         │    └── monthly_contribution_api.py
	         ├── db_refresh
	           ├── db
	           │   ├──facebook_github.db   ( Now this is zipped ,so make sure u extract it and place it like this)
	           ├── __init__.py
	           ├── fb_git_crawler.py
	           └── db_table_utils.py
	
	
	4) Sub folder (db_refresh):-
		a) fb_git_crawler.py 
			--> This is the crawler program which will fetch data from  github API of Facebook organization.
			--> I have used Github library  for  this 'github' , this is awesome .
			--> You will ask why not use simple 'request' library  from python ,
			     well i can use it but i came across this 'github' library which  is so simple  to use and 
			     comes with so many functionalites which can server my purpose .
			--> whole  thing is how i can  use less lines of code and fulfill my requirement.
			--> so 'github' , all i have to  do is i pass github registered username and password OR github 
			    Oth-APP Client_ID and ACCESS_KEY (Token combo) and wallah ...i can fetch data .
			--> now i just have to fetch organization public repos information and how few details of all  
			    the commits  that has happened on all  that  public repositories.
			--> once i have the required columns , i am inserting  those information in Database tables.
			--> Database information is  next
		
		b) db_table_utils.py
			--> This  is a place  where i have defined database tables creation , drop , making an 
			     connection and other stuff.
			--> Here i have used SQLITE database , since its so cool , handy and so much light  which can 
			    easily be integrated in this  usecase.
			--> So what i have  done is i have created a Database 'facebook_github.db' which is present in its 
			    sub folder 'db'.
			--> Within this database i have made 2 tables , 
			     one is master and other is child (with Primary and foreign  key relationship.)
			--> Master Table (public_repos)
					--> This is table which will have  following columns 
					--> id ( The unique  ID for one repository, PRIMARY  KEY)
					--> name ( The name of that Repository)
					--> full_name  ( Kind of Full name , value begins with organization)
					--> begin_date ( The  creation  date  of  that repository)
			--> Child Table (public_repos_commits)
					--> This is table which will have  following columns 
					--> commit_id ( The unique  Commit  ID when one  commit happens at repo, PRIMARY  KEY)
					--> repo_id ( The Repo_id of that public  repository , FORIEGN KEY to Master table  (ID))
					--> author_name  ( The person/user who made the commit)
					--> commit_dt ( The date on which commit happens)
	
	4) Sub folder (custom_api):-
		a) monthly_contribution_api.py
			--> Place  where i have  build a APP using Flask Library.
			--> 2 action  that i want it to perform 
				--> one calculate monthly  contribution  data  and  return result
				--> another one  is just optional  thing ,  
				    if i want to refresh data in tables then it can just do  that.
			--> Both action can  be controlled by API it has generated , by passing  relevant parameters
			--> for e.g..  http://127.0.0.1:5000/stats can give u ur monthly data 
			       But http://127.0.0.1:5000/refreshdb will refresh database 
						 (synchronize with fresh commits that has happened newly)
						 
						 
			--> Lets see the MONTHLY data API.
	
				 API for monthly report
					1) http://127.0.0.1:5000/stats
					This will  just  display the Data  in a JSON Format with repository name ,months ,count 
					
					2) http://127.0.0.1:5000/stats?type=table
					--> Now this is just a additional parameter if u specify then give this value as table', 
					    now i have set only table view type.we can also have like chart view but we can do 
							that later.
					--> So you will get  the  entire information in tablular  view.
					
					3) I am displaying it on browser using  HTML Template ( under templates folder)

			--> Lets see the REFRESH database API.
			
			   API To Refresh  DATABASE TABLES
					1) http://127.0.0.1:5000/refreshdb?git_user=<username>&git_pass=<password>  
					    OR
						http://127.0.0.1:5000/refreshdb?client_id=<ClientID>&client_secret=<SecretKey>
						
					--> This will hit  the  program made to crawl API of facebook public repositories ,
					    check for fresh commits and insert that to database tables.
					--> Now  Github API to access You need to have  a username and password, 
					    so these  can be passed  to the above API made for username and password.
					--> Github also has this flexiblty to  make your own OAuth Apps where you will 
					    get your own  Client ID and Client Secret key , so pass this to the  
							above API made for OAuth API.
					
					--> Just Remmember , this will  take a very good amount of time ..
					    so better do it at the end,since i am already giving PreLoaded
							Database tables with this folder setup.
	
		
	
### TO  Run  the APP :-
	1) python monthly_contribution_api.py 
    --> Once its running, go  to  browser and use the mentioned API to  get required data
		
		
### Limitations / Worries :-
	--> The Crawler  took a considerable amount of time to fetch data and insert into tables.
	--> We can parallelize it using Multiprocessing Pool to fasten the crawling.
	--> The API which shows monthly results is like a complete snapshot displayed in browser.
		--> This could  be  made like first  page user will get all public repositories.
		--> when user click on any repository , it will  navigate to another page showing its monthly contribution.
	--> The Report could have been made  monthly column  wise , i could have  used pivot  approach or another approach.
	 
	 
	 
#### SQL QUERY to get the desired results:-
  --> This  is based on the  2 tables mentioned earlier 

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
	limit 10	 
 	 
