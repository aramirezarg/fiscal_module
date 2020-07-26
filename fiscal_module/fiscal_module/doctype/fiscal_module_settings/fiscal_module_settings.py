# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document
from fiscal_module.setup import install
import frappe


def get_option(options, attr, default=None):
    return options[attr] if attr in options else default


class FiscalModuleSettings(Document):
    pass


@frappe.whitelist()
def check_structure():
    install.create_documents_structure()