#!/bin/env python3
import sys
import json
import requests


class NameComDNS:
    def __init__(self, domain_name, username, token):
        self.domain_name = domain_name
        self.username = username
        self.token = token

    def list_records(self):
        url = 'https://api.name.com/v4/domains/%s/records' % self.domain_name
        r = requests.get(url, auth=(self.username, self.token))

        return r.json()

    def create_record(self, data):
        url = 'https://api.name.com/v4/domains/%s/records' % self.domain_name
        r = requests.post(url, data=json.dumps(data), auth=(self.username, self.token))
        if r.status_code == 200 or r.status_code == 201:
            print(r.json())
        else:
            raise Exception('%s: %s' % (r.status_code, r.content))

    def del_record(self, record_id):
        url = 'https://api.name.com/v4/domains/%s/records/%s' % (self.domain_name, record_id)
        r = requests.delete(url, data=data, auth=(self.username, self.token))

        print(r.json())


def receive_suffix_list():
    req = requests.get('https://raw.githubusercontent.com/publicsuffix/list/master/public_suffix_list.dat')
    req.raise_for_status()

    li = req.text.split('\n')
    li = filter(lambda row: not row.startswith('//'), li)
    li = map(lambda row: row.strip(), li)
    li = filter(lambda row: row, li)
    li = map(lambda row: row[2:] if row.startswith('*.') else row, li)
    li = map(lambda row: row.encode("idna"), li)
    li = map(lambda row: row.decode("utf-8"), li)
    li = map(lambda row: row.lower(), li)

    return list(li)


def split_zone_and_host(suffix_list, domain):
    domain = domain.lower().encode("idna").decode("utf-8").lower()

    candidate = None
    for suffix in suffix_list:
        if domain.endswith(f'.{suffix}'):
            if candidate is None or len(candidate) < len(suffix):
                candidate = suffix

    if candidate:
        pos = domain[:-(1 + len(candidate))].rfind('.') + 1
        zone_name = domain[pos:]
        host_name = domain[:-1-len(zone_name)] if zone_name != domain else None
        return (host_name, zone_name)
    else:
        raise Exception("public zone suffix not found for `%s`" % domain)


if __name__ == '__main__':
    file_name, cmd, certbot_domain, certbot_validation, name_com_username, name_com_token = sys.argv

    suffix_list = receive_suffix_list()
    (host_name, zone_name) = split_zone_and_host(suffix_list, certbot_domain)
    data = {
        'domainName': zone_name,
        'host': '_acme-challenge',
        'fqdn': '_acme-challenge.%s' % zone_name,
        'type': 'TXT',
        'answer': certbot_validation,
        'ttl': 300,
    }
    if host_name is not None:
        data.update({
            'host': '_acme-challenge.%s' % host_name,
            'fqdn': '_acme-challenge.%s.%s' % (host_name, zone_name),
        })

    ncd = NameComDNS(zone_name, name_com_username, name_com_token)

    if cmd == 'add':
        ncd.create_record(data)

    elif cmd == 'clean':
        j = ncd.list_records()

        for record in j['records']:
            if record['host'] == '_acme-challenge':
                ncd.del_record(record['id'])
