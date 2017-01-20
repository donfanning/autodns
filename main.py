#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from dns import start_dns
from queue import start_sqs
from es import start_es


def get_parser():
    parser = argparse.ArgumentParser('')

    # Subcommands
    subparsers = parser.add_subparsers(help='Mgmt commands')

    # Consul namespace
    parser_consul = subparsers.add_parser('consul')
    parser_consul.add_argument('--url', help="Consul address",
                               default="localhost:8500")
    parser_consul.set_defaults(func=start_dns)

    # SQS namespace
    parser_sqs = subparsers.add_parser('sqs')
    parser_sqs.add_argument('--queues', nargs='*', help="SQS Queues", default=[])
    parser_sqs.set_defaults(func=start_sqs)

    # Elasticsearch namespace
    parser_es = subparsers.add_parser('es')
    parser_es.add_argument('--ip', help="ES IP", default="")
    parser_es.add_argument('--domain', help="ES Domain", default="")
    parser_es.set_defaults(func=start_es)
    return parser


def main():
    # Calls default namespace for subcommands
    args = get_parser().parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
