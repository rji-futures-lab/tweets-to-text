#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Blueprint and routes for tweets2text website.
"""
from flask import Blueprint


bp = Blueprint('index', __name__)

@bp.route('/')
def hello_world():
    return 'Hello, world!'