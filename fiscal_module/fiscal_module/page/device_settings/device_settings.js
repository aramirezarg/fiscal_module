frappe.pages['Device Settings'].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('Loading device Data'),
        single_column: true,
    });

    setTimeout(() => {
        device_check(page, wrapper);
    }, 0)
}

function device_check(page, wrapper){
    setTimeout(() => {
        if(Device.id == null) {
            page.set_title(`${__("Loading device Info")}`)
            device_check();
        } else{
            page.set_title(`<strong>${__("Device")}</strong>: <small>${Device.id}</small>`)
            new DeviceManage(wrapper, page);
        }
    }, 200)
}


DeviceManage = class DeviceManage {
    constructor(wrapper, page) {
        this.page = page;
        this.base_wrapper = $(wrapper);
        this.wrapper = $(wrapper).find('.layout-main-section');
        this.edit_form = null;
        this.id = Device.id;
        this.head = "";
        this.url_manage = "fiscal_module.fiscal_module.page.device_settings.device_settings.";

        const assets = [
            'assets/ceti/js/jshtml-class.js',
            'assets/ceti/js/ceti-modal.js',
            'assets/ceti/js/ceti-api.js',
            'assets/ceti/js/ceti-form-class.js',
        ];

        frappe.require(assets, () => {
            this.make();
        });
    }

    make() {
        return frappe.run_serially([
            () => frappe.dom.freeze(),
            () => {
                this.get_device().then((r) => {
                    this.doc = r[0];
                    this.head = r[1];
					this.prepare_dom();
				});
            },
            () => {
                frappe.dom.unfreeze();
            },
            () => {
                this.add_actions();
            }
        ]);
    }

    get_device(){
		return frappe.xcall(this.url_manage + "get_device", {device: Device.id})
    }

    add_actions() {
		//this.page.show_menu()
        this.page.set_secondary_action(__('Device List'), () => {
			frappe.set_route('List/Device/List');
		});

        this.page.set_primary_action(__('Setting'), () => {
			this.update();
		});
	}

    prepare_dom() {
        let doc = frappe.get_doc("Device", this.id);
        let components = `
            <table class='table table-condensed table-bordered table-responsive'>
                <thead>
                    <h3>${__("Components")}</h3>
                </thead>
                <tbody>`;

        for (let index in Device.components) {
            if (!Device.components.hasOwnProperty(index)) continue;

            let obj = Device.components[index];
            components += `
                <tr>
                    <th>${obj.key}</th>
                    <td>${String(obj.value).substr(0, 100)}${obj.value.length > 100 ? '...' : ''}</td>
                </tr>`;
        }
        components += "</tbody></table>"

        this.wrapper.append(`
			<div class="device-container">
			    <div class="components-container">
			        ${this.head}
                    ${components}
                </div>
			</div>
		`);
    }

    update(){
        if(this.edit_form == null) {
			this.edit_form = new CETIForm({
				doctype: "Device",
				docname: this.id,
				form_name: "device",
                after_load: () => {
				    this.edit_form.form.field_group.fields_dict['fiscal_document'].grid.get_field('fiscal_document').get_query = (doc, cdt, cdn) => {
                        return {
                            filters:[
                                ['company', '=', "CETI"]
                            ]
                        }
                    }
                },
				call_back: ()=> {
					this.edit_form.hide();
					setTimeout(() => {
					    this.base_wrapper.find(".page-head").removeClass("hide");
                    }, 0)
				},
				title: __(`Update ${this.id}`),
			});
		}else{
			this.edit_form.show();
		}
    }
}