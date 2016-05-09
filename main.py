#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import requests
import argparse


def create_dns_register(public_ip, name, args):
    """Create a DNS register on Consul

    Parameters
    ----------
    public_ip: string
        Public ip address from Instance
    name: string
        Name of the instance (from tag)
    args: string
        Arguments from script
    """
    data = {
        "Datacenter": "dc1",
        "Address": public_ip,
        "Node": name,
    }
    requests.put("http://{}/v1/catalog/register".format(args.consul),
                 json=data)


def main():
    """ Apply the DNS creation on all instance of EC2 """

    parser = argparse.ArgumentParser("")
    parser.add_argument('--consul', help="Consul address", default="localhost:8500")
    args = parser.parse_args()
    ec2 = boto3.client('ec2')
    for instance in ec2.describe_instances()["Reservations"]:
        try:
            inst_obj = instance.get("Instances")[0]
            public_ip = inst_obj.get('PublicIpAddress')
            name_tags = filter(lambda item: item.get('Key') == 'Name',
                               inst_obj.get('Tags'))
            name = ''.join(map(lambda item: item.get('Value'), name_tags))
            create_dns_register(public_ip, name, args)
        except IndexError:
            continue

if __name__ == "__main__":
    main()
