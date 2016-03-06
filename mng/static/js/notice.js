/**
 * Created by cwh on 16-3-1.
 */
function edit_notice(elem) {
    elem.parentNode.nextElementSibling.style.display = "block";
    elem.parentNode.style.display = "none";
}

function quit_edit(elem) {
    elem.parentNode.parentNode.parentNode.previousElementSibling.style.display = "block";
    elem.parentNode.parentNode.parentNode.style.display = "none";
}

function remove_notice(notice_id) {
    var r = confirm("真的要删除吗？");
    if (r) {
        location.href = "../../" + notice_id + "/remove_notice";
    }
}
