# -*- coding: utf-8 -*-
import requests

from dns import DNS
from queue import Queue
from collections import namedtuple


def get_dns():
    dns = DNS('host')
    assert dns.host_consul == 'host'
    return dns


def fake_instances():
    return {"Reservations": [
        {
            "Instances": [
                {
                    "PublicIpAddress": "ip1",
                    "Tags": [
                       {
                           "Key": "Name",
                           "Value": "v1"
                       }
                    ]
                }
            ]
        }
    ]}


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


def test_list_all_queues(monkeypatch):
    queue = Queue(["tests"])

    def fake_queue(QueueName=None):
        assert QueueName == 'tests'
        queues = namedtuple("Queue", ["attributes"])
        queues.attributes = {
            'ApproximateNumberOfMessages': 0,
            'ApproximateNumberOfMessagesNotVisible': 0
        }
        return queues

    monkeypatch.setattr(queue.sqs, 'get_queue_by_name', fake_queue)
    data = queue.get_sqs_list()
    assert isinstance(data, dict)
    assert data.get("queue") == ["tests"]
    assert data.get("messages") == [0]
    assert data.get("notvisible") == [0]
