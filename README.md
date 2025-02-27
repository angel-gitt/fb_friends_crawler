Crawler.py is a crawler to obtain the friends URLS for a set of Facebook users

In the same folder, you should create a file called profiles.csv, containing each user profile in one line (without header)
Then you can create a venv, install the requirements and run the crawler.
    
    ```
    
    python3 -m venv .venv
    
    source .venv/bin/activate
    
    pip install-r requirements.txt
    
    python3 crawler.py 
    
    ```
    
It asks for your email and password the first time, to init facebook session. Then the browser profile is saved in chrome_profile/, and it loads with the facebook session up in upcoming executions
The friends of the users in profiles.csv are saved in friends.json
