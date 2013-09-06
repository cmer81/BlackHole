# -*- coding: utf-8 -*-
import os
import urwid
import language
from emailSender import EmailSender
from loger import Loger


class TokenValidationWindow(object):
    def __init__(self, data):
        self.token = os.urandom(4).encode('hex')
        self._palette = [('message', 'black', 'dark cyan'),
                         ('alert', 'dark red', 'black'),
                         ('bg', 'black', 'black'),]
        self.message = urwid.Text(_(u"Enter the Token for the sessionID: %s") % data.sessionID, align='center')
        self.response = urwid.Edit(u"", align='center')
        self.alert = urwid.Text(u"", align='center')
        try:
            EmailSender(data.user, self.token, data.sessionID)
        except Exception as e:
            Loger.writeError("Error sending eMail Token SMS to %s [%s" % (data.user.email, e))
            self.alert.set_text(u"%s" % e)

    def unhandled_input(self, input):
        if input == 'enter':
            if self.response.edit_text != '':
                if self.response.edit_text == self.token:
                    raise urwid.ExitMainLoop()
                else:
                    token = self.response.edit_text
                    self.response.edit_text = u""
                    self.alert.set_text(_(u"Token Invalid [%s]!!") % token)
                    
            else:
                self.alert.set_text(_(u"You must enter the Token!!"))

    def update_response(self, edit, new_edit_text):
        self.alert.set_text(u"")
        
    def main(self):
        self.ui = urwid.raw_display.Screen()
        self.ui.register_palette(self._palette)
        
        pile = urwid.Pile([urwid.AttrMap(urwid.Divider(), 'message'),
                          urwid.AttrMap(self.message, 'message'),
                          urwid.AttrMap(self.response, 'message'),
                          urwid.AttrMap(urwid.Divider(), 'message'),
                          urwid.AttrMap(self.alert, 'alert')])
        map = urwid.AttrMap(urwid.Filler(pile), 'bg')
        urwid.connect_signal(self.response, 'change', self.update_response)
        loop = urwid.MainLoop(map, self._palette, handle_mouse=False,unhandled_input=self.unhandled_input)
        loop.run()
