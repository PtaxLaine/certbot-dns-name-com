#!/bin/env python3
import sys
import json
import requests


class NameComDNS:
    def __init__(self, domain_name):
        self.username = None # username at name.com
        self.token = None # name.com API access token
        self.domain_name = domain_name
        if self.username is None or self.token is None:
            raise Exception("Name.com API access username or token not specified")

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


if __name__ == '__main__':

    file_name, cmd, certbot_domain, certbot_validation = sys.argv

    data = {
        'domainName': 'lonelyassistant.net',
        'host': '_acme-challenge',
        'fqdn': '_acme-challenge.lonelyassistant.net',
        'type': 'TXT',
        'answer': certbot_validation,
        'ttl': 300,
    }

    ncd = NameComDNS(certbot_domain)

    if cmd == 'add':
        ncd.create_record(data)

    elif cmd == 'clean':
        j = ncd.list_records()

        for record in j['records']:
            if record['host'] == '_acme-challenge':
                ncd.del_record(record['id'])
