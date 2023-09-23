# SpeakSprouts

A platform for language learners to connect with each other and practice languages by chatting. Users can create profiles and find language partners.

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

## Introductions for testing

Run the following commands to set up:
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
psql < schema.sql
```
Run the program with:
```
flask run
```
