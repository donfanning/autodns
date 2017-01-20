from queue import Queue, start_sqs
from collections import namedtuple

from main import get_parser


def mock_sqs_get_queue(monkeypatch, queue):
    def fake_queue(QueueName=None):
        assert QueueName == 'tests'
        queues = namedtuple("Queue", ["attributes"])
        queues.attributes = {
            'ApproximateNumberOfMessages': 0,
            'ApproximateNumberOfMessagesNotVisible': 0
        }
        return queues

    monkeypatch.setattr(queue.sqs, 'get_queue_by_name', fake_queue)
    return queue.get_sqs_list()


def test_list_all_queues(monkeypatch):
    queue = Queue(["tests"])

    data = mock_sqs_get_queue(monkeypatch, queue)
    assert isinstance(data, dict)
    assert data.get("queue") == ["tests"]
    assert data.get("messages") == [0]
    assert data.get("notvisible") == [0]


def test_print_queue(monkeypatch):
    queue = Queue(["tests"])
    data = mock_sqs_get_queue(monkeypatch, queue)
    output = queue.convert_to_tabulate(data)
    assert isinstance(output, unicode)


def test_command_sqs():
    parser = get_parser()
    args = parser.parse_args('sqs --queues queue1 queue2'.split())
    assert args.func == start_sqs
    assert args.queues == ['queue1', 'queue2']
