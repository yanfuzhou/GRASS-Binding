#GRASS Python binding example deployed behind Gunicorn using Gevent workers

##How to run this example?

###Step 1:

1) `virtualenvwrapper` should be installed into the same global site-packages area where virtualenv is installed.

```bash
$ pip install virtualenvwrapper
```

2) Add three lines to your shell startup file (.bashrc, .profile, .bash_profile, etc.)

```bash
$ nano ~/.bash_profile
```

```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

3) After editing it, reload the startup file
```bash
$ source ~/.bash_profile
```
  
Refer: http://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation  

###Step 2:

1) Create virtual environment

```bash
$ cd grass_binding/
$ virtualenv venv
$ source venv/bin/activate
$ add2virtualenv /usr/local/Cellar/grass7/7.2.0/grass-base/etc/python
```

*Note: python binding for grass on mac `/usr/local/Cellar/grass7/7.2.0/grass-base/etc/python`, path on different OS varies  

2) Install packages

```bash
$ pip install Flask
$ pip install flask-restplus
$ pip install gunicorn
$ pip install gevent
```

Refer:  
1) http://sourabhbajaj.com/mac-setup/Python/virtualenv.html  
2) http://stackoverflow.com/questions/10738919/how-do-i-add-a-path-to-pythonpath-in-virtualenv  

###Step 3:

Run in terminal (before this, make sure `$ source venv/bin/activate`):

```bash
$ ./gunicorn.sh
```

Other refers:  
https://grasswiki.osgeo.org/wiki/Working_with_GRASS_without_starting_it_explicitly  
