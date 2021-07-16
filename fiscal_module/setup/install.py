from __future__ import unicode_literals
import frappe


def after_install():
    update_fields()
    set_custom_scripts()
    create_documents_structure()


def get_option(options, attr, default=None):
    return options[attr] if attr in options else default


def add_custom_field(doctype, options):
    label = get_option(options, "label", "")
    fieldtype = get_option(options, "fieldtype")
    option = get_option(options, "options", label if fieldtype == "Link" else "")
    fieldname = get_option(options, "fieldname", frappe.scrub(label))
    name = f'{doctype}-{fieldname}'

    if frappe.get_value("Custom Field", name) is None:
        cf = frappe.new_doc("Custom Field")
        cf.dt = doctype
        cf.name = name
        cf.fieldname = fieldname
        cf.label = label
        cf.fieldtype = fieldtype
        cf.options = option
        cf.reqd = get_option(options, "reqd", 0)
        cf.no_copy = get_option(options, "no_copy", 1)
        cf.insert_after = get_option(options, "insert_after")
        cf.hidden = get_option(options, "hidden", 0)
        cf.fetch_from = get_option(options, "fetch_from", "")
        cf.print_hide = get_option(options, "print_hide", 0)
        cf.read_only = get_option(options, "read_only", 1)
        cf.translatable = 0
        cf.save()


def update_fields():
    docs = {
        "Fees": dict(naming_series=dict(reqd=0, hidden=1)),
        "Sales Invoice": dict(naming_series=dict(reqd=0, hidden=1)),
        "Purchase Invoice": dict(
            naming_series=dict(reqd=0, hidden=1),
            bill_no=dict(reqd=1),
            bill_date=dict(reqd=1),
        ),
    }
    for doc in docs:
        for field in docs[doc]:
            for attr in docs[doc][field]:
                frappe.db.set_value("DocField", {
                    "fieldname": field, "parentType": "DocType", "parent": doc
                }, attr, docs[doc][field][attr])


def set_custom_scripts():
    for doc in ["Purchase Invoice", "Sales Invoice", "Fees"]:
        if frappe.get_value("Custom Script", {"dt": doc}) is None:
            CS = frappe.new_doc("Custom Script")
            CS.dt = doc
            CS.script = """setInterval(()=>{ $("div[data-fieldname='naming_series']").hide()}, 500)"""
            CS.save()


def create_documents_structure():
    fields = {
        'fiscal_document_section_break1': dict(
            label="Fiscal Document", fieldname="fiscal_document_section_break1", fieldtype="Section Break"
        ),
        'Invoice Number': dict(),
        'Initial Date': dict(fieldtype="Date"),
        'Final Date': dict(fieldtype="Date"),

        'Column Break': dict(fieldtype="Column Break", fieldname="sales_invoice_column_break100", no_label=True),
        'Fiscal Document': dict(fieldtype="Link", print_hide='1', hidden='1'),
        'CAI': dict(
            fieldname="fiscal_document_description", fieldtype="Read Only",
            fetch_from='fiscal_document.fiscal_document'
        ),
        'Initial Number': dict(),
        'Final Number': dict(),
        'fiscal_document_section_break2': dict(fieldtype="Section Break", no_label=True),

        'Establishment': dict(hidden=1, print_hide=1),
        'Emission Point': dict(hidden=1, print_hide=1),
        'Fiscal Document Type': dict(hidden=1, print_hide=1),
        'Correlative': dict(hidden=1, print_hide=1),
    }

    doctypes = ["Sales Invoice", "Fees", "Purchase Invoice"]
    insert_after = ""

    for doctype in doctypes:
        for f in fields:
            field = fields[f]

            if doctype == "Purchase Invoice" and f in [
                "Invoice Number", "Initial Date", "Final Date",
                "Initial Number", "Final Number", "Fiscal Document Info",
                "fiscal_document_section_break1", "fiscal_document_section_break2",
                "Branch Office", "Emission Point", "Fiscal Document Type", "Correlative", "CAI"
            ]:
                pass
            else:
                no_label = get_option(field, "no_label", False)
                label = get_option(field, "label", "" if no_label else f)
                fieldname = get_option(field, "fieldname", frappe.scrub(f))
                fieldtype = get_option(field, "fieldtype", "Data")
                read_only = get_option(field, "read_only", 1)
                hidden = get_option(field, "hidden", 0)
                options = get_option(field, "options", label if fieldtype == "Link" else "")
                reqd = 0

                if doctype == "Purchase Invoice":
                    if "Fiscal Document" in [fieldname, label]:
                        reqd = 1 if fieldtype not in ["Column Break", "Section Break"] else 0
                        read_only = 0
                        insert_after = "bill_no"
                        hidden = 0

                    if "Fiscal Document" in [fieldname, label] and fieldtype == "Link":
                        fieldtype = "Data"
                        options = ""

                add_custom_field(doctype, dict(
                    label=label,
                    fieldname=fieldname,
                    fieldtype=fieldtype,
                    default=get_option(field, "default", ""),
                    insert_after=insert_after,
                    options=options,
                    fetch_from=get_option(field, "fetch_from"),
                    hidden=hidden,
                    print_hide=get_option(field, "print_hide", 0),
                    reqd=reqd,
                    read_only=read_only,
                ))
                insert_after = get_option(field, "insert_after", fieldname)

    add_custom_field("Fees", dict(
        label="POS Profile",
        fieldtype="Link"
    ))

    add_custom_field("Company", dict(
        label="Establishment",
        read_only=0,
        reqd=1,
        unique=1
    ))