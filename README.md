# SpeakSprouts - a language learning community

A platform for language learners to connect with each other and practice languages by chatting and interacting with community posts. Users can create profiles and find language partners.

- [Please Note](#please-note)
- [Current Functionalities](#current-functionalities)
- [Known Issues](#known-issues)
- [Instructions for Testing](#instructions-for-testing)

### Please note
The latest version of this app is running at a friends 
server. And to automate the fetching I have merged his pull request. The merged 
code only affects the automation and not the content of the app itself. 
So please note that the merged files should not be part of my grading.
You can view all of these changes [here](https://github.com/Savones/SpeakSprouts/pull/1).

## Current functionalities

### Profiles

- user can login, logout, make a new account and delete their account
- user can edit their profile by changing their profile picture, bio and the list of languages they know and how well they know them
- a profile includes the community posts a user has made
- user can view other peoples profiles
- user can search for other users from the home page

### Language partners

- a request to another user to become language partners can be sent from the other users profile
- a user can write a message to go along with the request
- if two people are already language partners the "send request" button won't show up, instead the "remove" partner and "open chat" will
- partner connection can be removed by clicking the remove button in their profile
- requests sent to a user can be found in notifications page by clicking the bell icon at top-right
- user can accept or deny requests sent to them, and also view the request messages
- accepting a request opens a chat between the language partners

### Chats

- user can chat only with people they are language partners with
- chats can be accessed from on the left side of the home page by clicking the chat icon under an username, or from another users profile
- every message sent gets saved to database, old chat messages can be viewed by scrolling
- dates and times the chats were sent are displayd on the chat
- the latest message sent in every chat is displayed on the home page
- the order of chats is that the latest chat interaction is at the top, also the amount of unread messages is displayed for each chat

### Community posts

- all posts can be viewed from the home page and clicked open with the "view post" button
- a new post can be made by clicking the add post button in home page
- users can leave comments under posts
- users community posts are displayed on their profile

## Known issues

- When editing your profile if you first choose a profile image and then change language related information, the new profile image turns back to the old one. This is due to a poor editing page design and the lack of time to change it. This bug can be avoided by either saving the image before changing the language options or by first changing the languages and then the image.

## Instructions for testing

After cloning this repo to your device, create an .env file to the root folder.
The .env file should have the following content.
```
DATABASE_URL=<databases-local-address>
SECRET_KEY=<your-secret-key>
```

### Recommendations for testing

When the program is first ran the database is populated with 20 fake users to make testing easier.
I recommend that you first register a new account and then send a language partner
request to a fake user by going to their profile. Then logout and login to that fake account (username and password are the same)
 and accept the partner request by going to the notifications (bell icon in top-right).
By doing this you are able to test the chatting feature, since chatting is only possible with language partners.

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
## Expansion ideas

- Searching people based on languages
- More advanced community post features, for example ability to like posts and comments, getting notifications when post is commented on, answering directly to a specific comment etc.
- Ability to block people, delete messages and posts/comments
