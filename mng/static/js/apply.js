/**
 * Created by cwh on 16-2-14.
 */
var liCount = 0;
function addLi() {
    console.log("add li called");
    var ul = document.getElementsByTagName("ul");
    var li = document.createElement("li");

    var labelYear = document.createElement("label");
    var labelMonth = document.createElement("label");
    var labelDay = document.createElement("label");
    labelYear.className = "year_time_input";
    labelMonth.className = labelDay.className = "time_label";
    labelYear.innerHTML = "年";
    labelMonth.innerHTML = "月";
    labelDay.innerHTML = "日";

    var inputYear = document.createElement("input");
    var inputMonth = document.createElement("input");
    var inputDay = document.createElement("input");
    inputYear.onfocus = highLight;
    inputMonth.onfocus = highLight;
    inputDay.onfocus = highLight;

    inputYear.className = "year_time_input";
    inputMonth.className = inputDay.className = "time_input";

    inputYear.name = "li_year_" + liCount;
    inputYear.id = "li_year_" + liCount;
    inputMonth.name = "li_month_" + liCount;
    inputMonth.id = "li_month_" + liCount;
    inputDay.name = "li_day_" + liCount;
    inputDay.id = "li_day_" + liCount;

    var rmBtn = document.createElement("button");
    rmBtn.className = "remove_time";
    rmBtn.innerHTML = "-";
    rmBtn.onclick = rmSelf;

    li.appendChild(inputYear);
    li.appendChild(labelYear);
    li.appendChild(inputMonth);
    li.appendChild(labelMonth);
    li.appendChild(inputDay);
    li.appendChild(labelDay);
    li.appendChild(rmBtn);
    ul[0].appendChild(li);
    liCount++;
    ul.value = liCount;
}

function rmSelf(element) {
    if (element instanceof MouseEvent) {
        this.parentNode.parentNode.removeChild(this.parentNode);
    } else {
        element.parentNode.parentNode.removeChild(element.parentNode);
    }
    liCount--;
}

var weekMode = false;
function changeIntervalMode() {
    weekMode = !weekMode;
    if (weekMode) {
        document.getElementById("time_interval_week").style.display = "block";
        document.getElementById("start_year").value = "";
        document.getElementById("start_month").value = "";
        document.getElementById("start_day").value = "";
        document.getElementById("end_year").value = "";
        document.getElementById("end_month").value = "";
        document.getElementById("end_day").value = "";
        document.getElementById("time_interval_day").style.display = "none";
        document.getElementById("time_interval_day").value = "";
        document.getElementById("interval_btn").innerHTML = "天";
    } else {
        document.getElementById("time_interval_week").style.display = "none";
        document.getElementById("time_interval_day").style.display = "block";
        document.getElementById("start_week").value = "";
        document.getElementById("end_week").value = "";
        document.getElementById("interval_btn").innerHTML = "周";
    }
}

function highLight(ipt) {
    var color = "#fff";
    if (isModify()) {
        color = "#eef"
    }
    if (ipt instanceof FocusEvent) {
        this.style.background = color;
    }
    else {
        ipt.style.background = color;
    }

}

function errorLight(ipt) {
    ipt.style.background = "#fee";
}

function validateDate(year, month, day) {
	return true;
    var date = new Date(year, month - 1, day);
    var strs = date.toLocaleDateString().split('/');
    return strs[0] == year && strs[1] == month && strs[2] == day;
}

