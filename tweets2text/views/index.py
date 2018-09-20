#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Blueprint and routes for tweets2text website.
"""
from flask import Blueprint, render_template


bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return render_template('index.html')
