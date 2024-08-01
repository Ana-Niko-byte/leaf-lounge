document.addEventListener('DOMContentLoaded', function(){
    let country = $('#id_default_country').val();
    if (!country){
        $('#id_default_country').css('color', '#aab7c4');
    }
    $('#id_default_country').change(function(){
        country = $(this).val();
        if (!country){
            $(this).css('color', '#aab7c4');
        } else {
            $(this).css('color', '#000');
        }
    });
});