#!/bin/bash

PIP=`which pip`

if [ "$PIP" != "" ];then
    export INSTALL="$PIP install --upgrade"
    echo "Installing dependencies..."
    $INSTALL django
    $INSTALL paramiko
    $INSTALL urwid
    $INSTALL simplejson
    $INSTALL django-qsstats-magic
    $INSTALL python-dateutil
    echo "READ: The installer wont install MySQLdb, because maybe you want to use some other engine. If you want to use Mysql, Install MySQLdb!!"
else
    echo "You need pip in you $PATH"
    exit 1
fi
