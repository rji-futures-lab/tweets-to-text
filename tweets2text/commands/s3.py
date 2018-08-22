# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom commands for managing tweet2text's integration with AWS S3.
"""
import click
from flask.cli import AppGroup, with_appcontext
from tweets2text.s3 import get_bucket


s3_cli = AppGroup('s3')


@s3_cli.command('create-bucket')
@with_appcontext
def create_bucket_command():
    """
    Create the S3 bucket specified in the `S3_BUCKET_NAME` env var.
    """
    bucket = get_bucket()
    
    if not bucket.creation_date:
        bucket.create()
        bucket.meta.client.get_waiter('bucket_exists')
        click.echo('%s created.' % bucket.name)
    else:
        click.echo('%s already exists.' % bucket.name)
