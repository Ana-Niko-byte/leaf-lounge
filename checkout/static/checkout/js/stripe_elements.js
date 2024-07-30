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
    // Prevents automatic submission.
    e.preventDefault();
    
    // Prevents multiple submissions by disabling Stripe card element and submit button.
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);

    // Triggers loading symbol.
    $('#book-payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // Retrieves Boolean save info checkbox (as it cannot be put directly into Stripe's paymentIntent),
    //csrf token (POST request), and gathers data for posting to URL.
    var saveInfo = Boolean($('#save-info').attr('checked'));
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    }

    // Creates URL to post to.
    var url = 'cache_checkout_data/';

    // Posts data to URL and updates PaymentIntent and returns 200 HttpResponse.
    // After POST, confirms card using Stripe's ConfirmCardPayment method.
    // If error, overlay hidden and form re-enabled with error display.
    $.post(url, postData).done(function(){
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details:{
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.street_1.value),
                        line2: $.trim(form.street_2.value),
                        city: $.trim(form.town_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping:{
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address:{
                    line1: $.trim(form.street_1.value),
                    line2: $.trim(form.street_2.value),
                    city: $.trim(form.town_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            },
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
    }).fail(function(){
        // Reload page to display error message from .views.py.
        location.reload();
    });
});