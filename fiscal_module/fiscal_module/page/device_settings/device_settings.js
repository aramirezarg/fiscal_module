frappe.pages['Device Settings'].on_page_load = function (wrapper) {
     frappe.ui.make_app_page({
         parent: wrapper,
         title: __('Device Settings'),
         single_column: true,
     });

     setTimeout(() => {
         wrapper.device_settings = new DeviceManage(wrapper);
     }, 0)
}

frappe.pages['Device Settings'].refresh = function(wrapper) {
	if (wrapper.device_settings) {
	    wrapper.device_settings.make();
	}
}

DeviceManage = class DeviceManage {
    constructor(wrapper) {
        this.page = wrapper.page;
        this.base_wrapper = $(wrapper);
        this.wrapper = $(wrapper).find('.layout-main-section');
        this.edit_form = null;
        this.has_device = false;
        this.settings = "";
        this.no_device = "";
        this.url_manage = "fiscal_module.fiscal_module.page.device_settings.device_settings.";

        const assets = [
            'assets/ceti/js/ceti-modal.js',
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
                    this.has_device = r.has_device;
                    if(this.has_device){
                        this.doc = r.doc;
                        this.settings = r.settings;
                    }else{
                        this.no_device = r.no_device;
                    }

					this.prepare_dom();
                    this.add_actions();
				});
            },
            () => {
                frappe.dom.unfreeze();
            }
        ]);
    }

    get_device(){
		return frappe.xcall(this.url_manage + "get_device", {device: Device.id})
    }

    add_actions() {
		this.page.show_menu()

        this.page.add_menu_item(__("Device List"), () => {
			frappe.set_route('List/Device/List');
		}, true)

        this.page.add_menu_item(__("Refresh"), () => {
			this.make();
		}, true)

        if(this.has_device){
            this.page.set_primary_action(__('Setting'), () => {
                this.update();
            });
        }else{
            this.page.set_primary_action(__('Set Setting'), () => {
                Device.connect().then(() => {
                    this.make();
                });
            });
        }
	}

    prepare_dom() {
        if(this.has_device) {
            this.wrapper.empty().append(`
                <div class="device-container">
                    <div class="components-container">
                        <div class="settings-container"></div>
                        <div class="network-device">
                            <div class="control-input-wrapper">
                                <div class="control-value like-disabled-input for-description">
                                    <div class="ql-editor read-mode">
                                        ${this.has_device ? this.doc.string_components : "<h1>None</h1>"}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `);

            $(".settings-container").empty().append(this.settings)
        }else{
            this.wrapper.empty().append(`
                <div class="device-container">
                    <div class="components-container">
                        <div class="settings-container">${this.no_device}</div>
                    </div>
                </div>`
            )
        }
    }

    update(){
        if(this.edit_form == null) {
			this.edit_form = new CETIForm({
				doctype: "Device",
				docname: Device.id,
				form_name: "device",
                after_load: () => {
				    this.edit_form.form.field_group.fields_dict['fiscal_document'].grid.get_field('fiscal_document').get_query = (doc, cdt, cdn) => {
                        return {
                            filters:[
                                ['company', '=', this.edit_form.form.get_value("company")]
                            ]
                        }
                    }
                },
				call_back: () => {
					this.edit_form.hide();
					this.make();
					setTimeout(() => {
					    this.base_wrapper.find(".page-head").removeClass("hide");
                    }, 0)

				},
				title: __(`Update Device`),
			});
		}else{
			this.edit_form.show();
		}
    }
}