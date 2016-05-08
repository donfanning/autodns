#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import requests
import argparse


def create_dns_register(public_ip, private_ip, name, args):
    """Create a DNS register on Consul

    Parameters
    ----------
    public_ip: string
        Public ip address from Instance
    private_ip: string
        Private ip addresss from Instance
    name: string
        Name of the instance (from tag)
    args: string
        Arguments from script
    """
    data = {
        "Datacenter": "dc1",
        "Address": private_ip,
        "Node": name,
        "TaggedAddresses": {
            "wan": public_ip
        }
    }
    requests.put("http://{}/v1/catalog/register".format(args.consul),
                 json=data)


def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('--consul', help="Consul address", default="localhost:8500")
    args = parser.parse_args()
    ec2 = boto3.client('ec2')
    for instance in ec2.describe_instances()["Reservations"]:
        try:
            inst_obj = instance.get("Instances")[0]
            public_ip = inst_obj.get('PublicIpAddress')
            private_ip = inst_obj.get('PrivateIpAddress')
            name_tags = filter(lambda item: item.get('Key') == 'Name',
                               inst_obj.get('Tags'))
            name = ''.join(map(lambda item: item.get('Value'), name_tags))

            create_dns_register(public_ip, private_ip, name, args)
        except IndexError:
            continue

if __name__ == "__main__":
    main()
