#!/usr/bin/python


import feedparser;
import datetime;
import time;
from twitter import Twitter, OAuth;
import config

#lqdn_en_rss_url = "http://www.laquadrature.net/en/rss.xml" ;
#lqdn_fr_rss_url = "http://www.laquadrature.net/fr/rss.xml" ;
lqdn_rp_en_rss_url = "http://www.laquadrature.net/en/press-review/feed" ;
lqdn_rp_fr_rss_url = "http://www.laquadrature.net/fr/revue-de-presse/feed" ;


class RSSFeed(object):

    def __init__(self, url, label):
        self.lastEntry = None;
        self.feed = None;
        self.url = url;
        self.label = label;
        self.logFile = None;

    def log(self, message):
        logMessage =  "%s - %s \n" %(time.asctime(), message)
        print logMessage
        self.logFile.write(logMessage.encode('utf-8'))

    def openRSS(self):
        self.feed = feedparser.parse(self.url);
        self.lastEntry = self.feed['entries'][0]['title']
        self.logFile = open('rp_to_twitter.log', 'w+', 1)

    def checkForNewEntries(self):

        self.log("[%s] Check for New entries, last entry tweeted was : %s" %(self.label,  self.lastEntry))
        #print "[%s] Check for New entries, last entry tweeted was : %s" %(self.label,  self.lastEntry)
        #self.logFile("[%s] Check for New entries, last entry tweeted was : %s" %(self.label,  self.lastEntry)
        self.feed = feedparser.parse(self.url);
        entries = self.feed['entries'];
        i = 0;

        try:
            entry = entries[i];
        except:
            self.log( "[%s] Can't open the first entry ... " % (self.label))
            #print "[%s] Can't open the first entry ... " % (self.label);
            return;

        entryTitle = entry['title'];

        while ((entryTitle != self.lastEntry) and (i+1 < len(entries))) :
            self.log( "[%s] New RSS found : %s" % (self.label, entry['title']))
            #print "[%s] New RSS found : %s" % (self.label, entry['title']);
            self.tweetEntry(entry);
            i = i+1;
            try :
                entry = entries[i];
            except:
                self.log( "[%s] Can't get the entry %d on %d" % (self.label, i, len(entries)))
                #print "[%s] Can't get the entry %d on %d" % (self.label, i, len(entries));
                return;
            entryTitle = entry['title']
        self.lastEntry = entries[0]['title']
            
    def tweetEntry(self, entry):

        t= Twitter( auth=OAuth(config.TOKEN,config.TOKENSEC, config.CONSKEY, config.CONSSEC));
        msg ="[%s]%s - %s" % (self.label, entry['title'], entry['link']); 

        self.log( "Twitter : %s" % (msg))
        #print "Twitter : %s" % (msg);
        try:
            t.statuses.update(status=msg);
        except:
            self.log( "Error while twitting : %s" % msg)
            #print "Error while twitting : %s" % msg;

    def run(self):
        self.openRSS();
        while True:
            self.checkForNewEntries();
            time.sleep(180);

#####################################################################################



myFeed = RSSFeed(lqdn_rp_en_rss_url, 'en');
myFeed.openRSS();

myFeedFr = RSSFeed(lqdn_rp_fr_rss_url, 'fr');
myFeedFr.openRSS();

while True:
    myFeed.checkForNewEntries();
    myFeedFr.checkForNewEntries();
    time.sleep(180);
    print "New check after 3 minutes";


