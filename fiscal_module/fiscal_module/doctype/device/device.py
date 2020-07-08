# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class Device(Document):
    @property
    def has_pos_profile(self):
        return self.pos_profile is not None

    @property
    def get_pos_profile(self):
        return frappe.get_doc("POS Profile", self.pos_profile)

    def fiscal_document_filters(self, pos_profile=None):
        return {
            "parentType": "POS Profile",
            "parent": pos_profile,
            "status": "enabled"
        }

    def has_fiscal_document(self, pos_profile=None):
        return frappe.db.count("POS Fiscal Document", self.fiscal_document_filters(pos_profile))

    def fiscal_document_name(self, pos_profile=None):
        return frappe.get_value(
            "POS Fiscal Document",
            self.fiscal_document_filters(pos_profile),
            "fiscal_document"
        )

    def get_fiscal_document(self, pos_profile=None):
        return frappe.get_doc("Fiscal Document", self.fiscal_document_name(pos_profile))