function checkActName() {
    var act_name = document.getElementById("act_name");
    if (act_name.value == "" || act_name.value.length > 100) {
        errorLight(act_name);
        return false;
    }
    return true;
}
function checkApplicant() {
    var applicant = document.getElementById("applicant");
    if (applicant.value == "" || applicant.value.length > 50) {
        errorLight(applicant);
        return false;
    }
    return true;
}
function checkTel() {
    var tel = document.getElementById("tel");
    if (tel.value == "" || tel.value.length > 30) {
        errorLight(tel);
        return false;
    }
    return true;
}
function checkOrg() {
    var apply_org = document.getElementById("apply_org");
    if (apply_org.value == "" || apply_org.value.length > 50) {
        errorLight(apply_org);
        return false;
    }
    return true;
}
function checkChair() {
    var chair_num = document.getElementById("chair_num");
    if (chair_num.value == "") {
        chair_num.value = 0;
    }
    return true;
}
function checkDesk() {
    var desk_num = document.getElementById("desk_num");
    if (desk_num.value == "") {
        desk_num.value = 0;
    }
    return true;
}
function checkTent() {
    var tent_num = document.getElementById("tent_num");
    if (tent_num.value == "") {
        tent_num.value = 0;
    }
    return true;
}
function checkUmb() {
    var umbrella_num = document.getElementById("umbrella_num");
    if (umbrella_num.value == "") {
        umbrella_num.value = 0;
    }
    return true;
}
function checkRed() {
    var red_num = document.getElementById("red_num");
    if (red_num.value == "") {
        red_num.value = 0;
    }
    return true;
}
function checkCloth() {
    var cloth_num = document.getElementById("cloth_num");
    if (cloth_num.value == "") {
        cloth_num.value = 0;
    }
    return true;
}
function checkLoud() {
    var loud_num = document.getElementById("loud_num");
    if (loud_num.value == "") {
        loud_num.value = 0;
    }
    var priority = document.getElementById("priority");
    if (loud_num.value > 0 && priority.value == "1") {
        errorLight(priority);
        errorLight(loud_num);
        return false;
    }
    return true;
}
function checkSound() {
    var sound_num = document.getElementById("sound_num");
    if (sound_num.value == "") {
        sound_num.value = 0;
    }
    var priority = document.getElementById("priority");
    if (sound_num.value > 0 && priority.value == "1") {
        errorLight(priority);
        errorLight(sound_num);
        return false;
    }
    return true;
}
function checkProjector() {
    var projector = document.getElementById("projector");
    if (projector.value == "") {
        projector.value = 0;
    }
    var priority = document.getElementById("priority");
    if (projector.value > 0 && priority.value == "1") {
        errorLight(priority);
        errorLight(projector);
        return false;
    }
    return true;
}
var li_valid = false;
function checkStartTime() {
    if (weekMode) return true;
    var ret = true;
    var start_month = document.getElementById("start_month");
    if (start_month.value == "" && !li_valid) {
        errorLight(start_month);
        ret = false;
    }
    var start_day = document.getElementById("start_day");
    if (start_day.value == "" && !li_valid) {
        errorLight(start_day);
        ret = false;
    }
    var start_year = document.getElementById("start_year");
    if (start_year.value != "" && start_day.value != "" && start_month != "") {
        if (!validateDate(start_year.value, start_month.value, start_day.value)) {
            errorLight(start_month);
            errorLight(start_day);
            ret = false;
        }
    }
    return ret;
}
function checkEndTime() {
    if (weekMode) return true;
    var ret = true;
    var end_month = document.getElementById("end_month");
    if (end_month.value == "" && !li_valid) {
        errorLight(end_month);
        ret = false;
    }
    var end_day = document.getElementById("end_day");
    if (end_day.value == "" && !li_valid) {
        errorLight(end_day);
        ret = false;
    }
    var end_year = document.getElementById("end_year");
    if (end_year.value != "" && end_month.value != "" && end_day.value != "") {
        if (!validateDate(end_year.value, end_month.value, end_day.value)) {
            errorLight(end_month);
            errorLight(end_day);
            ret = false;
        }
    }
    return ret;
}
function checkLiTime() {
    var ret = true;
    var i = 0;
    var liDateYear, liDateMonth, liDateDay;
    for (; i < liCount; i++) {
        liDateYear = document.getElementById("li_year_" + i);
        liDateMonth = document.getElementById("li_month_" + i);
        liDateDay = document.getElementById("li_day_" + i);
        if (liDateYear.value != "" && liDateMonth.value != "" && liDateDay.value != "") {
            li_valid = true;
            if (!validateDate(liDateYear.value, liDateMonth.value, liDateDay.value)) {
                errorLight(liDateYear);
                errorLight(liDateMonth);
                errorLight(liDateDay);
                li_valid = false;
                ret = false;
            }
        }
    }
    return ret;
}

function sortLi() {
    var lis = document.getElementsByTagName('li');
    var i = 0;
    for (; i < lis.length; i++) {
        var date_items = lis[i].getElementsByTagName('input');
        date_items[0].name = 'li_year_' + i;
        date_items[0].id = 'li_year_' + i;
        date_items[1].name = 'li_month_' + i;
        date_items[1].id = 'li_month_' + i;
        date_items[2].name = 'li_day_' + i;
        date_items[2].id = 'li_day_' + i;
    }
}

function checkAssistant() {
    var assistant = document.getElementById("assistant");
    if (assistant.value == "" || assistant.value.length > 50) {
        errorLight(assistant);
        return false;
    }
    return true;
}

function checkParam() {
    sortLi();
    var ret = true;
    ret = ret && checkActName();
    ret = ret && checkApplicant();
    ret = ret && checkTel();
    ret = ret && checkOrg();
    ret = ret && checkAssistant();
    ret = ret && checkChair();
    ret = ret && checkDesk();
    ret = ret && checkTent();
    ret = ret && checkUmb();
    ret = ret && checkRed();
    ret = ret && checkCloth();
    ret = ret && checkLoud();
    ret = ret && checkSound();
    ret = ret && checkProjector();
    ret = ret && checkLiTime();
    if (!isModify()) {
        ret = ret && checkStartTime();
        ret = ret && checkEndTime();
    }

    if (!ret) {
        alert("输入内容有误，请检查红色部分");
    }
    return ret;
}

function isModify() {
    return window.location.toString().indexOf('apply_modify') != -1
}
window.onload = function () {
    if (isModify()) {

    } else {
        addLi();
        document.getElementById("start_year").value = new Date().getFullYear().toString();
        document.getElementById("end_year").value = new Date().getFullYear().toString();
    }

}
;
