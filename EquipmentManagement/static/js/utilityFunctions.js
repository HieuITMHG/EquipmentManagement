function onClose(){
    document.getElementById("alert").style.display = "none";
}

function toggle_pending() {
    const pending_btn = document.getElementById('btn-pending')
    const history_btn = document.getElementById('btn-history')
    document.getElementById('pending').classList.remove('hidden');
    document.getElementById('history').classList.add('hidden');
    pending_btn.classList.add('bg-white')
    history_btn.classList.remove('bg-white')
}

function toggle_history() {
    const pending_btn = document.getElementById('btn-pending')
    const history_btn = document.getElementById('btn-history')
    document.getElementById('pending').classList.add('hidden');
    document.getElementById('history').classList.remove('hidden');
    pending_btn.classList.remove('bg-white')
    history_btn.classList.add('bg-white')
}

function show_detail(detailId) {
    // Find the element with the given ID
    var detailElement = document.getElementById(detailId);
    detailElement.classList.remove('hidden');
    detailElement.classList.add('flex');
}

function close_detail(detailId) {
    console.log(detailId);
    const detailElement = document.getElementById(detailId);
    detailElement.classList.remove('flex');
    detailElement.classList.add('hidden');
}