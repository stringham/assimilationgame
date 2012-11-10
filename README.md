assimilation2
=============

Assimilation with Django

Setting Up A Development Environment
------------------------------------

After checking out the git repo you will need to open a command line terminal 
and go to the directory: `<project_root>/assimilation/static/js`

From there you will need to checkout the Google Closure Library (requires 
[Subversion](http://subversion.apache.org/)) with the following command:

`svn checkout http://closure-library.googlecode.com/svn/trunk/ closure`

Afterwards you should have the goog directory at: `<project_root>/assimilation/static/js/closure/closure/goog`

Then you'll need to edit `<project_root>/game/settings.py` to have the correct path in the `ROOT` variable definition.

Next you need to create a local database on your system, to do this go to `<project_root>/` and run the command `python manage.py syncdb`

To run the server type `python manage.py runserver`!
