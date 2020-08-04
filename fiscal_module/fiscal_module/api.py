# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI Systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from fiscal_module.fiscal_module.doctype.device.device import Device
import datetime

class DeviceManage:
    @staticmethod
    def settings():
        return Device.general_settings()

    @staticmethod
    def get_current(settings):
        settings = DeviceManage.settings() if settings is None else settings
        return Device.get_current(settings)
"""
    @staticmethod
    def has_device(settings):
        return frappe.db.count("Device", {
            "identifier" if settings.device else "user": frappe.session.user
        })

    @staticmethod
    def get_device(settings):
        current_device = DeviceManage.current_device(settings)

        if settings.device:
            if current_device is None:
                frappe.throw(_(f'{_("The Device has not ben configured")}<br><br>'
                               f'<strong>{_("Please configure the Device before continuing")}</strong>'))

        else:
            return frappe.get_doc("Device", device)

    @staticmethod
    def pos_profile():
        from erpnext.stock.get_item_details import get_pos_profile

        pos_profile = get_pos_profile(frappe.defaults.get_user_default('company'))

        if pos_profile is None:
            frappe.throw(_(f'{_("The POS Profile has not ben configured for this device")}<br><br>'
                           f'<strong>{_("Please configure the POS profile before continuing")}</strong>'))

        return pos_profile

    @staticmethod
    def config():
        config = frappe.get_single("Fiscal Module Settings")
        if config is None:
            frappe.throw(_(f'{_("The Fiscal Module Settings has not ben set")}<br><br>'
                           f'<strong>{_("Please configure the Fiscal Module before continuing")}</strong>'))

        return config

    @staticmethod
    def fiscal_document_filters(pos_profile=None):
        return {
            "parentType": "POS Profile",
            "parent": pos_profile,
            "status": "enabled"
        }

    @staticmethod
    def fiscal_document_name(pos_profile=None):
        return frappe.get_value(
            "POS Fiscal Document",
            DeviceManage.fiscal_document_filters(pos_profile),
            "fiscal_document"
        )

    @staticmethod
    def get_fiscal_document(pos_profile=None):
        fiscal_document_name = DeviceManage.fiscal_document_name(pos_profile)

        if fiscal_document_name is None:
            frappe.throw(_(f'{_("The Fiscal Document has not ben configured for this User")}<br><br>'
                           f'<strong>{_("Please configure the Fiscal Document before continuing")}</strong>'))
        else:
            return frappe.get_doc("Fiscal Document", DeviceManage.fiscal_document_name(pos_profile))
"""

"""def fiscal_module_data(doc):
    config = DeviceManage.config()
    pos_profile = DeviceManage.pos_profile() if doc.pos_profile is None \
        else frappe.get_doc("POS Profile", doc.pos_profile)

    if config.device:
        DeviceManage.current_device()

    return DeviceManage.get_fiscal_document(pos_profile.name), pos_profile"""


@frappe.whitelist()
def set_device_id(device_id):
    if not Device.identifier():
        cookie_device_id = Device.identifier()# frappe.local.cookie_manager.cookies["device_id"]

        if frappe.get_value("Device", cookie_device_id):
            if frappe.device_id != device_id:
                frappe.rename_doc('Device', cookie_device_id, device_id)
                frappe.db.set_value("Device", device_id, "identifier", device_id)
        else:
            identifier_device(device_id)
    else:
        identifier_device(device_id)

    return frappe.local.cookie_manager.cookies


@frappe.whitelist()
def test_device_id():
    return frappe.local.cookie_manager.cookies, Device.identifier()


def identifier_device(device_id):
    frappe.local.cookie_manager.init_cookies()
    expires = datetime.datetime.now() + datetime.timedelta(days=(365 * 10))
    frappe.local.cookie_manager.set_cookie("device_id", device_id, expires=expires, httponly=True)

    frappe.device_id = device_id

    if frappe.get_value("Device", device_id) is None:
        doc = frappe.new_doc("Device")
        doc.workstation_name = f"Workstation {frappe.db.count('Device') + 1}"
        doc.identifier = device_id
        doc.company = frappe.defaults.get_user_default('company')
        doc.save()
