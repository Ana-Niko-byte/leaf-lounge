export function displayError(string, bookId, counter){
    /**
     * Sets the styling and innerHTML of the error.
     */
    document.getElementById(`qty_warning_${bookId}_${counter}`).innerHTML= string;
    document.getElementById(`qty_warning_${bookId}_${counter}`).style.color='red';
}

export function returnBookId(button){
    /**
     * Returns the id of the book for individual form handling.
     */
    return button.dataset.bookId;
}