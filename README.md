assimilation2
=============

Assimilation with Django

Future Plans
------------

- Create boards with black (neutral) spaces

- Implement AI, play against the computer

- Allow more than two players per game (up to 6?)

- Implement animation when a user takes a turn

- Play back a game turn by turn, time lapse?

- Allow AI's to play against each other

- Automatically end game when nobody else can win

Deploying to apfog
------------------
`af login`

`af update assimilation-game`

Setting Up A Development Environment
------------------------------------

After checking out the git repo you will need to open a command line terminal 
and go to the directory: `<project_root>/assimilation/static/js`

From there you will need to checkout the Google Closure Library (requires 
[Subversion](http://subversion.apache.org/)) with the following command:

`svn checkout http://closure-library.googlecode.com/svn/trunk/ closure`

Afterwards you should have the goog directory at: `<project_root>/assimilation/static/js/closure/closure/goog`

Next you need to create a local database on your system, to do this go to `<project_root>/` and run the command `python manage.py syncdb`


Makefile
--------
There is a makefile that you can use to compile from .less to .css, and to minify and optimize the javascript.

To build the javascript type the command `make js`

To build the css use `make css`

To run the webserver simply use `make run`