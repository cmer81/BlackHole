#!/bin/bash

if [ "`whoami` != "root" ];then
    echo "Must run as root"
    exit 1
fi

PIP=`which pip`

if [ "$PIP" != "" ];then
    BLACKHOLE_PATH="/opt/BackHole"
    export INSTALL="$PIP install --upgrade"
    echo "Installing dependencies..."
    $INSTALL django
    $INSTALL paramiko
    $INSTALL urwid
    $INSTALL simplejson
    $INSTALL django-qsstats-magic
    $INSTALL python-dateutil
    echo "READ: The installer wont install MySQLdb, because maybe you want to use some other engine. If you want to use Mysql, Install MySQLdb!!"

    mkdir $BLACKHOLE_PATH
    groupadd blackhole
    cp -rf apache $BLACKHOLE_PATH
    cp -rf blackhole $BLACKHOLE_PATH
    cp launcher/* $BLACKHOLE_PATH

    echo "Ready!! Now you must configure the logs path in $BLACKHOLE_PATH/blackhole.config. Make shure that the group 'blackhole' has write permissions!!!"
    echo "Now: configure the DB information (db/user/password) in $BLACKHOLE_PATH/blackhole/black_hole/settings.py"
    echo "Run (to create the tables): $BLACKHOLE_PATH/blackhole/manage.py syncdb"
    echo "Run (the lead the initial configuration: $BLACKHOLE_PATH/blackhole/manage.py initial_setup"
    echo "Configure the web server, the example configuration is in $BLACKHOLE_PATH/apache/. You can use the blackhole.conf.example for it!!"
    echo "Now you are ready to run it, just load your configurations in the web!!"
    echo "REMEMBER to set $BLACKHOLE_PATH/blackhole_launcher.py as the users shell!!"

else
    echo "You need pip in you $PATH"
    exit 1
fi
