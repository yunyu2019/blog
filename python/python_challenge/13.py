#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:
#www.pythonchallenge.com/pc/return/disproportional.html
import xmlrpclib

phonebook=xmlrpclib.ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php')
"""
print phonebook.system.listMethods()
print phonebook.system.methodHelp('phone')
print phonebook.system.methodSignature('phone')
"""
call=phonebook.phone('Bert')
print call[4:].lower()