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
    let url_manage = "fiscal_module.fiscal_module.api.";
    if(window["device_id"] != null){
        setCookie("device_id", window["device_id"], (365*10));
        console.log("client device id: " + window["device_id"]);

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

    setTimeout(() => {
        frappe.call({
            method: url_manage + "test_device_id",
            always: (r) => {
                console.log(r);
            },
        });
    }, 2000)
}

if (window.requestIdleCallback) {
    requestIdleCallback(DeviceInfo);
    //requestIdleCallback(set_device_id);
} else {
   setTimeout(DeviceInfo, 0);
   //setTimeout(set_device_id, 0);
}

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}