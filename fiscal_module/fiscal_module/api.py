# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI Systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import json


class FiscalDocumentManage:
    @staticmethod
    def has_device():
        return frappe.db.count("Device", {
            "user": frappe.session.user
        })

    @staticmethod
    def get_device(device=None):
        if device is None:
            frappe.throw(_(f'{_("The Device has not ben configured")}<br><br>'
                           f'<strong>{_("Please configure the Device before continuing")}</strong>'))

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
                           f'<strong>{_("Please configure the the Fiscal Module before continuing")}</strong>'))

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
            FiscalDocumentManage.fiscal_document_filters(pos_profile),
            "fiscal_document"
        )

    @staticmethod
    def get_fiscal_document(pos_profile=None):
        fiscal_document_name = FiscalDocumentManage.fiscal_document_name(pos_profile)

        if fiscal_document_name is None:
            frappe.throw(_(f'{_("The Fiscal Document has not ben configured for this User")}<br><br>'
                           f'<strong>{_("Please configure the Fiscal Document before continuing")}</strong>'))
        else:
            return frappe.get_doc("Fiscal Document", FiscalDocumentManage.fiscal_document_name(pos_profile))


def fiscal_module_data(doc):
    config = FiscalDocumentManage.config()
    pos_profile = FiscalDocumentManage.pos_profile() if doc.pos_profile is None \
        else frappe.get_doc("POS Profile", doc.pos_profile)

    if config.device:
        FiscalDocumentManage.get_device(pos_profile.device)

    return FiscalDocumentManage.get_fiscal_document(pos_profile.name), pos_profile
