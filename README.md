# twitter
Twitter-like project with google app engine and python

## What is the project about ?

This is an acadmic project consisting in re-creating a minimalistic version of Twitter. </br>
It is currently in development.

## The repository

The *app.yaml* descibes where is the starting point of the program :

```{yaml}
-url: /.*
 script: lib.main.app
```
</br>

The file *main.py* in the lib folder contains all the routing of the app.

*static* contains all the files that are neither code, nor html template (anything that won't change at all).</br>
*lib* contains the code itself and the html templates
- All the handlers for each endpoints are in lib
- The folder crud contains the classes to access the data store, and models for the users and tweets

### _TODO_

- add a user's tweets in its timeline
- allow a user to have a short description on its profile
- allow a user to edit its tweets

- refactor the searchEngine handler with its own crud class
- refactor opperations linked to tweets in a tweet_CRUD class
- turn the crud classes into static class ?
