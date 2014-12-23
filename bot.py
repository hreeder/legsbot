import logging
import sys

import config as botConfig

from twisted.internet import protocol, reactor
from twisted.words.protocols import irc

class LegsBot(irc.IRCClient):
    """A bot to provide dancer's legs"""
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        print "Connection Made"

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        print "Connection Lost, %s" % (reason, )

    def signedOn(self):
        print "Signed on as %s." % (self.nickname,)

        for channel in self.factory.config.channels:
            self.join(channel)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        print "[%s] %s: %s" % (channel, user, msg,)
        if msg == "\o/":
            if self.factory.config.replyAll or user.split("!", 1)[0] in self.factory.config.replyTo:
                self.msg(channel, " | ")
                self.msg(channel, "/ \\")

    def _get_nickname(self):
        return self.factory.config.nickname

    def _get_realname(self):
        return self.factory.config.realname

    def _get_username(self):
        return self.factory.config.username
    nickname = property(_get_nickname)
    realname = property(_get_realname)
    username = property(_get_username)


class BotFactory(protocol.ClientFactory):
    protocol = LegsBot

    def __init__(self, config):
        self.config = config


    def ClientConnectionLost(self, connector, reason):
        print "Lost Connection (%s), reconnecting." % (reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
        reactor.stop()

if __name__ == "__main__":
    print "Starting Bot"
    factory = BotFactory(botConfig)
    print "Factory Built"
    
    reactor.connectTCP(botConfig.ircServer, botConfig.ircPort, factory)
    reactor.run()
