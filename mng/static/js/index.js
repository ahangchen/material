/**
 * Created by cwh on 16-2-12.
 */
function onNavItemClick(e) {
    var navItems = document.getElementsByTagName('li');
    var navItem;
    var i = 0;
    for (; i < navItems.length; i++) {
        navItem = navItems[i];
        if (navItem.className == "active") {
            navItem.className = null;
            //break;
        } else if (e.target.parentNode.isSameNode(navItem)) {
            navItem.className = "active";
        }
    }
}

function changeContent(url) {
    var content_frame = document.getElementById("content-frame");
    content_frame.setAttribute("src", url);
}

function view(e) {
    onNavItemClick(e);
    var today = new Date();
    changeContent(today.getFullYear() + '/' + (today.getMonth() + 1) + '/' + today.getDate() + '/' + "view");
}

function apply(e) {
    onNavItemClick(e);
    changeContent("apply");
}

function faq(e) {
    onNavItemClick(e);
    changeContent("faq");
}

function download(e) {
    onNavItemClick(e);
    changeContent("download");
}

function publish(e) {
    onNavItemClick(e);
    changeContent("publish");
}

function setting(e) {
    onNavItemClick(e);
    changeContent("setting");
}

function export_xls(e) {
    onNavItemClick(e);
    changeContent("export_html");
}

function createXMLHttpRequest() {
    var xml_request;
    if (window.XMLHttpRequest) {
        xml_request = new XMLHttpRequest();
        if (xml_request.overrideMimeType)
            xml_request.overrideMimeType('text/xml');
    } else if (window.ActiveXObject) {
        try {
            xml_request = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            try {
                xml_request = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (e) {
            }
        }
    }
    return xml_request;
}

window.onbeforeunload = function () {
    var xml_request = createXMLHttpRequest();
    var url_header = 'http://' + window.location.host + '/';
    var url = url_header + "backup";
    xml_request.open("GET", url, true);// 异步处理返回
    xml_request.setRequestHeader("Content-Type",
        "application/x-www-form-urlencoded;");
    xml_request.send();
};