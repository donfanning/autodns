# -*- coding: utf-8 -*-
#!/usr/bin/env python
import re
import boto3
import requests
import argparse

from tabulate import tabulate
from collections import defaultdict


def get_sqs_list(sqs, queues):
    """ Get a list of queues with messages numbers """
    data = defaultdict(list)
    for arg_queue in queues:
        sqs_queue = sqs.get_queue_by_name(QueueName=arg_queue)
        data['queue'].append(arg_queue)
        data['messages'].append(sqs_queue.attributes['ApproximateNumberOfMessages'])
        data['notvisible'].append(sqs_queue.attributes['ApproximateNumberOfMessagesNotVisible'])

    print(tabulate({"Queue": data.get('queue'),
                    "Messages": data.get('messages'),
                    "NotVisible": data.get('notvisible')}))


def get_dns_host(instances):
    """ Get DNS list with PublicIpAddress """
    print(tabulate({"IP": instances.values(), "Name": instances.keys()}))


def put_dns_register(consul, name, ip):
    data = {"Datacenter": "dc1", "Address": ip, "Node": name}
    requests.put("http://{}/v1/catalog/register".format(consul), json=data)
    return data


def create_dns_register(consul, instances):
    """Create a DNS register on Consul"""
    for name, ip in instances.iteritems():
        print(put_dns_register(consul, name, ip))


def main():
    """ Apply the DNS creation on all instance of EC2 """
    parser = argparse.ArgumentParser("")
    parser.add_argument('--consul', help="Consul address", default="localhost:8500")
    parser.add_argument('--read', action='store_true')
    parser.add_argument('--sqs', action='store_true')
    parser.add_argument('queues', nargs='*')
    args, ec2 = parser.parse_args(), boto3.client('ec2')

    instances = {}
    for instance in ec2.describe_instances()["Reservations"]:
        try:
            # Instance should be a key/value of EC2 Name vs. PublicIP
            inst_obj = instance.get("Instances")[0]
            public_ip = inst_obj.get('PublicIpAddress')
            name_tags = filter(lambda item: item.get('Key') == 'Name', inst_obj.get('Tags'))
            name = ''.join(map(lambda item: item.get('Value'), name_tags))
            instances[name] = public_ip
        except IndexError:
            continue

    if args.read:
        get_dns_host(instances)
    elif args.sqs:
        get_sqs_list(boto3.resource('sqs'), args.queues)
    else:
        create_dns_register(args.consul, instances)

if __name__ == "__main__":
    main()
