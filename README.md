# slackIP - https://github.com/nerby/slackIP
Find global IP address of a host and post it to a slack channel

The problem your home is connected to the Internet behind a NAT,
your global IP address may change. Get your global IP address and
if it changes write the info to a slack channel.

Find the IP address using this cool opendns feature:
dig +short myip.opendns.com @resolver1.opendns.com

Write to the slack channel using Incoming WebHooks.

Unconditionally write IP address to slack channel
thud$ ./slackip.py -h hooks.slack.com -u /services/???

Save previous runs in a file if the value in the file doesn't change
don't write to slack channel
thud$ ./slackip.py -h hooks.slack.com -u /services/??? -s /tmp/myip
