# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI Systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from fiscal_module.fiscal_module.doctype.device.device import Device


@frappe.whitelist()
def set_identifier_device_data(device_components=None, string_components=None, detail_components=None, device_id=None):
    if device_components is not None:
        import json
        from ceti.api import encrypt

        request_components = json.loads(device_components)
        detail_components = json.loads(detail_components)
        components = {}

        base = ""
        for item in request_components:
            components[item.component] = get_component(request_components, item.component)
            base = base + f'%({item.component})s|'

        HA1_str = base % components
        device_id = encrypt(HA1_str, "md5")

    cookie_device_id = Device.identifier()
    if cookie_device_id is None:
        Device.set_identifier(device_id, string_components, detail_components)
    else:
        if frappe.get_value("Device", cookie_device_id) is None:
            Device.set_identifier(device_id, string_components, detail_components)
        else:
            if cookie_device_id != device_id:
                if frappe.get_value("Device", device_id) is None:
                    frappe.rename_doc('Device', cookie_device_id, device_id)
                    frappe.db.set_value("Device", device_id, "identifier", device_id)
                else:
                    pass
                    # TODO: Disconnect

    return device_id


def get_component(components, component):
    for item in components:
        if item["key"] == component:
            return item["value"]

    return ""
