document.addEventListener("DOMContentLoaded", () => {
    /**
     * Handles update/delete functionality of books in the basket.
     */

    // Update Book Quantity in Basket.
    const update_btns = document.getElementsByClassName('update-book');
    for (let button of update_btns){
        // Iterates over each update button visible in the template and executes styling code 
        // + displays buttons for form handling.
        button.addEventListener('click', function(e){
            e.preventDefault();
            // Set quantity value to input field 'value'.
            const bookId = button.dataset.bookId;
            const actualQTY = document.getElementById(`quantity_${bookId}`);

            // Styling
            const inputFields = document.getElementById(`form_${bookId}`);
            const cancel = document.getElementById(`cancel_${bookId}`);
            const save = document.getElementById(`save_${bookId}`);

            // Toggle form visibility instead of url redirect in template.
            cancelActions(cancel, button, save, inputFields, actualQTY);

            // Handle visibility of elements when form is displayed.
            handleStyling(cancel, button, save, inputFields, actualQTY);

            // Submit the relevant form.
            saveForm(save, bookId);
        });
    }
});

function cancelActions(cancelBtn, updateBtn, saveBtn, inputFields, actualQTY){
    /**
     * Handles the display of various buttons when the form is hidden.
     * 
     * Arguments:
     * cancelBtn - the 'Cancel' button.
     * updateBtn - the 'Update Quantity' button.
     * saveBtn - the 'Save Changes' button.
     * inputFields - the group of input fields for book quantity.
     * actualQTY : string - the actual value of {{ book.quantity }}.
     */
    cancelBtn.addEventListener('click', function(e){
        e.preventDefault();
        cancelBtn.classList.add('d-none');
        inputFields.classList.remove('d-flex');
        inputFields.classList.add('d-none');
        actualQTY.classList.remove('d-none');

        updateBtn.classList.remove('d-none');
        saveBtn.classList.add('d-none');
    });
}

function handleStyling(cancelBtn, updateBtn, saveBtn, inputFields, actualQTY){
    /**
     * Handles the display of various buttons when the form is displayed.
     * 
     * Arguments:
     * cancelBtn - the 'Cancel' button.
     * updateBtn - the 'Update Quantity' button.
     * saveBtn - the 'Save Changes' button.
     * inputFields - the group of input fields for book quantity.
     * actualQTY : string - the actual value of {{ book.quantity }}.
     */
    // Display 'cancel' button when form is displayed.
    cancelBtn.classList.remove('d-none');

    // Display input inputFields.
    inputFields.classList.remove('d-none');
    inputFields.classList.add('d-flex');
    actualQTY.classList.add('d-none');

    // Display 'save' button instead of 'update' button.
    updateBtn.classList.add('d-none');
    saveBtn.classList.remove('d-none');
}

function saveForm(saveBtn, bookId){
    /**
     * Saves the relevant quantity form.
     * 
     * Arguments:
     * saveBtn - the 'Save Changes' button.
     * bookId - the unique id of the book being updated.
     */
    saveBtn.addEventListener('click', function(e){
        e.preventDefault();
        document.getElementById(`update_form_${bookId}`).submit();
    });
}