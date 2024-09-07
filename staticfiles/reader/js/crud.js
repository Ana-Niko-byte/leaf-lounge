document.addEventListener("DOMContentLoaded", () => {
    const slider = document.getElementById("review-slide");
    displayForm(slider);
    handleCancel(slider);
})

function displayForm(slider){
    const editButtons = [...document.getElementsByClassName("btn-edit")];
    for (let button of editButtons){
        button.addEventListener('click', function(e){
            e.preventDefault();
            const reviewId = button.dataset.reviewId;

            // Display the form
            if (slider.classList.contains("d-none")){
                slider.classList.remove("d-none");
                slider.classList.add("d-flex");
            }

            enterFormDetails(reviewId, button);
        })
    }
}

function handleCancel(slider){
    /**
     * Handles the user clicking the cancel button.
     * 
     * Attaches a "click" event to the button with Id "cancelReview".
     * If the slider is shown, removes Bootstrap "d-flex" class and adds "d-none" class.
     */
    document.getElementById("cancelReview").addEventListener("click", () => {
        if (slider.classList.contains("d-flex")){
            slider.classList.remove("d-flex");
            slider.classList.add("d-none");
        }
    })
}

function enterFormDetails(reviewId, button){
    /**
     * Retrieves necessary values and sets them into the Review form for editing.
     * 
     * In dropdown, selects the appropriate book from the list and disables the input.
     * Sets retrieved review values and puts them into the appropriate form fields.
     * Dynamically sets the update_review URL.
     */
    const form = document.getElementById("re-review");
    const book = button.dataset.bookTitle;
    const title = button.dataset.reviewTitle;
    const comment = button.dataset.reviewComment;
    const rating = button.dataset.reviewRating;

    const formTitle = document.getElementById("id_title");
    const formRating = document.getElementById("id_rating");
    const formComment = document.getElementById("id_comment");

    const option = [...document.getElementsByTagName("option")].filter(option => option.hasAttribute("selected"))[0];
    const relevant_option = [...document.getElementsByTagName("option")].filter(option => option.innerText.includes(`${book}`))[0];

    if (option.hasAttribute("selected")){
        option.removeAttribute("selected");
    }

    relevant_option.setAttribute("selected", "selected");
    formTitle.value = title;
    formRating.value = rating;
    formComment.value = comment;

    form.setAttribute("action", `update_review/${reviewId}/`);
}