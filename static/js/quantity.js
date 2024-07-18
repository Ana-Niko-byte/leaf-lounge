import { displayError } from './module.js';

document.addEventListener("DOMContentLoaded", () => {
    /**
     * Increments/decrements the quantity of books to be ordered.
     * 
     * Method:
     * On DOM content load, retrieves the "decrement" and "increment" buttons.
     * Retrieves the current value of the input element with class "qty_input".
     * Attaches a "click" event listener to each button and increments/decrements the value as needed.
     * Re-assigns the value back to the input element.
     * 
     * Displays errors if user attempts to decrease quantity of books lower than 1 or increase over 99.
     */

    const iButtons = document.getElementsByClassName('increment');

    function returnBookId(button){
        /**
         * Returns the id of the book for individual form handling.
         */
        return button.dataset.bookId;
    }

    for (let i of iButtons){
        /**
         * Increases value of 'qty_input' by 1.
         */
        i.addEventListener('click', function(e){
            e.preventDefault();

            let bookId = returnBookId(i);

            // Retrieves the value of the quantity input field.
            let quantity = returnQuantity(bookId);
            
            quantity += 1;
            document.getElementById(`book_id_${ bookId }`).value = quantity;
            // Error handling.
            determineError(bookId, quantity);
        });
    }

    function determineError(bookId, quantity){
        /**
         * Determines the display of the value error and disables buttons.
         */

        const increment_btn = document.getElementById(`increment_${ bookId }`);

        if (quantity > 0){
            // Resets value if there is an error displayed.
            resetError(bookId, quantity);

            // Resets buttons to enabled.
            increment_btn.disabled = false;

            if (quantity > 98){
                increment_btn.disabled = true;
                displayError('Maximum quantity allowed: 99', bookId);
            }
        // Does it really though?
        } else if (quantity < 2) {
            displayError('Minimum quantity required: 1', bookId);
            // Keeps the value of 'quantity' at 1.
            quantity = 1;
        }
    }

    // export function displayError(string, bookId){
    //     /**
    //      * Sets the styling and innerHTML of the error.
    //      */
    //     document.getElementById(`qty_warning_${bookId}`).innerHTML= string;
    //     document.getElementById(`qty_warning_${bookId}`).style.color='red';
    // }

    function resetError(bookId, quantity){
        /**
         * Resets the styling and innerHTML of the error.
         */
        document.getElementById(`qty_warning_${bookId}`).innerHTML='';
        document.getElementsByClassName('qty_input')[0].value = quantity;
    }
});

    function returnQuantity(bookId){
        /**
         * Fetches book Id for individual form handling.
         * 
         * Returns: (int) : The integer value of the current book amount in basket.
         */
        let quantity = parseInt(document.getElementById(`book_id_${ bookId }`).value);
        return quantity;
    }