import requests

from dns import DNS, start_dns
from queue import Queue
from collections import namedtuple

from main import get_parser


def fake_instances():
    """ EC2 mock instances JSON describe """
    return {"Reservations": [
        {
            "Instances": [
                {
                    "PublicIpAddress": "ip1",
                    "Tags": [{"Key": "Name", "Value": "v1"}]
                }
            ]
        }
    ]}


def get_dns():
    return DNS('host')


def test_fetch_instances(monkeypatch):
    dns = get_dns()
    monkeypatch.setattr(dns.ec2, 'describe_instances', fake_instances)
    instances = dns.fetch_ec2_instances()
    assert isinstance(instances, dict)
    assert instances == {"v1": "ip1"}


def test_insert_consul(monkeypatch):
    dns = get_dns()

    def fake_put(host, json=None):
        assert host == 'http://host/v1/catalog/register'
        assert json == {'Address': 't1', 'Datacenter': 'dc1', 'Node': 'v1'}

    monkeypatch.setattr(requests, 'put', fake_put)
    result = dns.put_dns_register('host', 'v1', 't1')
    assert isinstance(result, dict)


def test_command_initial():
    parser = get_parser()
    args = parser.parse_args('consul --url host:100'.split())
    assert args.func == start_dns
    assert args.url == "host:100"
