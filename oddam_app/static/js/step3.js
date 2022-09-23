function show_id() {
    const ids = get_checked_chexboxes();
    const params = new URLSearchParams();
    ids.forEach(id => params.append("type_ids", id))
    const address = '/get_inst_by_cat?' + params.toString();
    fetch(address)
        .then(response => response.text())
        .then(data => document.getElementById("inst").innerHTML = data);

}

function get_checked_chexboxes() {
    const markedCheckbox = document.querySelectorAll('input[type="checkbox"]:checked');
    const ids = [];
    markedCheckbox.forEach(box => ids.push(box.value));
    return ids;
}


$(document).ready(function () {
    const li_buttons = $('.checkboxy');
    li_buttons.click(show_id);
});
