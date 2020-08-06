# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI Systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from fiscal_module.fiscal_module.doctype.device.device import Device


@frappe.whitelist()
def set_device_id(device_components=None):
    import json
    from ceti.api import encrypt

    settings = Device.general_settings()
    request_components = json.loads(device_components)
    components = {}
    changes = False

    if settings.identifier_mode:
        for item in request_components:
            if frappe.db.count("Device Component", {
                "component": item['key'],
                "parent": settings.name
            }) == 0:
                changes = True
                settings.append('device_component', dict(
                    component=item['key'],
                    excluded=1 if item['value'] == 'not available' else 0
                ))
            elif item['value'] == 'not available':
                frappe.db.set_value("Device Component", {
                    "component": item["key"],
                    "parent": settings.name
                }, "excluded", 1)

    if changes:
        settings.save()
        settings.reload()

    base = ""
    for item in settings.device_component:
        if item.excluded == 0:
            components[item.component] = get_component(request_components, item.component)
            base = base + f'%({item.component})s|'

    HA1_str = base % components
    device_id = encrypt(HA1_str, "md5")

    cookie_device_id = Device.identifier()
    if cookie_device_id is None:
        Device.set_identifier(device_id)
    else:
        if frappe.get_value("Device", cookie_device_id) is None:
            Device.set_identifier(device_id)
        else:
            if cookie_device_id != device_id:
                if frappe.get_value("Device", device_id) is None:
                    frappe.rename_doc('Device', cookie_device_id, device_id)
                    frappe.db.set_value("Device", device_id, "identifier", device_id)

    return device_id


def get_component(components, component):
    for item in components:
        if item["key"] == component:
            return item["value"]

    return ""
