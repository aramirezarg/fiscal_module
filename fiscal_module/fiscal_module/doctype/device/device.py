# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import datetime


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

            if fd.status == "Enabled":
                filters = {
                    "fiscal_document": fd.fiscal_document,
                    "name": ("!=", fd.name),
                    "status": "Enabled"
                }
                if frappe.db.count("Device Fiscal Document", filters) > 0:
                    frappe.throw(_('The Fiscal Document {0} already use in Device {1}').format(
                        fd.fiscal_document, frappe.get_value("Device Fiscal Document", filters, "parent")
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

        device_filter = {"name": Device.identifier()} if settings.device else {"user": frappe.session.user}

        if frappe.db.count("Device", device_filter) == 0:
            frappe.throw(_(f'{_("This Device or Browser has not ben configured")}<br><br>'
                           f'<strong>{_("Please configure this Device before continuing")}</strong>'))
        else:
            return frappe.get_doc("Device", device_filter)

    @staticmethod
    def identifier():
        return frappe.cache().hget('device_id', frappe.session.sid)

    @staticmethod
    def set_identifier(device_id, string_components=None, detail_components=None):
        expires = datetime.datetime.now() + datetime.timedelta(days=365)
        frappe.cache().hset('device_id', frappe.session.sid, device_id)
        frappe.local.cookie_manager.set_cookie("device_id", device_id, expires=expires)

        if frappe.get_value("Device", device_id) is None:
            doc = frappe.new_doc("Device")
            doc.identifier = device_id
            doc.string_components = "" if string_components is None else string_components

            doc.company = frappe.defaults.get_user_default('company')
            if detail_components is not None:
                for row in detail_components:
                    doc.host = row["host"]
                    doc.workstation_name = row["host"]
                    doc.primary_device = row["primary_device"]
                    doc.mac = row["mac"]

            doc.save()
