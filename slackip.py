#!/usr/bin/env python
"""
## slackip.py
##
## I am behind a NAT get my global IPv4 address and write it to a slack channel
##
## https://github.com/nerby/slackIP
##
## Atanu Ghosh
## <atanu@acm.org>
## 2017-03-05
"""
from __future__ import print_function

import getopt
import httplib
import os
import sys

IPHOST = "ipinfo.io"
CHANNEL = """
{"channel": "#pandabot",
"username": "webhookbot",
"text": "IP address of host %s is %s",
"icon_emoji": ":ghost:"}
"""

def get_my_ip():
    """
    Get my IPv4 external address
    """

    conn = httplib.HTTPConnection(IPHOST)
    conn.request("GET", "/ip")
    response = conn.getresponse()

    return response.status, response.reason, response.read()

def write_to_slack_channel(host, url, hostname, ipaddress):
    """
    Write to slack channel

curl -X POST --data-urlencode 'payload={"channel": "#pandabot", "username": "webhookbot", "text": "This is posted to #pandabot and comes from a bot named webhookbot.", "icon_emoji": ":ghost:"}' https://hooks.slack.com/services/??? # pylint: disable=locally-disabled, line-too-long
    """

    conn = httplib.HTTPSConnection(host)
    conn.request("POST", url, CHANNEL % (hostname, ipaddress))
    response = conn.getresponse()
    ret = response.read()
    conn.close()

    if response.reason != "OK":
        print(response.reason, ret, file=sys.stderr)
        return False

    return True

USAGE =\
"""\
usage: %s
\t -h --host
\t -u --url
"""

def main():
    """
    Main function
    """

    def usage():
        """
        Usage message
        """
        print(USAGE % sys.argv[0], end='', file=sys.stderr)

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "h:u:",
                                ["host=", "url="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)


    url = None
    host = None

    for option, arg in opts:
        if option in ("-h", "--host"):
            host = arg
        if option in ("-u", "--url"):
            url = arg

    if not url or not host:
        print("The host and URL must be provided", file=sys.stderr)
        return

    status, reason, ipaddress = get_my_ip()
    if status != 200:
        print("Problem", reason, file=sys.stderr)
        return

    print(ipaddress)

    write_to_slack_channel(host, url, os.uname()[1], ipaddress)

if __name__ == '__main__':
    main()
