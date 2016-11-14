# -*- coding: utf-8 -*-
import json
import boto3

class ES(object):
    def __init__(self, ip, domain):
        self.domain = domain
        self.ip = ip
        self.es = boto3.client('es')

    def fetch_domain_config(self):
        return self.es.describe_elasticsearch_domain(DomainName=self.domain)

    def extract_access_list(self, output):
        policie = json.loads(output.get('DomainStatus').get('AccessPolicies'))

        data = policie.get('Statement')[0]['Condition']['IpAddress']['aws:SourceIp']
        data.append(self.ip)

        return policie

    def update_access_list(self, access_list):
        return self.es.update_elasticsearch_domain_config(
            DomainName=self.domain,
            AccessPolicies=json.dumps(access_list)
        )
