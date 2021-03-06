# -*- coding: utf-8 -*-
import boto3

from collections import defaultdict
from tabulate import tabulate


def start_sqs(args):
    queue = Queue(args.queues)
    output = queue.convert_to_tabulate(queue.get_sqs_list())
    print(output)


class Queue(object):
    def __init__(self, queues):
        self.sqs = boto3.resource('sqs')
        self.queues = queues

    def get_sqs_list(self):
        """ Get a list of queues with messages numbers """
        data = defaultdict(list)
        for arg_queue in self.queues:
            sqs_queue = self.sqs.get_queue_by_name(QueueName=arg_queue)
            data['queue'].append(arg_queue)
            data['messages'].append(
                sqs_queue.attributes['ApproximateNumberOfMessages']
            )
            data['notvisible'].append(
                sqs_queue.attributes['ApproximateNumberOfMessagesNotVisible']
            )
        return data

    def convert_to_tabulate(self, data):
        """ Print queue list on tabulate """
        return tabulate(
            {"Queue": data.get('queue'), "Messages": data.get('messages'),
             "NotVisible": data.get('notvisible')}
        )
