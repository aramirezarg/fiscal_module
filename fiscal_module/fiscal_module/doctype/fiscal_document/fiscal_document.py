# -*- coding: utf-8 -*-
# Copyright (c) 2020, CETI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import date_diff, cint, cstr
from frappe import _


class FiscalDocument(Document):
    def autoname(self):
        self.name = f'{self.fiscal_document} ({self.prefix})'

    def validate(self):
        self.validate_expired_document()
        self.validate_current_position()
        self.validate_dates()

    def fiscal_document_has_expired(self):
        return date_diff(self.final_date,
                         (datetime.now() if self.validation_date is None else self.validation_date)) < 0

    def validate_expired_document(self, throw=False):
        return False
        if self.fiscal_document_has_expired():
            self.execute_validate("The Fiscal Document has expired" + self.validation_date, throw)

    def execute_validate(self, message, throw=False):
        if throw:
            frappe.throw(message)
        else:
            frappe.msgprint(_(message), indicator='red', alert=True)

    def validate_dates(self):
        if date_diff(self.initial_date, self.final_date) > 0:
            frappe.throw('The final date must be greater than the initial date')

    def validate_current_position(self, throw=False):
        if cint(self.current_position) > cint(self.final_number):
            message = "There are no invoice numbers available for the active tax document"
            self.execute_validate(message, throw)

    def invoice_number(self):
        if self.current_position is None or self.current_position == 0:
            self.current_position = self.initial_number
        else:
            self.current_position = (cint(self.current_position) + 1)

        self.validate_current_position(True)

        frappe.db.set_value("Fiscal Document", self.name, "current_position", self.current_position)

        return f'{self.prefix}-{str(self.current_position).zfill(self.last_segment_length)}'

    def date_range(self):
        return f'{self.get_formatted("initial_date")} - {self.get_formatted("final_date")}'

    def invoice_range(self):
        return f'{self.prefix}-{str(self.initial_number).zfill(self.last_segment_length)} - {self.final_number}'

    @property
    def get_initial_number(self):
        return f'{self.prefix}-{str(self.initial_number).zfill(self.last_segment_length)}'

    @property
    def get_final_number(self):
        return f'{self.prefix}-{str(self.final_number).zfill(self.last_segment_length)}'

    def fiscal_document_invoice(self, doc):
        from ceti.utils import money_in_words
        return frappe.render_template(
            "fiscal_module/fiscal_module/doctype/fiscal_document/fiscal_document_invoice.html", {
                "model": self,
                "doc": doc,
                "letter_amount": money_in_words(doc.grand_total)
            })

    def get_customer_address(self, customer):
        if frappe.get_value("Address", customer.customer_primary_address) is not None:
            from frappe.contacts.doctype.address.address import get_address_display

            return get_address_display(customer.customer_primary_address)
        else:
            return ''

    def set_fiscal_data_in_invoice1(self, invoice, pos_profile):
        frappe.db.sql("""
            update `tabSales Invoice` set 
                naming_series=%s,
                invoice_number=%s,
                fiscal_document=%s,
                initial_date=%s,
                final_date=%s,
                initial_number=%s,
                final_number=%s,
                pos_profile=%s
        	where name=%s
        """, (
            self.prefix,
            self.invoice_number(),
            self.name,
            self.initial_date,
            self.final_date,
            self.get_initial_number,
            self.get_final_number,
            pos_profile,
            invoice
        ))

    def set_fiscal_data_in_invoice(self, party):
        name = self.invoice_number()

        party.name = name
        party.invoice_number = name
        party.fiscal_document = self.name
        party.fiscal_document_description = self.fiscal_document
        party.initial_date = self.initial_date
        party.final_date = self.final_date
        party.initial_number = self.get_initial_number
        party.final_number = self.get_final_number

    def validate_from_invoice(self):
        self.validate_expired_document(True)
        self.validate_current_position(True)

    def normalize_taxes(self, taxes):
        _taxes = []
        for tax in taxes:
            _taxes.append(dict(
                description=tax.description,
                base=tax.base_total,
                rate=tax.rate,
                amount=tax.tax_amount,
                total=tax.total,
            ))

        return _taxes

    def render_taxes(self, taxes):
        return frappe.render_template(
            "fiscal_module/fiscal_module/doctype/fiscal_document/taxes.html", {
                "data": self.normalize_taxes(taxes),
            })

    def test(self):
        pass


def fiscal_document_data(doc, method=None):
    from fiscal_module.fiscal_module import api
    fiscal_document, pos_profile = api.fiscal_module_data(doc)

    fiscal_document.validation_date = doc.posting_date
    fiscal_document.validate_from_invoice()
    return fiscal_document, pos_profile


def validate_fiscal_document(doc, method=None):
    fiscal_document_data(doc)


"""def set_fiscal_document_info(doc, method=None):
    fiscal_document, pos_profile = fiscal_document_data(doc)
    fiscal_document.set_fiscal_data_in_invoice(doc.name, pos_profile.name)"""


def set_fiscal_document_info(doc, method=None):
    fiscal_document, pos_profile = fiscal_document_data(doc)

    if not doc.invoice_number:
        fiscal_document.set_fiscal_data_in_invoice(doc)


def set_purchase_invoice_name(doc, method=None):
    doc.name = doc.invoice_number


def test():
    pass
