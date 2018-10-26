# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialize AWS Simple Email Service (SES)."""
import logging
from .boto3 import get_boto3session


class SESHandler(logging.Handler):
    """A handler for sending emails via AWS SES."""

    def __init__(self, **kwargs):
        """
        Initialize a SESHandler instance.

        Kwargs:
            fromaddr (str): Email address of the sender.
            toaddrs (list): Email address of the recipients.
            subject (str): Subject of the email.
        """
        logging.Handler.__init__(self)
        self.fromaddr = kwargs['fromaddr']
        self.toaddrs = kwargs['toaddrs']
        self.subject = kwargs['subject']

    source = "gordonj@rjionline.org"

    def emit(self, record):
        """Send the email."""
        client = get_boto3session().client('ses')
        client.send_email(
            Source=self.fromaddr,
            Destination=dict(
                ToAddresses=self.toaddrs,
            ),
            Message=dict(
                Subject=dict(
                    Data=self.subject
                ),
                Body=dict(
                    Text=dict(
                        Data=self.format(record),
                    )
                )
            )
        )


ses_handler = SESHandler(
    fromaddr='gordonj@rjionline.org',
    toaddrs=['gordonj@rjionline.org'],
    subject='Application Error'
)
ses_handler.setLevel(logging.ERROR)
ses_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
