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
            this.persistent_name();

            frappe.call({
                method: this.url_manage + "set_device_id",
                args: {device_id: this.id},
                always: (r) => {
                    console.log(r);
                },
            });

            setTimeout(() => {
                 frappe.call({
                    method: this.url_manage + "test_device_id",
                    //args: {device_id: this.id},
                    always: (r) => {
                        console.log(r);
                    },
                });
            },2000)
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

    persistent_name() {
        let date = new Date();
        date.setTime(date.getTime() + (100*24*60*60*1000));
        let expires = "; expires=" + date.toUTCString();

        document.cookie = `device_id=${this.id} ${expires} ; path=/`;
    }

    get_persistent_name() {
        let nameEQ ="device_id=";
        let ca = document.cookie.split(';');
        for(let i=0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)===' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length,c.length);
        }
        return null;
    }
}
Device = new CurrentDevice();