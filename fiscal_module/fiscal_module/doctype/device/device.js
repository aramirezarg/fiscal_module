// Copyright (c) 2020, CETI and contributors
// For license information, please see license.txt

frappe.ui.form.on("Device", "refresh", function(frm) {
    frm.fields_dict['fiscal_document'].grid.get_field('fiscal_document').get_query = (doc, cdt, cdn) => {
        return {
            filters:[
                ['company', '=', frm.doc.company]
            ]
        }
    }
});