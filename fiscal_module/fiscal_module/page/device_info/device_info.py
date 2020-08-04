# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


@frappe.whitelist()
def check_device(device=None):
    name = device
    if frappe.get_value("Device", device) is None:
        doc = frappe.new_doc("Device")
        doc.workstation_name = f"Workstation {frappe.db.count('Device') + 1}"
        doc.identifier = device
        doc.company = frappe.defaults.get_user_default('company')
        doc.save()

        name = doc.name

    return name
