/**
 * Created by cwh on 2017/2/20.
 */
function need_clean() {
    var today = new Date();
    if(today.getMonth() == 7 || today.getMonth() == 8 || today.getMonth() == 1 || today.getMonth() == 2) {
        document.getElementById('clean_form').style.display = 'block';
    } else {
        document.getElementById('clean_form').style.display = 'none';
    }
}

need_clean();