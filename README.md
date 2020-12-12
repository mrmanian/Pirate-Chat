# [Pirate Chat](https://mrmchat.herokuapp.com/)
This project was designed to function as a chat application, where multiple users can connect and have a conversation. Implemented into the app is a pirate themed bot with many functionalities. This application was created using Flask, React, SocketIO, and a Postgresql database with SQLAlchemy.

## Table of Contents 

1. [Installation](#installation)
2. [API](#api)
3. [OAuth](#oauth)
4. [Known Problems](#known-problems)
5. [Improvement](#improvement)
6. [Final Remarks](#final-remarks)

## Installation
Prerequisites: 

* Windows, MacOS, or Linux machine.
* [Git Bash](https://git-scm.com/downloads) installed in order to run Git commands.
* [Python](https://www.python.org/downloads/) installed in your system/virtual environment.

#### **Install basic packages**

To run this app, you first need to clone my repo to your local machine and then cd into it by typing the following commands on your terminal.

        git clone https://github.com/mrmanian/Pirate-Chat.git
        cd Pirate-Chat

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

Let us also install packages used for linting and checking coverage.

        pip install pylint --upgrade
        sudo $(which pip) install black
        pip install alchemy-mock
        pip install coverage
        npm install -g eslint
        npm init
        eslint --init

Accept the default options for eslint or configure it to your liking.

Install a couple other npm packages I used for styling and creating login buttons.

        npm install react-facebook-login
        npm install react-google-login
        npm install react-social-login-buttons
        npm install react-linkify

Note: if you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says 'pip cannot be found', run `which pip` and use `sudo [path to pip from which pip] install` .

#### **Setup PSQL Database**

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

Now that everything is installed and setup, create a new file called `keys.env` and type the following line inside the file while replacing [username] and [password] with the same credentials you made on the previous step. Do not include the [].

        DATABASE_URL=postgresql://[username]:[password]@localhost/postgres

Quit out of psql by running `\q` . In order to enable your db admin password to work, open the following file in vim and replace all values of `ident` with `md5`, if it isn't already changed.

        sudo vim /var/lib/pgsql9/data/pg_hba.conf
        :%s/ident/md5/g

Close out of vim and then restart psql. Ensure that `keys.env` has the correct username/password of the superuser you created!
        
        sudo service postgresql restart

We also need to change the owner of the postgres database to the username that you created. This is required for heroku deployment which will be covered in the later steps. Go into psql by typing `psql` and run the following. The username should be the same username that you have in the `keys.env` file you created!

        ALTER DATABASE postgres OWNER TO [your_username]

#### **Run the app**

That is all for the initial setup! We will not have to re-run all of those commands anymore! Now, every time you want to run the application, you only have to do the following. Open up 3 terminals and run one line per terminal. Make sure you are in the root-level directory of the project.
        
        sudo service postgresql start
        npm run watch
        python app.py
        
If prompted to install webpack-cli, type 'yes'. If you are using AWS Cloud9, preview the application by clicking 'preview running application'. This should successfully render the HTML!

If there is an error from sqlalchemy saying relation 'chat_history' does not exist, follow these steps to create the table. On a new terminal, open up the python console by typing `python`, then do the following. 

        import models
        models.db.create_all()
        models.db.session.commit()
        exit()

This should create the table from the `models.py` file and now the code will work!

#### **Run the Unit Tests**

I have configured all the files into the repository already so to run the unit tests, run the following command on the root directory. Make sure you start the psql database though.

        sudo service postgresql start
        coverage run -m --source=. unittest tests/*.py && coverage html

#### **Deploy to Heroku and setup Heroku database**

Once the code successfully runs locally, now we can deploy it for the world to see! We will be using Heroku to deploy. Sign up for an account [here.](https://dashboard.heroku.com/apps) Once the sign up process is complete, we need to install Heroku on your system, so in your terminal type the following command. Note that this might take some time to fully install.

        npm install -g heroku

Next go through the following steps to prepare for Heroku deployment.

        heroku login -i
        heroku create [your_app_name]

Now to setup postgres database on Heroku. Fill in [your_username] with the username in the `keys.env` file.

        heroku addons:create heroku-postgresql:hobby-dev
        heroku pg:wait
        PGUSER=[your_username] heroku pg:push postgres DATABASE_URL

It should ask for your password after this. This password should be the same password for the username you created. (Same password that is in the `keys.env` file). Enter it and run the following commands.

        heroku pg:psql
        select * from chat_history;
        \q

Once that is complete, navigate to [this](https://dashboard.heroku.com/apps) website and click on your newly created app. Click on Settings, then scroll to "Config Vars." Click "Reveal Config Vars" and add the key value pairs for each environmental variable. In this case, we only need to input the key for the Giphy API. Check the API section of the README to see how to setup Giphy. Go to the `keys.env` file and copy the name and key exactly onto heroku. Also, under buildpacks, add 'heroku/python' and 'heroku/nodejs'.

Now we can push the code to Heroku so that it can be deployed. The following command will do precisely that.

        git push heroku main

If all went correctly, the website should be up and running!! In case it does not load properly, you can debug it by running the following command on your console.

        heroku logs --tail

**[Back to top](#Pirate-Chat)**

## API

#### Funtranslate API

I used the endpoint 'https://api.funtranslations.com/translate/pirate.json?text=' to make the get request.

Note that there is a rate limit of 5 calls per hour in the free tier. There are no API credentials for the free tier.

#### Fungenerator API

I used the endpoint 'https://api.fungenerators.com/pirate/generate/insult?limit=5' to make the get request.

Note that there is a rate limit of 5 calls per day in the free tier. There are no API credentials for the free tier.

#### Giphy API

Sign up for an account [here](https://developers.giphy.com/) and confirm your email address. After confirmation, you will get an API key. Make note of the key and enter the following inside your `keys.env` file. 

        GIPHY_KEY=[your_api_key]

I used the endpoint 'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&limit=1&q=' to make the get request. Put your own API key where it says {GIPHY_KEY}.

**[Back to top](#Pirate-Chat)**

## OAuth

#### Google OAuth

Go to the [google](https://console.developers.google.com/) website and sign up for a developer account or login to your existing personal account. Click "CREATE PROJECT" or in the dropdown menu called "Select a Project" in the top, click "NEW PROJECT". Click "Credentials" in the left hand bar, then click "+ CREATE CREDENTIALS" and then click "OAuth client ID". If you see a warning that says "To create an OAuth client ID, you must first set a product name on the consent screen", do the following steps: 1. Click the "CONFIGURE CONSENT SCREEN" button. 2. Choose "External" 3. For "Application name," specify a name for your app. Go back to Credentials -> Create Credentials -> OAuth client ID. Once that is done, click on the pen icon on your newly created app. Enter in the name of your website/local environment where it says "URIs". There should be two places where it says that, enter it in both.

Note that this client ID does not have to be kept a secret. Input your unique ID in the `GoogleLoginButton.jsx` in the following place replacing [your_client_id]:
        
        return (
                <GoogleLogin
                clientId='[your_client_id]'
                render={renderProps => (
                        <GoogleLoginButton onClick={renderProps.onClick} disabled={renderProps.disabled}></GoogleLoginButton>
                )}
                onSuccess={handleSubmit}
                onFailure={handleFailure}
                cookiePolicy={'single_host_origin'}
                />
        );


#### Facebook OAuth

Go to the [facebook](https://developers.facebook.com/apps) website and sign up for a developer account or login to your existing personal account. Click "CREATE APP" then when prompted select "FOR EVERYTHING ELSE". Enter your app name and contact email address. Click enter and scroll down to where it says products and select Facebook Login. Click on "Settings" and then where it says "Valid OAuth Redirect URI" enter the name of your website/local environment. 

Note that this app ID does not have to be kept a secret. Input your unique ID in the `FacebookLoginButton.jsx` in the following place replacing [your_app_id]:

        return (
                <FacebookLogin
                appId='[your_app_id]'
                autoLoad={false}
                fields='name,picture'
                callback={handleSubmit}
                onFailure={handleFailure}
                render={renderProps => (
                        <FacebookLoginButton onClick={renderProps.onClick}></FacebookLoginButton>
                )}
                /> 
        );

**[Back to top](#Pirate-Chat)**

## Known Problems

#### Problem #1: Showing the number of users connected works perfectly fine, but there is one caveat- the user must logout otherwise the number will not update.

* I tried searching for ways to send an alert if the user closes the screen without pressing logout, but could not find anything. Also, a user can continuously login many times in one window and the user count will increment. This is because the user did not logout before logging into another account. Another option is to make a separate login page rather than have it in the same page as the chatbox.

#### Problem #2: The app displays when the user is typing, but it does not show to everyone.

* I managed to implement a feature where it shows when a user is typing, however, it only shows it in the users screen and not to everyone. I would have to emit the ' is typing' message across all users, but it is not simple since the message is dynamically changing. And if multiple users are typing at the same time the texts would overlap.

**[Back to top](#Pirate-Chat)**

## Improvement

#### Improvement #1: Add a friends list/blocked user list.

* An improvement would be to create a separate section which displays a list of friends or blocked users. To do this, I would have to make special note of every user that logs on and maintain a separate database with any friends/blocked users they added.

#### Improvement #2: Render url link preview in-line.

* I implemented this feature using the library react-tiny-link, however the app would break and render useless if an invalid url link was entered, so I removed it completely. How I originally did it was I searched if the message had an 'http' in it, and if it did, I would pass the react-tiny-link object with the message as the parameter and it will do the rest. If the link is invalid, or if the link does not start with http, for example 'espn.com' will not render as a link. The way I can fix this would be to call a function that will verify that the message is indeed a valid url before returning the react-tiny-link object.

#### Improvement #3: Make the login buttons on a separate page.

* Creating a separate login page would make the app look better for starters, and it would also fix the issue regarding counting the number of online users. I would have the login page load first, then after the user authenticates, it will hide, making the actual chatbox page come into view.

**[Back to top](#Pirate-Chat)**

## Final Remarks

Please feel free to let me know if any issues arise via the issues tab on Github. If there is a big feature that would be beneficial to add, feel free to fork the repo and try to implement it or let me know so I can also attempt to add it and update the repository!

**[Back to top](#Pirate-Chat)**
