# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


@frappe.whitelist()
def get_device(device=None):
    if frappe.get_value("Device", device):
        doc = frappe.get_doc("Device", device)
        return [
            doc,
            frappe.render_template("fiscal_module/fiscal_module/page/device_settings/device_settings.html", {
                "doc": doc,
                "data": frappe.session.data
            }),
            frappe.session.data
        ]

    return None
