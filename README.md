==============================================
BlackHole: Integrated ssh security tool
==============================================
![main](http://img577.imageshack.us/img577/2091/mainwindowa.png)
![web](http://img32.imageshack.us/img32/957/indexgm.png)


<dl>
  <dt>IMPORTANT</dt>
  <dt>I've made some changes.</dd>
  <dt>I need to rewrite the manual (the install section), just use the installation script and read what it tells you to do</dt>
</dl>

What is BlackHole?
is difficult to express in a few words
It's a solution to trace users who connect to a linux/unix machine with ssh.
It was designed for an environment with many servers, its not for domestic use.
For example: When you have to grant access to many environments, like Testing, Production, QA, etc.


Basically its a curses ssh client, that can keep trace of the entire ssh session.
Is divided into two functionalities:
* User management
* Logging and statistics
* Access Control

Requirements
============

* [Django](https://www.djangoproject.com/)
* [Paramiko](http://www.lag.net/paramiko/)
* [MySQLdb](http://www.lag.net/paramiko/)
* [Urwid](http://excess.org/urwid/)
* [python-simplejson](https://github.com/simplejson/simplejson)
* [django-qsstats-magic](https://bitbucket.org/kmike/django-qsstats-magic)
* [python-dateutil](http://labix.org/python-dateutil)
* [django_extensions](https://github.com/django-extensions/django-extensions)
* libapache2-mod-wsgi (Only if you want to use apache)

License
=======

Liensed under a BSD-style license.

What it can do?
==============

The main advantage that Blackhole gives you is that you can still use generic users.
But without losing track of who is who.

![Diagram](http://img717.imageshack.us/img717/371/diagramv.jpg)

You define a user for the connection and a private key.
Then you assign that session configuration to a profile, and then all the users with that profile can login to that host.
But you now who is who, and more. 
You know what he is doing because BlackHole stores all the session activity to a log file.

And have satistics about your users
![Stats1](http://img849.imageshack.us/img849/4737/logincount.png)
![Stats2](http://img33.imageshack.us/img33/9905/sourceg.png)
![Stats3](http://img29.imageshack.us/img29/2551/statska.png)

Also download those session logs
![logs](http://img534.imageshack.us/img534/6042/logsx.png)

You can have full control of you users, by enable them or disable them.
Or enabled them only in a time range, or to a limited group of hosts.

Also they can talk to each other, with it's integrated Chat.
![chat](http://img59.imageshack.us/img59/5710/chatsgk.png)

BlackHole must run as the user shell, so the only thing that he can use is BlackHole.
I recommend to disable scp and sftp in the BlackHole server.

Installation
==============

Use the installation script. It will install all the dependencies, except the parts that you can choose, DB and web server.
For those you need to choose.
I use apache and Mysql, there are apache examples of configuration files inside.

Extras
======

BlackHole also haves some extra functionalities, that are disabled by default.
You can send a token, to ensure that the user is who he is saying he is.
* You can send it by mail

You can authenticate web users with radius, for this you need to install python-pyrad,
if you use this feature I recommend you to also authenticate ssh users with radius.



