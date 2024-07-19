// This file handles the increment and decrement of book quantities in the library app as basket uses counters.

document.addEventListener("DOMContentLoaded", () => {
    const iButtons = [...document.getElementsByClassName('library-increment')];
    const dButtons = [...document.getElementsByClassName('library-decrement')];

    for (let i of iButtons){
        i.addEventListener('click', function(e){
            e.preventDefault();

            const bookId = i.dataset.bookId;
            let quantity = parseInt(document.getElementById(`book_id_${bookId}`).value);
            quantity += 1;

            determineError(bookId, quantity);

            document.getElementById(`book_id_${bookId}`).value = quantity;
        })
    }

    for (let d of dButtons){
        d.addEventListener('click', function(e){
            e.preventDefault();

            const bookId = d.dataset.bookId;
            let quantity = parseInt(document.getElementById(`book_id_${bookId}`).value);
            quantity -= 1;

            determineError(bookId, quantity);

            document.getElementById(`book_id_${bookId}`).value = quantity;
        })
    }

    function determineError(bookId, quantity){
        /**
         * Determines the display of the value error and disables buttons.
         */
    
        let increment_btn = document.getElementById(`increment_${ bookId }`);
        let decrement_btn = document.getElementById(`decrement_${ bookId }`);
        if (quantity > 0){
            // Resets value if there is an error displayed.
            resetError(bookId, quantity);
    
            // Resets buttons to enabled.
            increment_btn.disabled = false;
            decrement_btn.disabled = false;
    
        if (quantity > 98){
            increment_btn.disabled = true;
            displayError('Maximum quantity allowed: 99', bookId);
        }
        // Does it really though?
        } else if (quantity < 2) {
            displayError('Minimum quantity required: 1', bookId);
            // Keeps the value of 'quantity' at 1.
            quantity = 1;
            decrement_btn.disabled = true;
        }
    }
})

function displayError(string, bookId){
    /**
     * Sets the styling and innerHTML of the error.
     */
    document.getElementById(`qty_warning_${bookId}`).innerHTML= string;
    document.getElementById(`qty_warning_${bookId}`).style.color='red';
}

function resetError(bookId, quantity){
    /**
     * Resets the styling and innerHTML of the error.
     */
    document.getElementById(`qty_warning_${bookId}`).innerHTML='';
    console.log(document.getElementById(`qty_warning_${bookId}`).innerHTML);
    document.getElementsByClassName('qty_input')[0].value = quantity;
}