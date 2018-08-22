# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom commands for managing tweet2text's integration with AWS DynamoDB.
"""
import click
from flask.cli import AppGroup, with_appcontext
from tweets2text.dynamodb import get_dynamodb, schema


dynamodb_cli = AppGroup('dynamodb')


@dynamodb_cli.command('create-tables')
@click.option('--delete', '-d', help='Drop existing tables.', is_flag=True)
@with_appcontext
def create_tables_command(delete):
    """
    Create all tables in DynamoDB, skipping any that already exists.
    """
    dynamodb = get_dynamodb()
    created_tables = [t.name for t in dynamodb.tables.all()]
    for table_def in schema:
        table_name = table_def['TableName']
        exists = table_name in created_tables
        
        if exists and not delete:
            click.echo(' %s already created.' % table_name)
        else:
            if exists and delete:
                table = dynamodb.Table(table_name)
                dynamodb.meta.client.delete_table(TableName=table_name)
                click.echo('  Deleting %s...' % table_name)
                table.wait_until_not_exists()
                click.echo('  %s deleted.' % table_name)

            table = dynamodb.create_table(**table_def)
            table.meta.client.get_waiter('table_exists').wait(
                TableName=table_def['TableName']
            )
            click.echo(
                ' {0.table_name} created at {0.creation_date_time}'.format(table)
            )

    click.echo('All tables created.')
