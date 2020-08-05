# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI Systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from fiscal_module.fiscal_module.doctype.device.device import Device


@frappe.whitelist()
def set_device_id(device_id, current_device_id=None):
    cookie_device_id = Device.identifier()

    if current_device_id is None:
        Device.set_identifier(device_id)
    else:
        if frappe.get_value("Device", cookie_device_id) is not None:
            Device.set_identifier(device_id)
        else:
            if cookie_device_id != device_id:
                frappe.rename_doc('Device', cookie_device_id, device_id)
                frappe.db.set_value("Device", device_id, "identifier", device_id)