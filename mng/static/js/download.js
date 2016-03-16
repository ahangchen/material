/**
 * Created by cwh on 16-2-13.
 */
//
//function docDownload() {
//    if (this.id == "doc0") {
//
//    }
//}
//
//window.onload = function(){
//    var docBtns = document.getElementsByTagName("button");
//    var i =docBtns.length;
//    for (;i--;) {
//        console.log(i);
//        docBtns[i].onclick = docDownload;
//    }
//};

function changeFileName(elem) {
    var file_path_splits = elem.value.split("\\");
    elem.nextElementSibling.value = file_path_splits[file_path_splits.length - 1];
    elem.nextSibling.data = file_path_splits[file_path_splits.length - 1];
    console.log("test");
}

function validateRemove(doc_id) {
    var r = confirm("真的要删除吗？");
    if (r) {
        location.href = "../../" + doc_id + "/rm_doc";
    }
}

function checkUpload() {
    if (document.getElementById("upload_file").value != "") {
        return true;
    } else {

        return false;
    }
    return
}