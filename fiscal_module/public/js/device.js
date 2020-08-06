class CurrentDevice {
    constructor() {
        this.id = null;
        this.url_manage = "fiscal_module.fiscal_module.api.";
        this.components = [];
        this.construct();
    }

    construct() {
        this.set_device_id();
    }

    send_device_id_to_server(){
        frappe.call({
            method: this.url_manage + "set_device_id",
            args: {
                device_components: this.get_components()
            },
            always: (r) => {
                this.id = r.message;
            },
        });
    }

    set_device_id(){
        setTimeout(() => {
            Fingerprint2.get((components) => {
                this.components = components;
                this.send_device_id_to_server()
            })
        },0)
    }

    get_components(){
        let joined_components = [];
        this.components.forEach((component) => {
            let value = typeof component.value == "object" ? component.value.join() : component.value
            joined_components.push({key: component.key, value: value.length > 100 ? value.substring(0, 100) : value});
        })
        return joined_components;
    }
}

Device = new CurrentDevice();