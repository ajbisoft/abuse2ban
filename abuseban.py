#!/usr/bin/python3

import re
import os

# Set failure threshold for ban
ban_threshold = 10

# Log search function
def log_search(log_file, regex, cut_start, cut_stop, cut_start_offset = 1):
    with open(log_file, "r") as file:
        for line in file:
            if (regex.search(line)):
                ip = line.split(cut_start)[cut_start_offset].split(cut_stop)[0]
                if ip not in badips:
                    badips[ip] = 1
                else:
                    badips[ip] += 1

# Main code
badips = {}

# Search mail.log for failed SASL login attempts
log_file = "/var/log/mail.log"
regex = re.compile(".*]: SASL.*authentication failed.*")
log_search(log_file, regex, '[', ']', 2)

# Search auth.log for failed ssh login attempts
log_file = "/var/log/auth.log"
regex = re.compile(".*sshd.*Failed password.*")
log_search(log_file, regex, 'from ', ' port')

# Flush blocked IPs
print("Flushing blocked IP list...", end = '')
if os.system("iptables -F INPUT") == 0:
    print("OK!")
else:
    print("failed!")

# Ban IPs with auth failures over given threshold
for ip, fail_count in sorted(badips.items()):
    if fail_count >= ban_threshold:
        print("IP {} failed auth {} times. Blocking... ".format(ip, fail_count), end='')
        if os.system("iptables -A INPUT -s {}/32 -j DROP".format(ip)) == 0:
            print("OK!")
        else:
            print("failed!")
