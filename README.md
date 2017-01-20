Consul Filler
===

You can fill consul with IPs from your AWS account, it fetches the Tag name and the public ip address to do it.

How to use
---

Update Consul with IP address and tag names

$ python main.py consul --url localhost:8500


BONUS
===

Listing SQS
---

$ python main.py sqs --queues queue1 queue2 queue3


Updating ElasticSearch IP ACL
---

$ python main.py es --ip 192.168.0.2 --domain elasticsearch
