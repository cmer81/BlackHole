# -*- coding: utf-8 -*-
import paramiko
import termios
import tty
import os
import select
import socket
import sys
import stat
import blackHole
import signal
from datetime import datetime
from loger import Loger


class SecureShellClient(object):
    """
    classdocs
    """
    def __init__(self, widget, size):
        """
        * blackHole: blackHole object
        * widget: HostTree object
        * size: size of the terminal
        """
        self.blackHole = blackHole.BlackHole.instance
        self.hostConnection = widget.hostConnectionObject
        self.widget = widget
        self.size = size
        self.userConnection = self.hostConnection.getConnectionUser(self.blackHole.data.user)
        self.sessionStartDate = datetime.now()
        self.sessionStopDate = None
        self.closed = False
        self.logFile = None
        
        try:
            paramiko.util.logging.getLogger().setLevel(30)
            try:
            #Create the Socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((self.hostConnection.host.ip, self.hostConnection.host.port))
            except Exception as e:
                exceptionMsg = "*** Connect failed: [%s] to %s" % (str(e), self.hostConnection.host.name)
                Loger.writeError(exceptionMsg)
                raise Exception(exceptionMsg)
            try:
                # Create the Transport
                t = paramiko.Transport(sock)
                try:
                    #Connect to the ssh server
                    t.start_client()
                    try:
                        t.auth_publickey(self.userConnection, self.widget.pk)
                        Loger.write("[login] user=%s to=%s as=%s sessionID=%s" % (self.blackHole.data.user.userName,
                                                                                  self.hostConnection.host.name,
                                                                                  self.userConnection,
                                                                                  self.blackHole.data.sessionID))
                    except paramiko.SSHException as e:
                        t.close()
                        sock.close()
                        Loger.writeError("%s [%s] %s " % (self.blackHole.data.user.userName,
                                                          self.hostConnection.host.name, e.message))
                        raise Exception(e)  
                    chan = t.open_session()
                    cols, rows = size
                    chan.get_pty('xterm', cols, rows)
                    chan.invoke_shell()
                    self.interactiveShell(chan)
                    chan.close()
                    t.close()
                    sock.close()    
                    self.closeLog()
                except paramiko.SSHException as e:
                    exceptionMsg = '*** SSH negotiation failed to %s.' % self.hostConnection.host.name
                    Loger.writeError(exceptionMsg)
                    t.close()
                    sock.close()
                    raise Exception(exceptionMsg)
                except Exception as e:
                    raise e
            except Exception as e:
                raise Exception(e)
        except Exception as e:
            raise Exception(e)
    
    def closeLog(self, signum=None, frame=None):
        if not self.closed:
            self.sessionStopDate = datetime.now()
            sessionDuration = round((self.sessionStopDate - self.sessionStartDate).total_seconds() / 60, 3)

            Loger.write("[logout] user=%s to=%s as=%s sessionID=%s" % (self.blackHole.data.user.userName,
                                                                                self.hostConnection.host.name,
                                                                                self.userConnection,
                                                                                self.blackHole.data.sessionID))
            self.blackHole.writeSessionLog(self.hostConnection.host,
                                           self.hostConnection.userAuthentication,
                                           self.sessionStartDate,
                                           self.sessionStopDate,
                                           sessionDuration,
                                           self.logFile)
            self.closed = True

    def interactiveShell(self, chan):
        signal.signal(signal.SIGHUP, self.closeLog)
        oldtty = termios.tcgetattr(sys.stdin)
        log = self.blackHole.data.user.logEnable
        if log:
            try:
                if os.path.isdir(os.path.join(self.blackHole.settings.log_path, self.blackHole.data.user.profile.name)):
                    logFile = "%s/%s/%s-%s-%s-%i_%s.log" % (self.blackHole.settings.log_path,
                                                            self.blackHole.data.user.profile.name,
                                                            self.blackHole.data.user.userName,
                                                            self.userConnection, 
                                                            self.hostConnection.host.name,
                                                            self.blackHole.data.sessionID,
                                                            self.sessionStartDate.strftime("%Y%m%d_%H%M%S"))
                else:
                    Loger.writeError("[ERROR] Log Path don't Exists: %s" % os.path.join(self.blackHole.settings.log_path,
                                                                                        self.blackHole.data.user.profile.name))
                    logFile = "%s/%s-%s-%s-%i_%s.log" % (self.blackHole.settings.log_path,
                                                         self.blackHole.data.user.userName,
                                                         self.userConnection,
                                                         self.hostConnection.host.name,
                                                         self.blackHole.data.sessionID,
                                                         self.sessionStartDate.strftime("%Y%m%d_%H%M%S"))
                self.logFile = logFile
                file = open(logFile, 'w')
                os.chmod(file.name, stat.S_IRUSR | stat.S_IRGRP | stat.S_IWRITE | stat.S_IWGRP | stat.S_IROTH)
            except Exception as e:
                raise Exception("Creating log File [%s]" % e)
        try:
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())
            chan.settimeout(0.0)
            if log: 
                file.write("-------------- TIME STAMP: %s --------------\n" % self.sessionStartDate.strftime("%Y-%m-%d %H:%M"))
            while True:
                r, w, e = select.select([chan, sys.stdin], [], [])
                if chan in r:
                    try:
                        x = chan.recv(1024)
                        if len(x) == 0:
                            break
                        if log:
                            try:
                                file.write(str(x).decode().replace('\r', ''))
                                file.flush()
                                os.fsync(file.fileno())
                            except:
                                file.write(str(x))
                                file.flush()
                                os.fsync(file.fileno())
                        sys.stdout.write(x)
                        sys.stdout.flush()                      
                    except socket.timeout:
                        break
                            #raise Exception(e)
                if sys.stdin in r:
                    x = os.read(sys.stdin.fileno(), 1)
                    if len(x) == 0:
                        break
                    chan.send(x)
        except:
            pass
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
            if log:
                file.close()
