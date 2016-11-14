#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from dns import DNS
from queue import Queue
from sg import SecurityGroup, AlreadyExists


def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument(
        '--consul', help="Consul address", default="localhost:8500"
    )
    parser.add_argument('--read', action='store_true', default=False)

    parser.add_argument('--sqs', action='store_true', default=False)
    parser.add_argument('queues', nargs='*', default=[])

    parser.add_argument('--sg_machine', default="")
    parser.add_argument('--sg_enable_ip', default="")

    args = parser.parse_args()
    if args.sg_machine and args.sg_enable_ip:
        # Enable machine IP on security group for ssh
        sg = SecurityGroup(args.sg_machine, args.sg_enable_ip)
        try:
            print(sg.add_rule())
            print("Adicionando regra de desbloqueio")
        except AlreadyExists:
            print(sg.remove_rule())
            print("Removendo regra de desbloqueio")

    elif args.sqs:
        # If --sqs is passed list queues data
        queue = Queue(args.queues)
        queue.print_data(queue.get_sqs_list())
    else:
        # Default inserting data on consul
        dns = DNS(args.consul)
        instances = dns.fetch_ec2_instances()
        if args.read:
            dns.get_dns_host(instances)
        else:
            dns.create_dns_register(args.consul, instances)

if __name__ == "__main__":
    main()
