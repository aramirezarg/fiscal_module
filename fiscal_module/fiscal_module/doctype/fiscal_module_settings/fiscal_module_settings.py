# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class FiscalModuleSettings(Document):
    def validate(self):
        self.check_documents()

    def check_documents(self):
        fields = dict(
            ####################
            fiscal_document_section_break1=dict(
                label="Fiscal Document", fieldtype="Section Break"
            ),
            invoice_number=dict(
                label="Invoice Number", fieldtype="Data"
            ),
            initial_date=dict(
                label="Initial Date", fieldtype="Date"
            ),
            final_date=dict(
                label="Final Date", fieldtype="Date"
            ),

            ####################
            fiscal_document_column_break2=dict(
                label="", fieldtype="Column Break"
            ),
            fiscal_document=dict(
                label="Fiscal Document", fieldtype="Link", print_hide='Print Hide'
            ),
            fiscal_document_description=dict(
                label="CAI", fieldtype="Read Only", fetch_from='fiscal_document.fiscal_document', hidden=1
            ),
            initial_number=dict(
                label="Initial Number", fieldtype="Data"
            ),
            final_number=dict(
                label="Final Number", fieldtype="Data"
            ),
            fiscal_document_section_break2=dict(
                label="", fieldtype="Section Break"
            ),
        )

        doctypes = ["Sales Invoice", "Fees"]
        insert_after = ""

        for doctype in doctypes:
            for f in fields:
                field = fields[f]
                filters = {"dt": doctype, "fieldname": f}

                if frappe.get_value("Custom Field", filters) is None:
                    doc = frappe.new_doc("Custom Field")
                    doc.dt = doctype
                    doc.label = field["label"]
                    doc.fieldname = f
                    doc.fieldtype = field["fieldtype"]
                    doc.options = field["label"] if field["fieldtype"] == "Link" else ""

                    doc.read_only = 1
                    doc.translatable = 0
                    doc.insert_after = insert_after

                    if "fetch_from" in field:
                        doc.fetch_from = field['fetch_from']

                    if "hidden" in field:
                        doc.hidden = field['hidden']

                    if "print_hide" in field:
                        doc.printhide = field['print_hide']

                    doc.save()
                    insert_after = f

        if frappe.get_value("Custom Field", {
            "dt": "Fees",
            "fieldname": "pos_profile"
        }) is None:
            doc = frappe.new_doc("Custom Field")
            doc.label = "POS Profile"
            doc.fieldname = "pos_profile"
            doc.dt = "Fees"
            doc.fieldtype = "Link"
            doc.options = "POS Profile"
            doc.translatable = 0
            doc.read_only = 1

            doc.save()

        if frappe.get_value("Custom Field", {
            "dt": "POS Profile",
            "fieldname": "fiscal_document"
        }) is None:
            doc = frappe.new_doc("Custom Field")
            doc.label = "Fiscal Document"
            doc.fieldname = "fiscal_document"
            doc.dt = "POS Profile"
            doc.fieldtype = "Table"
            doc.options = "POS Fiscal Document"
            doc.translatable = 0
            doc.reqd = 1

            doc.save()

        if frappe.get_value("Custom Field", {
            "dt": "POS Profile",
            "fieldname": "device"
        }) is None:
            doc = frappe.new_doc("Custom Field")
            doc.label = "Device"
            doc.fieldname = "device"
            doc.dt = "POS Profile"
            doc.fieldtype = "Link"
            doc.options = "Device"
            doc.insert_after = "fiscal_document"
            doc.translatable = 0
            doc.reqd = 1

            doc.save()

        if frappe.get_value("Custom Field", {
            "dt": "Purchase Invoice",
            "fieldname": "invoice_number"
        }) is None:
            doc = frappe.new_doc("Custom Field")
            doc.label = "Invoice Number"
            doc.fieldname = "invoice_number"
            doc.dt = "Purchase Invoice"
            doc.fieldtype = "Data"
            doc.translatable = 0
            doc.reqd = 1
            doc.save()

        if frappe.get_value("Custom Field", {
            "dt": "Purchase Invoice",
            "fieldname": "fiscal_document"
        }) is None:
            doc = frappe.new_doc("Custom Field")
            doc.label = "Fiscal Document"
            doc.fieldname = "fiscal_document"
            doc.dt = "Purchase Invoice"
            doc.fieldtype = "Data"
            doc.translatable = 0
            doc.reqd = 1
            doc.save()