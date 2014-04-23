rp_to_twitter
=============

send the lqdn rp to twitter


Dependencies
============

- virtualenv recommended in ve/, doit with "virtualenv ve"
- then source ve/bin/activate
- and pip install twitter feedparser


Launch Script
=============

can be launched using supervisord as follow (path is an example)


[program:rp_to_twitter]
command=./runinenv /var/www/rp/rp_to_twitter/ve python rp_to_twitter.py
directory=/var/www/rp/rp_to_twitter
user=rp
redirect_stderr=true
autostart=true
autorestart=true

