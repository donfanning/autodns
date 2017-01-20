from es import ES, start_es

from main import get_parser


# def mock_sqs_get_queue(monkeypatch, queue):
#     def fake_queue(QueueName=None):
#         assert QueueName == 'tests'
#         queues = namedtuple("Queue", ["attributes"])
#         queues.attributes = {
#             'ApproximateNumberOfMessages': 0,
#             'ApproximateNumberOfMessagesNotVisible': 0
#         }
#         return queues

#     monkeypatch.setattr(queue.sqs, 'get_queue_by_name', fake_queue)
#     return queue.get_sqs_list()


# def test_list_all_queues(monkeypatch):
#     queue = Queue(["tests"])

#     data = mock_sqs_get_queue(monkeypatch, queue)
#     assert isinstance(data, dict)
#     assert data.get("queue") == ["tests"]
#     assert data.get("messages") == [0]
#     assert data.get("notvisible") == [0]
#
def fake_es_describe(DomainName=''):
    assert DomainName == 'domain'
    return {}


def test_fetch_domain(monkeypatch):
    es = ES('ip', 'domain')

    monkeypatch.setattr(es.es, 'describe_elasticsearch_domain',
                        fake_es_describe)

    config = es.fetch_config()
    assert isinstance(config, dict)


def test_extract_access_list(monkeypatch):
    es = ES('192.168.0.2/32', 'domain')
    data = {
        "DomainStatus": {
            "AccessPolicies": '{"Statement":[{"Condition":{"IpAddress":{"aws:SourceIp":["192.168.0.1/32"]}}}]}'
        }
    }
    config, ips = es.append_ip_acl(data)
    assert ips == ["192.168.0.1/32", "192.168.0.2/32"]
    assert isinstance(config, dict)


def test_command_sqs():
    parser = get_parser()
    args = parser.parse_args('es --ip ip_add --domain foo'.split())
    assert args.func == start_es
    assert args.ip == 'ip_add'
    assert args.domain == 'foo'
