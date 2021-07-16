class CurrentDevice {
    constructor() {
        this.id = frappe.get_cookie("device_id");
        this.url_manage = "fiscal_module.fiscal_module.api.";
        this.all_components = [];
        this.components = [];
        this.detail_components = [];
        this.string_components = "";
        this.check_local_device();
    }

    connect(){
        return new Promise(resolve => {
            this.set_device_id().then(() => {
                this.send_identifier_device_data().then(() => {
                    resolve();
                });
            });
        });
    }

    check_local_device(){
        if(this.has_id()){
            this.send_identifier_device_data().then();
        }
    }

    has_id(){
        return typeof this.id != "undefined" && this.id != null;
    }

    send_identifier_device_data() {
        return new Promise(resolve => {
            frappe.call({
                method: this.url_manage + "set_identifier_device_data",
                args: this.has_id() ? {
                    device_id: this.id
                } : {
                    device_components: this.components,
                    string_components: this.string_components,
                    detail_components: this.detail_components
                },
                always: (r) => {
                    this.id = r.message;
                    resolve();
                },
            });
        });
    }

    set_device_id() {
        return new Promise(resolve => {
            if (this.has_id()) {
                resolve();
            }else{
                return frappe.ui.form.qz_connect().then(() => {
                    this.listNetworkDevices().then(() => {
                        resolve();
                    });
                }).then((data) => {
                    return data;
                }).catch((err) => {
                    frappe.ui.form.qz_fail(err);
                });
            }
        });
    }

    listNetworkDevices() {
        return new Promise(resolve => {
            qz.networking.devices().then((data) => {
                this.set_string_components(data);
                data.map((item) => {
                    this.all_components.push({
                        key: item.mac,
                        value: `${item.hostname} ${item.name}`,
                    });

                    if (item.hasOwnProperty("mac") && item.primary) {
                        this.components.push({
                            key: item.mac,
                            value: `${item.hostname} ${item.name}`,
                        });

                        this.detail_components.push({
                            mac: item.mac,
                            host: item.hostname,
                            primary_device: item.name
                        });
                    }
                });

                resolve();
            }).catch();
        });
    }

    set_string_components(data) {
        let listItems = function(obj) {
            let html = '';
            let labels = { mac: 'MAC', ip: 'IP', up: 'Up', ip4: 'IPv4', ip6: 'IPv6', primary: 'Primary' };

            Object.keys(labels).forEach(function(key) {
                if (!obj.hasOwnProperty(key)) { return; }
                if (key !== 'ip' && obj[key] === obj['ip']) { return; }

                let value = obj[key];
                if (key === 'mac') { value = obj[key].match(/.{1,2}/g).join(':'); }
                if (typeof obj[key] === 'object') { value = value.join(', '); }

                html += '<li><strong>' + labels[key] + ':</strong> <code>' + value + '</code></li>';
            });

            return html;
        };

        let list = '';
        for (let i = 0; i < data.length; i++) {
            let info = data[i];

            if (i === 0) {
                list += "<li>" +
                    "   <strong>Hostname:</strong> <code>" + info.hostname + "</code>" +
                    "</li>" +
                    "<li>" +
                    "   <strong>Username:</strong> <code>" + info.username + "</code>"
                "</li>";
            }
            list += "<li>" +
                "   <strong>Interface:</strong> <code>" + (info.name || "UNKNOWN") + (info.id ? "</code> (<code>" + info.id + "</code>)" : "</code>") +
                "   <ul>" + listItems(info) + "</ul>" +
                "</li>";
        }

        this.string_components = "<strong>Network details:</strong><ul>" + list + "</ul>";
    }
}

Device = new CurrentDevice();