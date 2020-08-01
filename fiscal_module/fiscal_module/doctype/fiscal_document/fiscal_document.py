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
        self.name = f'{self.fiscal_document} ({self.get_prefix})'

    def validate(self):
        self.set_prefix()
        self.validate_company()
        self.validate_expired_document()
        self.validate_current_position()
        self.validate_protected_current_position()
        self.validate_dates()

    def set_prefix(self):
        self.prefix = self.get_prefix

    @property
    def get_prefix(self):
        return f"{self.establishment_id}-{self.emission_point_id}-{self.fiscal_document_type_id}"

    def validate_company(self):
        if self.establishment_id is None:
            self.execute_validate("Set the Establishment Number in your Company", True)

    @property
    def fiscal_document_has_expired(self):
        return date_diff(self.final_date,
                         (datetime.now() if self.validation_date is None else self.validation_date)) < 0

    @property
    def fiscal_document_out_range(self):
        return date_diff((datetime.now() if self.validation_date is None else self.validation_date),
                         self.initial_date) < 0

    def validate_expired_document(self, throw=False):
        if self.fiscal_document_has_expired:
            self.execute_validate("The Fiscal Document has expired", throw)

        if self.fiscal_document_out_range:
            self.execute_validate("The Fiscal Document is out of time", True)

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

    def validate_protected_current_position(self, throw=True, protected=None):
        protected = frappe.get_value("Fiscal Document", self.name, "current_position") if protected is None else protected

        if cint(self.current_position) != cint(protected):
            message = "The current position on your screen does not correspond to the last changes, please refresh"
            self.execute_validate(message, throw)

    def validate_unique_invoice(self, invoice):
        if frappe.db.count("Sales Invoice", {
            "invoice_number": invoice
        }) > 0:
            message = "The last invoice number is exist, please update the fiscal document"
            self.execute_validate(message, True)

    def invoice_number(self):
        if self.current_position is None or self.current_position == 0:
            self.current_position = self.initial_number
        else:
            self.current_position = (cint(self.current_position) + 1)

        correlative = str(self.current_position).zfill(self.correlative_size)
        invoice_number = f'{self.prefix}-{correlative}'

        self.validate_current_position(True)
        self.validate_unique_invoice(invoice_number)

        frappe.db.set_value("Fiscal Document", self.name, "current_position", self.current_position)

        return invoice_number, correlative

    def date_range(self):
        return f'{self.get_formatted("initial_date")} - {self.get_formatted("final_date")}'

    def invoice_range(self):
        return f'{self.prefix}-{str(self.initial_number).zfill(self.correlative_size)} - {self.final_number}'

    @property
    def get_initial_number(self):
        return f'{self.prefix}-{str(self.initial_number).zfill(self.correlative_size)}'

    @property
    def get_final_number(self):
        return f'{self.prefix}-{str(self.final_number).zfill(self.correlative_size)}'

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

    def set_fiscal_data_in_invoice(self, party):
        name, correlative = self.invoice_number()

        party.name = name
        party.invoice_number = name
        party.fiscal_document = self.name
        party.fiscal_document_description = self.fiscal_document
        party.initial_date = self.initial_date
        party.final_date = self.final_date
        party.initial_number = self.get_initial_number
        party.final_number = self.get_final_number

        if party.doctype != "Purchase Invoice":
            self.set_fiscal_document_dependencies(party, correlative)

    def set_fiscal_document_dependencies(self, party, correlative):
        party.establishment = self.establishment_id
        party.emission_point = self.emission_point_id
        party.fiscal_document_type = self.fiscal_document_type_id
        party.correlative = correlative

    def validate_from_invoice(self, settings):
        self.validate_expired_document(settings.date_range == 1)
        self.validate_current_position(settings.billing_range == 1)

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
    settings = frappe.get_single("Fiscal Module Settings")

    fiscal_document.validation_date = doc.posting_date
    fiscal_document.validate_from_invoice(settings)
    return fiscal_document, pos_profile


def validate_fiscal_document(doc, method=None):
    if frappe.get_value("Sales Invoice", doc.name) == 1:
        pass
    else:
        if doc.fiscal_document:
            fiscal_document = frappe.get_doc("Fiscal Document", doc.fiscal_document)
            settings = frappe.get_single("Fiscal Module Settings")

            fiscal_document.validation_date = doc.posting_date
            fiscal_document.validate_from_invoice(settings)
        else:
            fiscal_document_data(doc)


# Set data in invoice
def set_fiscal_document_info(doc, method=None):
    fiscal_document, pos_profile = fiscal_document_data(doc)
    fiscal_document.set_fiscal_data_in_invoice(doc)


def autoname_purchase_invoice(doc, method=None):
    if doc.status != "Canceled":
        doc.name = doc.invoice_number


def on_cancel_purchase_invoice(doc, method=None):
    if doc.amended_from is not None:
        frappe.rename_doc('Purchase Invoice', doc.name, f'{doc.name}_VOID')
        frappe.publish_realtime("redirect_invoice_on_cancel", f'{doc.name}_VOID')


def validate_fiscal_documents_in_pos(doc, method=None):
    checks = []
    for fd in doc.fiscal_document:
        if frappe.get_value("Fiscal Document", fd.fiscal_document, "company") != doc.company:
            frappe.throw(_('The Fiscal Document must belong to the company {0}').format(doc.company))

        checks.append(fd.fiscal_document)

    if len(checks) != len(set(checks)):
        frappe.throw(_('The Fiscal Document must be unique'))


@frappe.whitelist()
def fix_invoices():
    invoices = frappe.get_list("Sales Invoice", fields="name,invoice_number", filters={
        "invoice_number": ("!=", "name")
    })

    _fix_invoices = [invoice.name for invoice in invoices if invoice.name != invoice.invoice_number]

    count = 0
    for invoice in _fix_invoices:
        doc = frappe.get_doc("Sales Invoice", invoice)
        fiscal_document, pos_profile = fiscal_document_data(doc)

        name = fiscal_document.invoice_number()
        frappe.rename_doc('Sales Invoice', invoice, name)
        frappe.db.set_value("Sales Invoice", name, "invoice_number", name)

        frappe.publish_realtime(
            "progress", dict(
                progress=[count, len(_fix_invoices)],
                title=_('Fixed {0}').format(name),
            ),
            user=frappe.session.user
        )
        count += 1