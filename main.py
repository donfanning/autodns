# -*- coding: utf-8 -*-
#!/usr/bin/env python
import boto3
import requests
import argparse


def get_dns_host(instances):
    """ Get DNS list with PublicIpAddress """
    from tabulate import tabulate
    print(tabulate({"IP": instances.values(), "Name": instances.keys()}))


def create_dns_register(consul, instances):
    """Create a DNS register on Consul"""
    for key, value in instances.iteritems():
        data = {"Datacenter": "dc1", "Address": value, "Node": key}
        requests.put("http://{}/v1/catalog/register".format(consul), json=data)


def main():
    """ Apply the DNS creation on all instance of EC2 """

    parser = argparse.ArgumentParser("")
    parser.add_argument('--consul', help="Consul address", default="localhost:8500")
    parser.add_argument('--read', action='store_true')
    args, ec2 = parser.parse_args(), boto3.client('ec2')

    instances = {}
    for instance in ec2.describe_instances()["Reservations"]:
        try:
            inst_obj = instance.get("Instances")[0]
            public_ip = inst_obj.get('PublicIpAddress')
            name_tags = filter(lambda item: item.get('Key') == 'Name', inst_obj.get('Tags'))
            name = ''.join(map(lambda item: item.get('Value'), name_tags))
            instances[name] = public_ip
        except IndexError:
            continue

    if args.read:
        get_dns_host(instances)
    else:
        create_dns_register(args.consul, instances)

if __name__ == "__main__":
    main()
