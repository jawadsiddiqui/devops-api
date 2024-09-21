import socket
import re


def get_ipv4_for_domain(domain):
    return [ip for ip in socket.gethostbyname_ex(domain)[2] if '.' in ip]


def is_valid_ipv4(ip):
    pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    return pattern.match(ip) is not None
