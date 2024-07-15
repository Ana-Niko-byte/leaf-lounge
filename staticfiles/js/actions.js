document.addEventListener("DOMContentLoaded", () => {
    /**
     * Handles update/delete functionality of books in the basket.
     */

    // Update Book Quantity in Basket.
    const update_btn = document.getElementsByClassName('update-book')[0];
    // Or best handle this logic in view?
    update_btn.addEventListener('click', function(e){
        document.getElementsByClassName('updateForm')[0].submit();
    });

    // Delete Books in Basket.
    const delete_btn = document.getElementsByClassName('delete-book')[0];
    // Or best handle this logic in view?
    delete_btn.addEventListener('click', function(e){
        e.preventDefault();
        console.log('you\'ve clicked the delete button');
        // Postpone until hardback/softback of books has been added to model
    });
});