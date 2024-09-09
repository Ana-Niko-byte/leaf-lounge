document.addEventListener("DOMContentLoaded", () => {
    handleFormDisplays();
});

function handleFormDisplays(){
    /**
     * Retrieves the subscribe toggler from the footer and attaches a change listener.
     * Calls the appropriate functions for handling the displays of the subscribe and unsubscribe forms.
     */
    const subscribeSwitch = document.getElementById("subscribe-unsubscribe");
    subscribeSwitch.addEventListener("change", function() {
        const subscribeForm = document.getElementsByClassName("subscribe-form")[0];
        const unsubscribeForm = document.getElementsByClassName("unsubscribe-form")[0];
        if (this.checked){
            handleChecked(subscribeForm, unsubscribeForm);
        } else {
            handleUncheck(subscribeForm, unsubscribeForm);
        }
    });
}

function handleChecked(subForm, unsubForm){
    /**
     * Handles the form displays based for the 'Unsubscribe' form.
     * If the subscribe form is visible, removes the Bootstrap5 visibility class.
     * If the unsubscribe form is hidden, removes the Bootstrap5 invisibility class.
     * Adds the relevant classes to display the unsubscribe form and hide the other.
     */
    if (subForm.classList.contains('d-flex')){
        subForm.classList.remove('d-flex');
    }

    if (unsubForm.classList.contains('d-none')){
        unsubForm.classList.remove('d-none');
    }

    subForm.classList.add('d-none');
    unsubForm.classList.add('d-flex');
}

function handleUncheck(subForm, unsubForm){
    /**
     * Handles the form displays based for the 'Subscribe' form.
     * If the subscribe form is hidden, removes the Bootstrap5 invisibility class.
     * If the unsubscribe form is visible, removes the Bootstrap5 visibility class.
     * Adds the relevant classes to display the subscribe form and hide the other.
     */
    if (subForm.classList.contains('d-none')){
        subForm.classList.remove('d-none');
    }

    if (unsubForm.classList.contains('d-flex')){
        unsubForm.classList.remove('d-flex');
    }

    subForm.classList.add('d-flex');
    unsubForm.classList.add('d-none');
}