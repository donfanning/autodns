#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import botocore


class AlreadyExists(botocore.exceptions.ClientError):
    def __init__(self, value):
        self.value = value


class SecurityGroup(object):

    def __init__(self, instance, address):
        """ Instance enables SSH address on its SG """
        self.instance = instance
        self.address = address
        self.ec2 = boto3.client("ec2")

    def get_security_group(self):
        """ Get security group data for an instance """
        instance = self.ec2.describe_instances(
            Filters=[{"Name": "tag-value", "Values": [self.instance]}]
        )
        try:
            output = [res.get("Instances")[0].get('SecurityGroups')[0]
                      for res in instance.get('Reservations')][0]
        except IndexError:
            output = {}
        return output

    def add_rule(self):
        sg = self.get_security_group()
        try:
            return self.ec2.authorize_security_group_ingress(
                GroupId=sg.get("GroupId"), IpProtocol="tcp",
                FromPort=22, ToPort=22,
                CidrIp="{}/32".format(self.address)
            )
        except botocore.exceptions.ClientError:
            raise AlreadyExists("Regra já existente")

    def remove_rule(self):
        sg = self.get_security_group()
        return self.ec2.revoke_security_group_ingress(
            GroupId=sg.get("GroupId"), IpProtocol="tcp",
            FromPort=22, ToPort=22,
            CidrIp="{}/32".format(self.address)
        )
