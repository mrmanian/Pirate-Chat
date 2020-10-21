# Pirate Themed Chat App
This project was designed to function as a chat application, where multiple users can connect and have a conversation. Implemented into the app is a pirate themed bot with many functionalities. This application was created using Flask, React, SocketIO, and a Postgresql Database with SQLAlchemy.

## Table of Contents 

1. [Installation](#installation)
2. [API](#api)
3. [OAuth](#oauth)
4. [Resolved Issues Milestone 1](#resolved-issues-milestone-1)
5. [Known Problems Milestone 1](#known-problems-milestone-1)
6. [Resolved Issues Milestone 2](#resolved-issues-milestone-2)
7. [Known Problems Milestone 2](#known-problems-milestone-2)
8. [Extra Credit Features](#extra-credit-features)
9. [Improvement](#improvement)
10. [Final Remarks](#final-remarks)

## Installation
Prerequisites: 

* Windows, MacOS, or Linux machine.
* [Git Bash](https://git-scm.com/downloads) installed in order to run Git commands.
* [Python](https://www.python.org/downloads/) installed in your system/virtual environment.

#### **Install basic packages**

To run this app, you first need to clone my repo to your local machine and then cd into it by typing the following commands on your terminal.

        git clone https://github.com/NJIT-CS490/project2-m2-mrm54.git
        cd project2-m2-mrm54

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

We also need to change the owner of the postgres database to the username that you created. This is required for heroku deployment which will be covered in the later steps. Go into psql by typing `psql` and run the following. The username should be the same username that you have in your `keys.env` file!

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

This should create the table from the `models.py` file and now the code should work!

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

Once that is complete, navigate to [this](https://dashboard.heroku.com/apps) website and click on your newly created app. Click on Settings, then scroll to "Config Vars." Click "Reveal Config Vars" and add the key value pairs for each environmental variable. In this case, we only need to input the key for the Giphy API. Go to the `keys.env` file and copy the name and key exactly onto heroku.

Now we can push the code to Heroku so that it can be deployed. The following command will do precisely that.

        git push heroku main

Also, go to your heroku [dashboard](https://dashboard.heroku.com/apps) and click on your newly created app and go to settings. Under buildpacks, add 'heroku/nodejs' and 'heroku/python' if they are not there already.

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

#### Giphy API

Sign up for an account [here](https://developers.giphy.com/) and confirm your email address. After confirmation, you will get an API key. Make note of the key and enter the following inside your `keys.env` file. 

        GIPHY_KEY=[your_api_key]

I used the endpoint 'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&limit=1&q=' to make the get request. Put your own API key where it says {GIPHY_KEY}.

**[Back to top](#Pirate-Themed-Chat-App)**

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

**[Back to top](#Pirate-Themed-Chat-App)**

## Resolved Issues Milestone 1

#### Issue #1: There was an error from sqlalchemy saying relation 'chat_history' does not exist.

* This means that the table to store the messages was not created. To resolve this, I opened up the python console on the terminal I was using by typing `python`, and then running the following commands to create the table.

        import models
        models.db.create_all()
        models.db.session.commit()
        exit()

#### Issue #2: PSQL Database default user required a password which was not set.

* Resolved by logging into my created user and then using SQL syntax to set the password for the default user. I made the default user password the same as the password for my created user for simplicity. Prior knowledge of SQL and databases helped me figure this out.

        psql -d postgres -U [my_created_user]
        ALTER USER ec2-user WITH PASSWORD '[new_password]'

#### Issue #3: Sometimes funtranslate API would not give an output for longer sentences.

* I checked the error message and apparently the message could not append to the database because the database column for message could only store 120 characters. I found out from [this](https://dba.stackexchange.com/questions/189876/size-limit-of-character-varying-postgresql#:~:text=1%20Answer&text=The%20maximum%20number%20of%20characters,stored%20is%20about%201%20GB) website that the max number of characters for the varying character type is 10485760. Using SQL commands I was able to alter the the table to accept longer sentences.

        ALTER TABLE chat_history ALTER COLUMN message TYPE character varying(10485760)

#### Issue #4: When assigning new usernames for each new connection, the old username would not save resulting in everyone having the same username.

* The official [docs](https://flask-socketio.readthedocs.io/en/latest/) helped me resolve this issue. Adding the parameter `request.sid` to the socketio.emit call makes note of each unique session id/connection, thus being able to differentiate among the different connections.

        socketio.emit('userName', {
            'userName': name
        }, request.sid)

**[Back to top](#Pirate-Themed-Chat-App)**

## Known Problems Milestone 1

#### Problem #1: The title of the app on the top-center of the page gets cut off when shrinking the screen size.

* This can be fixed by putting it into its own container and keeping it a fixed size. Another possible way to fix this would be to have it shrink/grow in size relative to the screen size.

#### Problem #2: Usernames are generated via random numbers from 0 to 99999, so technically there is a tiny chance that two users can have the same name.

* This can be fixed by implementing a login page where users input their own username or login from a third party oauth such as google. This way I can implement code where users cannot have the same username.

#### Problem #3: The input/submit button element of the app sticks to the top when there is no chat history to display.

* Some CSS tweaking should fix this issue. I would set the position to be absolute and set the bottom to 0. This should set the Button element to the bottom of the chat box container.

**[Back to top](#Pirate-Themed-Chat-App)**

## Resolved Issues Milestone 2

#### Issue #1: Styling problems from Milestone 1 mentioned above.

* Resolved by adding the title of the app inside the same container where the number of online users are displayed. This ensures that it remains visible even if the page shrinks. Also resolved the input/submit button issue by setting the height and width the same as the chatbox container.

#### Issue #2: UseEffect runs multiple times when I only want it to run once per change.

* Resolved by adding a second parameter [] to the useEffect call. [This](https://css-tricks.com/run-useeffect-only-once/) website helped be figure out this solution.

        useEffect(() => {
            // Task
        }, []);

#### Issue #3: Could not filter out the map of messages to determine what is an image and what is a url inside the return statement.

* This took a while to figure out for me since I could not perform conditional statements inside a map function in react. After lots of researching, [this](https://stackoverflow.com/questions/44969877/if-condition-inside-of-map-react) website showed me two options to do it. I could either do it by a ternary operator or create a regular javascript function and call that function inside the return. I chose to call a separate function since that was simpler and more apt to my needs.

**[Back to top](#Pirate-Themed-Chat-App)**

## Known Problems Milestone 2

#### Problem #1: Showing the number of users connected works perfectly fine, but there is one caveat- the user must logout otherwise the number will not update.

* I tried searching for ways to send an alert if the user closes the screen without pressing logout, but could not find anything. Also, a user can continuously login many times in one window and the user count will increment. This is because the user did not logout before logging into another account. Another option is to make a separate login page rather than have it in the same page as the chatbox.

#### Problem #2: The app displays when the user is typing, but it does not show to everyone.

* I managed to implement a feature where it shows when a user is typing, however, it only shows it in the users screen and not to everyone. I would have to emit the ' is typing' message across all users, but it is not simple since the message is dynamically changing. And if multiple users are typing at the same time the texts would overlap.

**[Back to top](#Pirate-Themed-Chat-App)**

## Extra Credit Features

#### Feature #1: User can see when they are typing in real time. Does not emit to other users though, if I had more time I could probably figure it out.

* I used lodash's debounce function to figure this out. When there is a change in the input field where the user is typing the message, the debounce function will call itself and display the username followed by ' is typing' for 1.5 seconds.

#### Feature #2: Add Facebook OAuth.

* Added Facebook OAuth for authentication via the steps listed under [OAuth](#oauth).


#### Feature #3: Implement gif command using Giphy API.

* Added a bot feature where calling !!gif followed by a word or phrase, will output a related gif. I did this via the steps listed under [API](#api).

**[Back to top](#Pirate-Themed-Chat-App)**

## Improvement

#### Improvement #1: Add a friends list/blocked user list.

* An improvement would be to create a separate section which displays a list of friends or blocked users. To do this, I would have to make special note of every user that logs on and maintain a separate database with any friends/blocked users they added.

#### Improvement #2: Render url link preview in-line.

* I implemented this feature using the library react-tiny-link, however the app would break and render useless if an invalid url link was entered, so I removed it completely. How I originally did it was I searched if the message had an 'http' in it, and if it did, I would pass the react-tiny-link object with the message as the parameter and it will do the rest. If the link is invalid, or if the link does not start with http, for example 'espn.com' will not render as a link. The way I can fix this would be to call a function that will verify that the message is indeed a valid url before returning the react-tiny-link object.

**[Back to top](#Pirate-Themed-Chat-App)**

## Final Remarks

Please feel free to let me know if any issues arise via the issues tab on Github. Also, if there is a big feature that would be beneficial to add, feel free to fork the repo and try to implement it or let me know so I can also attempt to add it and update the repository!

**[Back to top](#Pirate-Themed-Chat-App)**
