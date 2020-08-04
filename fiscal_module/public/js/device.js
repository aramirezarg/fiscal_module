window["device_id"] = null;
window["deviceComponents"] = [];

function DeviceInfo() {
    let options = {
        excludes: {
            userAgent: true,
            language: true,
            fonts: true,
            adBlock: true,
            plugins: true,
            enumerateDevices: true
        }
    }

    setTimeout(() => {
        Fingerprint2.get(options, function (components) {
            window["deviceComponents"] = components;

            window["device_id"] = Fingerprint2.x64hash128(components.map(function (pair) {
                return pair.value
            }).join(), 31)

            set_device_id();
        })
    },0)

}

function set_device_id(){
    if(window["device_id"] != null){
         console.log("client device id: " + window["device_id"])
        let url_manage = "fiscal_module.fiscal_module.api.";

        frappe.call({
            method: url_manage + "set_device_id",
            args: {device_id: window["device_id"]},
            always: (r) => {
                console.log(r);
            },
        });
    }else{
        setTimeout(() => {
            set_device_id();
        }, 0)
    }


}

if (window.requestIdleCallback) {
    requestIdleCallback(DeviceInfo);
    //requestIdleCallback(set_device_id);
} else {
   setTimeout(DeviceInfo, 0);
   //setTimeout(set_device_id, 0);
}