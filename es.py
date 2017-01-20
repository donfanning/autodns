# -*- coding: utf-8 -*-
import json
import boto3


def start_es(args):
    if not args.ip or not args.domain:
        raise Exception("Wrong parameters")
    es = ES(args.ip, args.domain)
    config, ips = es.append_ip_acl(es.fetch_config())
    print(es.update_access_list(config))


class ES(object):
    def __init__(self, ip, domain):
        self.domain = domain
        self.ip = ip
        self.es = boto3.client('es')

    def fetch_config(self):
        return self.es.describe_elasticsearch_domain(DomainName=self.domain)

    def append_ip_acl(self, data):
        """ Append the IP as last item of ACL """
        try:
            options = data.get('DomainStatus').get('AccessPolicies')
            policy = json.loads(options)
        except:
            return {}, []
        ips = policy['Statement'][0]['Condition']['IpAddress']['aws:SourceIp']
        ips.append(self.ip)
        return policy, ips

    def update_access_list(self, access_list):
        if access_list:
            return self.es.update_elasticsearch_domain_config(
                DomainName=self.domain,
                AccessPolicies=json.dumps(access_list)
            )
