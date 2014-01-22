#!/usr/bin/python


import feedparser;
import datetime;
import time;
from twitter import Twitter, OAuth;

#lqdn_en_rss_url = "http://www.laquadrature.net/en/rss.xml" ;
#lqdn_fr_rss_url = "http://www.laquadrature.net/fr/rss.xml" ;
lqdn_rp_en_rss_url = "http://www.laquadrature.net/en/press-review/feed" ;
lqdn_rp_fr_rss_url = "http://www.laquadrature.net/fr/revue-de-presse/feed" ;

#Credential for Twitter
consKey = '';
consSec = '';
token = ''
tokenSec = '';




class RSSFeed(object):

    def __init__(self, url, label):
        self.lastEntry = None;
        self.feed = None;
        self.url = url;
        self.label = label;

    def openRSS(self):
        self.feed = feedparser.parse(self.url);
        self.lastEntry = time.strptime(self.feed['entries'][0]['published']
                ,"%a, %d %b %Y %H:%M:%S +0000");
        print "Initialized RSS time : %s" %self.lastEntry;
        
    def checkForNewEntries(self):
        self.feed = feedparser.parse(self.url);
        entries = self.feed['entries'];
        i = 0;

        entry = entries[i];
        myPubliDate = time.strptime(entry['published'],"%a, %d %b %Y %H:%M:%S +0000");
#        myPubliDate = time.strptime('2014-01-22 12:00:00' , '%Y-%m-%d %H:%M:%S');

        while ((myPubliDate > self.lastEntry) and (i+1 < len(entries))) :
            print "New RSS found : %s" % entry['title'];
            self.tweetEntry(entry);
            i = i+1;
            entry = entries[i];
            myPubliDate = time.strptime(entry['published'],
                    "%a, %d %b %Y %H:%M:%S +0000");

        self.lastEntry = myPubliDate;
            
    def tweetEntry(self, entry):

        t= Twitter( auth=OAuth(token, tokenSec, consKey, consSec));
        msg ="[%s]%s - %s" % (self.label, entry['title'], entry['link']); 

        print "Twitter : %s" % (msg);
        t.statuses.update(status=msg);

    def run(self):
        self.openRSS();
        while True:
            self.checkForNewEntries();
            time.sleep(10);
            print "New check";

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


