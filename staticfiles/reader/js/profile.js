function handleFilteredElements(list){
    /**
     * Handles the display of the filtered list (unselected elements).
     * 
     * Arguments:
     * list : (array) : the list of unwanted elements with class 'profile-details'. 
     */
    for (let element of list){
        if (element.classList.contains('d-block')){
            element.classList.remove('d-block');
        } else if (!element.classList.contains('d-none')) {
            element.classList.add('d-none');
        }
    }
}

function handleChosenElement(element){
    /**
     * Handles the display of the filtered out element (selected element).
     * 
     * Arguments:
     * element : object : the selected element for display.
     */
    if (element.classList.contains('d-none')){
        element.classList.remove('d-none');
    } else if (!element.classList.contains('d-block')){
        element.classList.add('d-block');
    }
}

function hideStarter(){
    /**
     * Retrieves the 'profile-starter' element and hides it.
     */
    const starter = document.getElementsByClassName('profile-starter')[0];
    starter.classList.add('d-none');
}

function FilterAndDisplay(buttonDataValue){
    // Get list for filtering.
    let list = [...document.getElementsByClassName('profile-details')];

    // Retrieve the dataset value to filter out by and filter.
    // const buttonDataValue = button.dataset.detail;
    const filteredList = list.filter(
        (element) => element.dataset.profile !== `${buttonDataValue}-details`
    );

    // Retrieve the filtered out element. This will always be one element long.
    const filteredElement = list.filter(element => !filteredList.includes(element))[0];

    // Handle the display of filtered elements.
    handleFilteredElements(filteredList);

    // Handle the display of the filtered out element.
    handleChosenElement(filteredElement);
}

// Profile Ratings
function profile_fill(){
    /**
     * Retrives the user's book rating and sets the rating bar's width to be the rating as a percentage out of 10.
     */
    const reviews = document.getElementsByClassName("review");
    for (let review of reviews){
        const forloop = review.dataset.forloop;
        const box = document.getElementById(`profile-rating-box-${forloop}`);
        const barWidth = (box.dataset.rating) * 10;
        document.getElementById(`profile-rating-bar-${forloop}`).style.width = `${barWidth}%`;
    }
}

document.addEventListener('DOMContentLoaded', function(){
    // Change colour of placeholder in country field.
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

    // Hide/Display Profile Tabs (IIFE).
    const buttons = [...document.getElementsByClassName('display-button')];
    for (let button of buttons){
        (function(button){
            const buttonDataValue = button.dataset.detail;
            button.addEventListener('click', () => {
                hideStarter();
                FilterAndDisplay(buttonDataValue);
            });
        })(button);
    }

    // Star Ratings
    profile_fill();
});