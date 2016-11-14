# -*- coding: utf-8 -*-
import boto3
import requests

from tabulate import tabulate
from collections import defaultdict


class DNS(object):
    def __init__(self, host_consul=None):
        assert host_consul
        self.host_consul = host_consul
        self.ec2 = boto3.client('ec2')

    def put_dns_register(self, consul, name, ip):
        """ Put DNS on Consul via API """
        data = {"Datacenter": "dc1", "Address": ip, "Node": name}
        requests.put("http://{}/v1/catalog/register".format(consul), json=data)
        return data

    def create_dns_register(self, consul, instances):
        """ Insert instances on Consul """
        for name, ip in instances.iteritems():
            print(self.put_dns_register(consul, name, ip))

    def get_dns_host(self, instances):
        """ Get DNS list with PublicIpAddress """
        print(tabulate({"IP": instances.values(), "Name": instances.keys()}))

    def fetch_ec2_instances(self):
        """ Fetch EC2 instances data """
        instances = {}
        # Instance should be a key/value of EC2 Name vs. PublicIP
        for instance in self.ec2.describe_instances()["Reservations"]:
            try:
                inst_obj = instance.get("Instances")[0]
                public_ip = inst_obj.get('PublicIpAddress')
                name_tags = filter(
                    lambda item: item.get('Key') == 'Name',
                    inst_obj.get('Tags')
                )
                name = ''.join(map(lambda item: item.get('Value'), name_tags))
                instances[name] = public_ip
            except IndexError:
                continue
        return instances
