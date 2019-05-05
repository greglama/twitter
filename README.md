# twitter
Twitter-like project with google app engine and python

## What is the project about ?

This is an acadmic project consisting in a minimalistic version of Twitter. </br>
It is currently in development.

## The repository

The *app.yaml* descibes where is the starting point of the program :

```{yaml}
-url: /.*
 script: main.app
```
To start the server open a terminal and place yourself in the repository.</br>
Then run `dev_appserver.py app.yaml` (you will need google SDK to be able to run this).</br>
You can download it here: https://cloud.google.com/appengine/docs/standard/python/download
</br>

The file *main.py* contains all the routing of the app.

*static* contains all the files that are neither code, nor html template (anything that won't change at all, so just CSS here).</br>
*lib* contains the code itself and the html templates
- All the handlers for each endpoints are in lib
- The folder crud contains the classes to access the data store, and the models for the users and tweets