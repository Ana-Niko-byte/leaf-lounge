document.addEventListener("DOMContentLoaded", () => {
    /**
     * Function for incrementing/decrementing the quantity of books to be ordered.
     * 
     * Method:
     * On DOM content load, retrieves the "decrement" and "increment" buttons.
     * Retrieves the current value of the input element with class "qty_input".
     * Attaches a "click" event listener to each button and increments/decrements the value as needed.
     * Re-assigns the value back to the input element.
     * 
     * Displays error if user attempts to decrease quantity of books lower than 1.
     */

    const decrement_btn = document.getElementsByClassName('decrement')[0];
    const increment_btn = document.getElementsByClassName('increment')[0];

    let quantity = parseInt(document.getElementsByClassName('qty_input')[0].value);

    // Event Listeners
    decrement_btn.addEventListener('click', function(e){
        /**
         * Decreases value of 'qty_input' by 1.
         */
        e.preventDefault();
        quantity -= 1;

        determineError();
    });

    increment_btn.addEventListener('click', function(e){
        /**
         * Increases value of 'qty_input' by 1.
         */
        e.preventDefault();
        quantity += 1;

        determineError();
    });

    function determineError(){
        /**
         * Determines the display of the value error and disables buttons.
         */
        if (quantity > 0){
            // Resets value if there is an error displayed.
            resetError();
            // Resets buttons to enabled.
            decrement_btn.disabled = false;
            increment_btn.disabled = false;

            if (quantity > 98){
                increment_btn.disabled = true;
            }
        } else if (quantity < 2) {
            displayError();
            // Keeps the value of 'quantity' at 1 and prevents backstage decrement.
            quantity = 1;
            if (quantity <= 1){
                decrement_btn.disabled = true;
            }
        }
    }

    function displayError(){
        /**
         * Sets the styling and innerHTML of the error.
         */
        document.getElementById('qty_warning').innerHTML='Minimum quantity required to place order: 1';
        document.getElementById('qty_warning').style.color='red';
    }

    function resetError(){
        /**
         * Resets the styling and innerHTML of the error.
         */
        document.getElementById('qty_warning').innerHTML='';
        document.getElementsByClassName('qty_input')[0].value = quantity;
    }

});