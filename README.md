# Pirate Themed Chat App
This project was designed to function as a chat application, where multiple users can connect and have a conversation. Implemented into the app is a pirate themed bot with many functionalities. This application was created using Flask, React, SocketIO, and a Postgres Database.

## Table of Contents 

1. [Installation](#installation)
2. [API](#api)
3. [Resolved Issues](#resolved-issues)
4. [Known Problems](#known-problems)
5. [Improvement](#improvement)
6. [Final Remarks](#final-remarks)

## Installation
Prerequisites: 

* Windows, MacOS, or Linux machine.
* [Git Bash](https://git-scm.com/downloads) installed in order to run Git commands.
* [Python](https://www.python.org/downloads/) installed in your system/virtual environment.

#### Install basic packages

To run this app, you first need to clone my repo to your local machine and then cd into it by typing the following commands on your terminal.

        git clone https://github.com/NJIT-CS490/project2-m1-mrm54.git
        cd project2-m1-mrm54

Now let us install the packages required to run the app! First step is to upgrade node to version 7, yum to the latest version, and pip to the latest version. Enter yes to any and all prompt, if given.

        nvm install 7
        sudo yum update
        sudo /usr/local/bin/pip install --upgrade pip

Next, lets setup SocketIO and React by installing the following packages. 

        npm install
        pip install flask-socketio
        pip install eventlet
        npm install -g webpack
        npm install --save-dev webpack
        npm install socket.io-client --save

Note: if you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says 'pip cannot be found', run `which pip` and use `sudo [path to pip from which pip] install` .

#### Setup PSQL Database

Next, we need to setup a PSQL Database to work with Python. Run the following commands to install psycopg, sqlalchemy, and postgresql. Enter yes to any and all prompts, if given.

        sudo /usr/local/bin/pip install psycopg2-binary
        sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1
        sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-doc

Run the following commands to initialize, start up and make a new superuser/database.

        sudo service postgresql initdb
        sudo service postgresql start
        sudo -u postgres createuser --superuser $USER
        sudo -u postgres createdb $USER

If you get an error saying 'could not change directory', that's normal! It worked!

Go into psql by typing `psql` and create a new user and password by running the following. Replace the [values] in this command with your own. Make note of your credentials as we will need it in the later steps!

        create user [some_username_here] superuser password '[some_unique_new_password_here]';

Now that everything is installed and setup, create a new file called `sql.env` and type the following line inside the file while replacing [username] and [password] with the same credentials you made on the previous step. Do not include the [].

        DATABASE_URL=postgresql://[username]:[password]@localhost/postgres

Quit out of psql by running `\q` . In order to enable your db admin password to work, open the following file in vim and replace all values of `ident` with `md5`, if it isn't already changed.

        sudo vim /var/lib/pgsql9/data/pg_hba.conf
        :%s/ident/md5/g

Close out of vim and then restart psql. Ensure that `sql.env` has the correct username/password of the superuser you created!
        
        sudo service postgresql restart

We also need to change the owner of the postgres database to the username that you created. This is required for heroku deployment which will be covered in the later steps. Go into psql by typing `psql` and run the following. The username should be the same username that you have in your `sql.env` file!

        ALTER DATABASE postgres OWNER TO [your_username]

#### Run the app

That is all for the initial setup! We will not have to re-run all of those commands anymore! Now, every time you want to run the application, you only have to do the following. Open up 3 terminals and run one line per terminal. Make sure you are in the root-level directory of the project.
        
        sudo service postgresql start
        npm run watch
        python app.py
        
If prompted to install webpack-cli, type 'yes'. If you are using AWS Cloud9, preview the application by clicking 'preview running application'. This should successfully render the HTML!

If there is an error from sqlalchemy saying relation 'chat' does not exist, follow these steps to create the table. On a new terminal, open up the python console by typing `python`, then do the following. 

        import models
        models.db.create_all()
        models.db.session.commit()
        exit()

This should create the table from the `models.py` file and now the code should work!

#### Deploy to Heroku and setup Heroku database

Once the code successfully runs locally, now we can deploy it for the world to see! We will be using Heroku to deploy. Sign up for an account [here.](https://dashboard.heroku.com/apps) Once the sign up process is complete, we need to install Heroku on your system, so in your terminal type the following command. Note that this might take some time to fully install.

        npm install -g heroku

Next go through the following steps to prepare for Heroku deployment.

        heroku login -i
        heroku create [your_app_name]

Now to setup postgres database on Heroku. Fill in [your_username] with the username in the `sql.env` file.

        heroku addons:create heroku-postgresql:hobby-dev
        heroku pg:wait
        PGUSER=[your_username] heroku pg:push postgres DATABASE_URL

It should ask for your password after this. This password should be the same password for the username you created. (Same password that is in the `sql.env` file). Enter it and run the following commands.

        heroku pg:psql
        select * from chat;
        \q

Now we can push the code to Heroku so that it can be deployed. The following command will do precisely that.

        git push heroku main

If all went correctly, the website should be up and running!! In case it does not load properly, you can debug it by running the following command on your console.

        heroku logs --tail

**[Back to top](#Pirate-Themed-Chat-App)**

## API

#### Funtranslate API

I used the endpoint 'https://api.funtranslations.com/translate/pirate.json?text=' to make the get request.

Note that there is a rate limit of 5 calls per hour in the free tier. There are no API credentials for the free tier.

#### Fungenerator API

I used the endpoint 'https://api.fungenerators.com/pirate/generate/insult?limit=5' to make the get request.

Note that there is a rate limit of 5 calls per day in the free tier. There are no API credentials for the free tier.

**[Back to top](#Pirate-Themed-Chat-App)**

## Resolved Issues

#### Issue #1: There was an error from sqlalchemy saying relation 'chat' does not exist.

* This means that the table to store the messages was not created. To resolve this, I opened up the python console on the terminal I was using by typing `python`, and then running the following commands to create the table.

        import models
        models.db.create_all()
        models.db.session.commit()
        exit()

#### Issue #2: PSQL Database default user required a password which was not set.

* Resolved by logging into my created user (the same login info that is in the `sql.env` file); and then using SQL syntax to set the password for the default user. I made the default user password the same as the password for my created user for simplicity. Prior knowledge of SQL and databases helped me figure this out.

        psql -d postgres -U [my_created_user]
        ALTER USER ec2-user WITH PASSWORD '[new_password]'

#### Issue #3: Sometimes funtranslate API would not give an output for longer sentences.

* I checked the error message and apparently the message could not append to the database because the database column for message could only store 120 characters. I found out from [this](https://dba.stackexchange.com/questions/189876/size-limit-of-character-varying-postgresql#:~:text=1%20Answer&text=The%20maximum%20number%20of%20characters,stored%20is%20about%201%20GB) website that the max number of characters for the varying character type is 10485760. Using SQL commands I was able to alter the the table to accept longer sentences.

        ALTER TABLE chat ALTER COLUMN message TYPE character varying(10485760)

#### Issue #4: When assigning new usernames for each new connection, the old username would not save resulting in everyone having the same username.

* The official [docs](https://flask-socketio.readthedocs.io/en/latest/) helped me resolve this issue. Adding the parameter `request.sid` to the socketio.emit call makes note of each unique session id/connection, thus being able to differentiate among the different connections.

        socketio.emit('userName', {
            'userName': name
        }, request.sid)

**[Back to top](#Pirate-Themed-Chat-App)**

## Known Problems

#### Problem #1: The title 'Chat App' on the top-center of the page gets cut off when shrinking the screen size.

* This can be fixed by putting it into its own container and keeping it a fixed size. Another possible way to fix this would be to have it shrink/grow in size relative to the screen size.

#### Problem #2: Usernames are generated via random numbers from 0 to 99999, so technically there is a tiny chance that two users can have the same name.

* This can be fixed by implementing a login page where users input their own username or login from a third party oauth such as google. This way I can implement code where users cannot have the same username.

#### Problem #3: The Button element of the app sticks to the top when there is no chat history to display.

* Some CSS tweaking should fix this issue. I would set the position to be absolute and set the bottom to 0. This should set the Button element to the bottom of the chat box container.

**[Back to top](#Pirate-Themed-Chat-App)**

## Improvement

#### Improvement #1: Add a friends list/blocked user list.

* I will most likely implement this in the next milestone since authentication will be be required to enter the chat room, thus making adding friends via their authenticated username easier. Also I would need to store usernames in a separate database column since the way it is right now, I have both the random username and message combined into one string.

#### Improvement #2: Show when a user is typing.

* I started implementing this feature, but due to lack of time decided to scratch it. I was looking into using the react debounce function or the timeout function but could not get it to work. The function would displays 'User is typing...' whenever the user types into the text box and then stop displaying that message after a number of seconds/when the user stops typing.

**[Back to top](#Pirate-Themed-Chat-App)**

## Final Remarks

Please feel free to let me know if any issues arise via the issues tab on Github. Also, if there is a big feature that would be beneficial to add, feel free to fork the repo and try to implement it or let me know so I can also attempt to add it and update the repository!

**[Back to top](#Pirate-Themed-Chat-App)**
