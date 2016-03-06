/**
 * Created by cwh on 16-2-25.
 */
function detail(ele) {
    var detail_id = ele.value;
    document.getElementById(detail_id).style.display = 'table';
    ele.style.display = 'none';
    ele.nextElementSibling.style.display = 'inline-block';
}
function hide(ele) {
    var detail_id = ele.value;
    document.getElementById(detail_id).style.display = 'none';
    ele.style.display = 'none';
    ele.previousElementSibling.style.display = 'inline-block';
}
var cur_date_items;
function onDateClick(elem) {
    cur_date_items = elem.id.split("_");
    var cur_date = document.getElementById(cur_date_items[0] + "_" + cur_date_items[1] + "_" + cur_date_items[2]);
    cur_date.style.background = "#fff";
    elem.style.background = "#fee";
}

function apply_remove(apply_id) {
    var r = confirm("真的要删除吗？");
    if (r) {
        location.href = "../../../../" + apply_id + "/apply_remove";
    }
}

window.onload = function () {
    var calendar = document.getElementById("calendar");
    var dates = calendar.getElementsByTagName("td");
    cur_date_items = document.getElementById("cur_date").innerHTML.split("-");
    var i = 3;
    var date_td;
    var date_a;
    var td_date_items;
    for (; i < dates.length; i++) {
        date_td = dates[i];
        date_a = date_td.getElementsByTagName("a")[0];
        td_date_items = date_a.id.split("-");
        date_a.id = td_date_items[0] + "_" + td_date_items[1] + "_" + td_date_items[2];
        date_a.innerHTML = td_date_items[2];
        date_a.href = "../../../../" + date_a.id.replace(new RegExp("_", "gm"), "/") + "/view";
        if (cur_date_items[0] == td_date_items[0] && cur_date_items[1] == td_date_items[1] && cur_date_items[2] == td_date_items[2]) {
            date_td.style.background = "#fee";
        }
        if (cur_date_items[1] != td_date_items[1]) {
            date_a.style.color = "#999";
        }
    }
};