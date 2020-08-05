# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


@frappe.whitelist()
def get_device(device=None):
    if frappe.get_value("Device", device):
        return frappe.get_doc("Device", device)

    return None
