// Stripe Form Setup
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret_key').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// Validation + Errors
card.addEventListener('change', function(event){
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
        <span class="icon" role="alert">
            <i class="fa fa-times" aria-hidden="true"></i>
        </span>
        <span>${event.error.message}</span>
        `
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Form Submission
var form = document.getElementById('book-payment-form');

form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Prevent multiple submissions.
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);

    // Loading Symbol
    $('#book-payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        // Handle Errors.
        if (result.error) {
            // Define and set errors on form.
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);

            // Loading Symbol
            $('#book-payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);

            // Re-enable card element and submit button.
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);

        } else {
        // Handle Successful Card Confirmation.
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});