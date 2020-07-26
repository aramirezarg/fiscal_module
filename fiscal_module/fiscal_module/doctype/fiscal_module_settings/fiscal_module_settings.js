// Copyright (c) 2020, CETI and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fiscal Module Settings', {
	refresh(frm) {
		frm.add_custom_button(__('Check Structure'), () => {
	        frappe.call({
				method: "fiscal_module.fiscal_module.doctype.fiscal_module_settings.fiscal_module_settings.check_structure",
				always: function(r) {
					frappe.msgprint(__("Completed"));
				}
			});
		});
		frm.add_custom_button(__('Fix Invoices'), () => {
	        frappe.call({
				method: "fiscal_module.fiscal_module.doctype.fiscal_document.fiscal_document.fix_invoices",
				always: function(r) {
					console.log(r)
				    frappe.msgprint(__("Completed"));
				}
			});
		});
	}
});
