# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class Device(Document):
    def autoname(self):
        self.name = self.identifier

    def validate(self):
        self.validate_fiscal_documents()

    def validate_fiscal_documents(self):
        checks = []
        for fd in self.fiscal_document:
            if frappe.get_value("Fiscal Document", fd.fiscal_document, "company") != self.company:
                frappe.throw(_('The Fiscal Document {0} must belong to the company {1}').format(
                    fd.fiscal_document, self.company
                ))

            checks.append(fd.fiscal_document)

        if len(checks) != len(set(checks)):
            frappe.throw(_('The Fiscal Document must be unique'))

    @property
    def has_pos_profile(self):
        return self.pos_profile is not None

    @property
    def get_pos_profile(self):
        if frappe.get_value("POS Profile", self.pos_profile) is None:
            frappe.throw(_(f'{_("The POS Profile has not ben configured for this device")}<br><br>'
                           f'<strong>{_("Please configure the POS profile before continuing")}</strong>'))

        return frappe.get_doc("POS Profile", self.pos_profile)

    def fiscal_document_filters(self):
        return {
            "parentType": "Device",
            "parent": self.name,
            "status": "enabled"
        }

    @property
    def has_active_fiscal_document(self):
        return frappe.db.count("Device Fiscal Document", self.fiscal_document_filters())

    @property
    def active_fiscal_document_name(self):
        return frappe.get_value(
            "Device Fiscal Document",
            self.fiscal_document_filters(),
            "fiscal_document"
        )

    @property
    def get_active_fiscal_document(self):
        fiscal_document_name = self.active_fiscal_document_name

        if fiscal_document_name is None:
            frappe.throw(_(f'{_("The Fiscal Document has not ben configured in this Device")}<br><br>'
                           f'<strong>{_("Please configure the Fiscal Document before continuing")}</strong>'))
        else:
            return frappe.get_doc("Fiscal Document", self.active_fiscal_document_name)

    @staticmethod
    def general_settings():
        config = frappe.get_single("Fiscal Module Settings")
        if config is None:
            frappe.throw(_(f'{_("The Fiscal Module Settings has not ben set")}<br><br>'
                           f'<strong>{_("Please configure the Fiscal Module before continuing")}</strong>'))

        return config

    @staticmethod
    def get_current(settings=None):
        settings = Device.general_settings() if settings is None else settings
        cookie_device_id = Device.identifier()
        device_filter = {}

        if settings.device:
            if not cookie_device_id:  # "device_id" in frappe.local.cookie_manager.cookies:
                device_filter = {"name": cookie_device_id}
        else:
            device_filter = {"user": frappe.session.user}

        if frappe.get_value("Device", device_filter) is None:
            frappe.throw(_(f'{_("This Device has not ben configured")}<br><br>'
                           f'<strong>{_("Please configure this Device before continuing")} {cookie_device_id}</strong>'))
        else:
            return frappe.get_doc("Device", cookie_device_id)

    @staticmethod
    def identifier():
        return frappe.cache().hget('device_id', 'device_id')
        """d = None
        if hasattr(frappe.local.cookie_manager, "cookies"):
            if "device_id" in frappe.local.cookie_manager.cookies:
                d = frappe.local.cookie_manager.cookies["device_id"]["value"]
        else:
            d = None

        return d"""

    @staticmethod
    def identifier1():
        return Device.identifier()

    @staticmethod
    def set_identifier(device_id):
        import datetime
        expires = datetime.datetime.now() + datetime.timedelta(days=2)
        frappe.cache().hset('device_id', "device_id", device_id)

        if hasattr(frappe.local, "cookie_manager"):

            frappe.local.cookie_manager.set_cookie("device_id", device_id, expires=expires, httponly=False)

            if frappe.get_value("Device", device_id) is None:
                doc = frappe.new_doc("Device")
                doc.workstation_name = f"Workstation {frappe.db.count('Device') + 1}"
                doc.identifier = device_id
                doc.company = frappe.defaults.get_user_default('company')
                doc.save()
