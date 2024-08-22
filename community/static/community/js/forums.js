
document.addEventListener("DOMContentLoaded", () => {
    log_entry();
});

function log_entry(){
    /**
     * Changes the display and innerHTML of the 'Start Discussion' button and form.
     */
    const button = document.getElementById('start-forum');
    button.addEventListener('click', function(){
        const form = document.getElementById('forumForm');
        if (form.classList.contains('d-none')){
            form.classList.remove('d-none');
            form.classList.add('d-flex');
            button.innerHTML = '<i class="fa-solid fa-sm fa-x me-2"></i>Cancel';
        } else if (form.classList.contains('d-flex')){
            form.classList.remove('d-flex');
            form.classList.add('d-none');
            button.innerHTML = '<i class="fa-solid fa-plus me-2"></i>Start a Discussion';
        }
    });
}
