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

    def openRSS(self):
        self.feed = feedparser.parse(self.url);
        self.lastEntry = self.feed['entries'][0]['title']

        print "Initialized RSS : %s" %self.lastEntry;
        
    def checkForNewEntries(self):

        print "Check for New entries, last entry tweeted was : %s" % self.lastEntry  
        self.feed = feedparser.parse(self.url);
        entries = self.feed['entries'];
        i = 0;

        try:
            entry = entries[i];
        except:
            print "Can't open the first entry ... ";
            return;

        entryTitle = entry['title'];

        while ((entryTitle != self.lastEntry) and (i+1 < len(entries))) :
            print "New RSS found : %s" % entry['title'];
            self.tweetEntry(entry);
            i = i+1;
            try :
                entry = entries[i];
            except:
                print "Can't get the entry %d on %d" % (i, len(entries));
                return;
            entryTitle = entry['title']

        self.lastEntry = entryTitle;
            
    def tweetEntry(self, entry):

        t= Twitter( auth=OAuth(config.TOKEN,config.TOKENSEC, config.CONSKEY, config.CONSSEC));
        msg ="[%s]%s - %s" % (self.label, entry['title'], entry['link']); 

        print "Twitter : %s" % (msg);
        try:
            t.statuses.update(status=msg);
        except:
            print "Error while twitting : %s" % msg;

    def run(self):
        self.openRSS();
        while True:
            self.checkForNewEntries();
            time.sleep(180);
            //print "New check";

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


