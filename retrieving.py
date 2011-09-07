#!/usr/bin/env python
# coding: utf-8

"""
Retrieving data from the ``lilacs.type3`` collection::

    >>> from pymongo import Connection 
    >>> db = Connection().lilacs
    >>> db.type3.count()
    561811
    >>> for r in db.type3.find(None,{'_id':1}).limit(10): print r
    {u'_id': u'593411'}
    {u'_id': u'593410'}
    {u'_id': u'593409'}
    {u'_id': u'593408'}
    {u'_id': u'593407'}
    {u'_id': u'593406'}
    {u'_id': u'593402'}
    {u'_id': u'593328'}
    {u'_id': u'593405'}
    {u'_id': u'593404'}
    >>> r = db.type3.find_one()
    >>> r['v35']
    [{u'_': u'0101-6628'}]
    >>> r['v10'][0]['1']
    u'UFSC'
    >>> r['v10'][0]['p']
    u'Brasil'
    
"""

from pymongo import Connection

def setup():
    global db
    db = Connection().lilacs

def test_count():
    assert db.type3.count() == 561811   

def test_find():
    r = db.type3.find_one({'_id': '593411'})
    assert r['v35'] == [{u'_': u'0101-6628'}]

