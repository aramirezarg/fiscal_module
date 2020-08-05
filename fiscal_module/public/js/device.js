class CurrentDevice {
    constructor() {
        this.id = null;
        this.url_manage = "fiscal_module.fiscal_module.api.";
        this.components = [];
        this.construct();
    }

    construct() {
        this.send_device_id_to_server();
    }

    send_device_id_to_server(){
        this.set_device_id();

        if(this.id != null){
            frappe.call({
                method: this.url_manage + "set_device_id",
                args: {
                    device_id: this.id,
                    //current_device_id: frappe.get_cookie("device_id")
                },
                always: (r) => {
                    console.log(r);
                },
            });
        }else{
            setTimeout(() => {
                this.send_device_id_to_server();
            }, 0)
        }
    }

    excludes_components(){
        return {
            userAgent: true,
            language: true,
            fonts: true,
            adBlock: true,
            plugins: true,
            enumerateDevices: true
        }
    }

    set_device_id(){
        let options = {
            excludes: this.excludes_components()
        }

        setTimeout(() => {
            Fingerprint2.get(options, (components) => {
                this.components = components;

                this.id = Fingerprint2.x64hash128(components.map((pair) => {
                    return pair.value
                }).join(), 31)
            })
        },0)
    }
}
Device = new CurrentDevice();