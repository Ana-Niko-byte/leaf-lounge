export function displayError(string, bookId){
    /**
     * Sets the styling and innerHTML of the error.
     */
    document.getElementById(`qty_warning_${bookId}`).innerHTML= string;
    document.getElementById(`qty_warning_${bookId}`).style.color='red';
}