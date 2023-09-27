# SpeakSprouts

A platform for language learners to connect with each other and practice languages by chatting. Users can create profiles and find language partners.

## Please note!
The latest version of this app is running at a friends 
server. And to automate the fetching I have merged his pull request. The merged 
code only affects the automation and not the content of the app itself. 
So please note that the merged files should not be part of my grading.
This includes the systemd folder and the main.sh file.

## Requirements for the finished project

### Profiles

A profile should include an username, known languages and language levels, (friends list).
A profile could also include a freely worded description, looking to teach and/or learn, age, profile picture and chosen color for profile.

### Functionalities

Functionalities for users:
- user can login, logout and make a new account
- user can search for other users (based on languages or usernames)
- user can start a chat with another user if they are language partners
- user can request to be another users language partner
- user can accept or deny a request from another user to be their language partner
- user can block another user
- user can add a review on a language partners profile
- user can make community posts and comment or like other peoples posts


## Current functionalities

### Profiles

- login and logout are done, registeration works but more info should be asked to make a new account
- basic own profile and other users basic profiles can be viewed by clicking a user icon
- own profile information can be edited slightly

### Language partners

- a request to a user to become language partners can be sent from the other users profile
- a user can write a message to go along the request
- if two people are already language partners the send request button won't show up
- requests sent to a user can be found in notifications page by clicking the bell icon at top-right
- user can accept or deny requests sent to them, and also view the request messages

### Chats

- user can chat only with people they are language partners with
- chats can be accessed from main page on the left side by clicking the chat icon under a username
- every chat sent gets saved to database, old chat messages can be viewed by scrolling
- dates and times that chats were sent are also showing

### Community posts

- not done


## Instructions for testing

After cloning this repo to your device, create an .env file to the root folder.
The .env file should have the following content.
```
DATABASE_URL=<databases-local-address>
SECRET_KEY=<your-secret-key>
```

### Recommendations for testing

For testing purposes I have added 10 dummy users to the database when the program is first ran.
I recommend that you first register a new account and then send a language partner
request to a dummy user by going to their profile. Then logout and login to that dummy account (username and password are the same)
 and accept the partner request by going to the notifications (bell icon in top-right).
By doing this you can test the chatting feature, since chatting is only possible with language partners.

### Commands

Run the following commands to set up:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r ./requirements.txt
```
```
psql < schema.sql
```
Run the program with:
```
flask run
```
