# abuseban
Ban IPs abusing system services

## Description
Currently script searches for failed login attempts in `/var/log/auth.log` (sshd) and `/varlog/mail.log` (postfix/saslauthd). Found failed login attempts are counted per abuser IP. Once threshold is reached script uses `iptables -A INPUT -s <IP> -j DROP` to block that IP.

### Successfully tested on
- Debian 8

## Usage

`python3 abuseban.py`
