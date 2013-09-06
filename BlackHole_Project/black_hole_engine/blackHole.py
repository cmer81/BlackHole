# -*- coding: utf-8 -*-
import random
import os
import getpass
import datetime
import socket
from ConfigParser import ConfigParser
from django.core import exceptions
from django.core.management import setup_environ
from blackHoleExceptions import ErrorLoadingData, UnknownUser, FileMissing, UserDisabledTime, UserDisabled
import paramiko
import gui
from loger import Loger
import black_hole.settings
setup_environ(black_hole.settings)
from black_hole_db.models import User, PrivateKey, SessionLog


class Settings(object):
    def __init__(self, configParserObject):
        """
        BlackHole internal configuration class.
        Arguments:
        configParserObject - a config parser object, to read the configuration file.
        """
        section = 'settings'
        self.debug = configParserObject.getboolean(section, 'debug')
        self.application_path = configParserObject.get(section, 'application_path')
        self.log_path = configParserObject.get(section, 'log_path')
        self.chat_enabled = configParserObject.getboolean(section, 'chat_enabled')
        self.token_validation_enabled = configParserObject.getboolean(section, 'token_validation_enabled')
        if not os.path.isdir(self.application_path):
            raise ErrorLoadingData('Path %s does not exists' % self.application_path)
        if not os.path.isdir(self.log_path):
            raise ErrorLoadingData('Path %s does not exists' % self.log_path)


class Data(object):
    def __init__(self):
        try:
            self.user = User.objects.get(userName=getpass.getuser())
        except exceptions.ObjectDoesNotExist as e:
            raise UnknownUser(getpass.getuser())
        except Exception as e:
            raise e
        sourceInformation = os.environ.get('SSH_CLIENT')
        if sourceInformation:
            try:
                self.sourceIP = sourceInformation.split()[0]
                self.sourcePort = sourceInformation.split()[1]
            except IndexError:
                self.sourceIP = '0.0.0.0'
                self.sourcePort = 0
        else:
            self.sourceIP = '0.0.0.0'
            self.sourcePort = 0
        self.sessionID = random.randrange(100000, 999999, 1)


class BlackHole(object):
    """
    Main Class
    """
    instance = None

    def __init__(self, SETTINGS_FILE):
        """
        Creates an instance of BlackHole
        Arguments:
        SETTINGS_FILE -- Path of the settings File
        """
        self.version = "2.1"
        try:
            self.__setup(SETTINGS_FILE)
            Loger.write(self)
            if self.data.user.enable:
                if self.data.user.timeEnabled:
                    now = datetime.datetime.now().time().replace(second=0)
                    if not (self.data.user.timeFrom < now < self.data.user.timeTo):
                        raise UserDisabledTime(self.data.user)
                self.data.user.lastLogin = datetime.datetime.now()
                self.data.user.save()
            else:
                raise UserDisabled(self.data.user)
            self.blackHoleBrowser = gui.BlackHoleBrowser(self)
            BlackHole.instance = self
        except Exception as e:
            raise e

    def __str__(self):
        return "[auth] user=%s sessionID=%s from=%s:%s" % \
               (self.data.user.userName, self.data.sessionID, self.data.sourceIP, self.data.sourcePort)

    def main(self):
        self.blackHoleBrowser.main()

    def __setup(self, SETTINGS_FILE):
        """
        Load settings from settings file.
        Arguments:
        SETTINGS_FILE -- Path of the settings File
        """
        config = ConfigParser()
        try:
            config.read(SETTINGS_FILE)
            self.settings = Settings(config)
            self.data = Data()
        except IOError:
            raise FileMissing(SETTINGS_FILE)
        except Exception as e:
            raise e

    def getPrivateKey(self, user, environment):
        try:
            pk = PrivateKey.objects.get(user=user, environment=environment)
            try:
                if pk.type == 'DSA':
                    key = paramiko.DSSKey.from_private_key(pk)
                else:
                    key = paramiko.RSAKey.from_private_key(pk)
            except Exception as e:
                Loger.writeError("%s [%s]" % (user, e.message))
                return False
            return key
        except exceptions.ObjectDoesNotExist as e:
            return False

    def writeSessionLog(self, host, userIdentity, loginDate, logoutDate, sessionDuration, logFile):
        try:
            blackholeServer = socket.gethostname()
            sessionLog = SessionLog(user=self.data.user,
                                    host=host,
                                    userIdentity=userIdentity,
                                    sourceIP=self.data.sourceIP,
                                    loginDate=loginDate,
                                    logoutDate=logoutDate,
                                    sessionID=self.data.sessionID,
                                    sessionDuration=sessionDuration,
                                    blackholeServer=blackholeServer,
                                    logFile=logFile)
            sessionLog.save()
        except Exception as e:
            Loger.writeError("!!%s [%s]" % (self.data.user.userName, e))




