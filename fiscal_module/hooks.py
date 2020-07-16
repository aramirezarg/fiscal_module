# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "fiscal_module"
app_title = "Fiscal Module"
app_publisher = "CETI"
app_description = "Fiscal Module"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@ceti.systems"
app_license = "MIT"

doc_events = {
    "Sales Invoice": {
        "autoname": "fiscal_module.fiscal_module.doctype.fiscal_document.fiscal_document.set_fiscal_document_info",
        #"on_load": "fiscal_module.fiscal_module.doctype.fiscal_document.fiscal_document.set_fiscal_document_link",
        #"on_create": "fiscal_module.fiscal_module.doctype.fiscal_document.fiscal_document.set_fiscal_document_info",
        #"on_update": "fiscal_module.fiscal_module.doctype.fiscal_document.fiscal_document.set_fiscal_document_info",
        #"on_submit": "fiscal_module.fiscal_module.doctype.fiscal_document.fiscal_document.set_fiscal_document_info",
    },
    "Fees": {
        "autoname": "fiscal_module.fiscal_module.doctype.fiscal_document.fiscal_document.set_fiscal_document_info",
        #"on_load": "fiscal_module.fiscal_module.doctype.fiscal_document.fiscal_document.set_fiscal_document_link",
        #"on_create": "fiscal_module.fiscal_module.doctype.fiscal_document.fiscal_document.set_fiscal_document_info",
        #"on_update": "fiscal_module.fiscal_module.doctype.fiscal_document.fiscal_document.set_fiscal_document_info",
        #"on_submit": "fiscal_module.fiscal_module.doctype.fiscal_document.fiscal_document.set_fiscal_document_info",
    },
}

#doctype_js = {
#    "Sales Invoice": "public/js/payment_entry_doctype.js",
#    "Purchase Invoice": "public/js/purchase_invoice_doctype.js"
#}

#fixtures = [
#    "Custom Script", {
#        "dt": "Custom Field", "filters": [["dt", "in", ("Titulos", "Parcelas", "Payment Entry")]]}
#]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/fiscal_module/css/fiscal_module.css"
# app_include_js = "/assets/fiscal_module/js/fiscal_module.js"

# include js, css files in header of web template
# web_include_css = "/assets/fiscal_module/css/fiscal_module.css"
# web_include_js = "/assets/fiscal_module/js/fiscal_module.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "fiscal_module.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "fiscal_module.install.before_install"
# after_install = "fiscal_module.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "fiscal_module.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"fiscal_module.tasks.all"
# 	],
# 	"daily": [
# 		"fiscal_module.tasks.daily"
# 	],
# 	"hourly": [
# 		"fiscal_module.tasks.hourly"
# 	],
# 	"weekly": [
# 		"fiscal_module.tasks.weekly"
# 	]
# 	"monthly": [
# 		"fiscal_module.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "fiscal_module.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "fiscal_module.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "fiscal_module.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]
