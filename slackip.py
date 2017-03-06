#!/usr/bin/env python
"""
## slackip.py
##
## I am behind a NAT get my global IPv4 address and write it to a slack channel
##
## https://github.com/nerby/slackIP
##
## Atanu Ghosh
## <atanu@.......>
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

    return response.status, response.reason, response.read()[:-1]

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

    print("Sucessfully wrote to slack channel")

    return True

def save_ip_address_to_file(filename, ipaddress):
    """
    Save my IP address to a file
    """

    save = open(filename, 'w')
    save.write(ipaddress)
    save.close()

def read_ip_address_from_file(filename):
    """
    Read my saved IP address from file
    """

    try:
        with open(filename, "r") as saved:
            for line in saved:
                return True, line
    except IOError:
        pass

    return False, None

USAGE =\
"""\
usage: %s
\t -h --host
\t -u --url
\t -s --save
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
        opts, _ = getopt.getopt(sys.argv[1:], "h:u:s:",
                                ["host=", "url=", "save="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)


    url = None
    host = None
    save = None

    for option, arg in opts:
        if option in ("-h", "--host"):
            host = arg
        if option in ("-u", "--url"):
            url = arg
        if option in ("-s", "--save"):
            save = arg

    status, reason, ipaddress = get_my_ip()
    if status != 200:
        print("Problem", reason, file=sys.stderr)
        return

    print("Global IP address", ipaddress)

    if not url or not host:
        print("The host and URL must be provided", file=sys.stderr)
        return

    if save:
        status, saved_ipaddress = read_ip_address_from_file(save)
        if not status:
            print("No saved IP address in", save)
            save_ip_address_to_file(save, ipaddress)
        else:
            if ipaddress != saved_ipaddress:
                print("Saved IP address does not match current IP address",
                      saved_ipaddress, save)
                save_ip_address_to_file(save, ipaddress)
            else:
                print("IP address has not changed")
                return

    write_to_slack_channel(host, url, os.uname()[1], ipaddress)

if __name__ == '__main__':
    main()
