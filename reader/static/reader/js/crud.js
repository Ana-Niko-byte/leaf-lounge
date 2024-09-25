document.addEventListener("DOMContentLoaded", () => {
    const slider = document.getElementById("review-slide");
    displayForm(slider);
    handleCancel(slider);
});

function displayForm(slider){
    const editButtons = [...document.getElementsByClassName("btn-edit")];
    for (let button of editButtons){
        handleLoop(button, slider);
    }
}

function handleLoop(button, slider){
    /**
     * Handles the display of the 'Edit' form based on the button clicked.
     */
    button.addEventListener('click', function(e){
        e.preventDefault();
        const reviewId = button.dataset.reviewId;

        // Display the form
        if (slider.classList.contains("d-none")){
            slider.classList.remove("d-none");
            slider.classList.add("d-flex");
        }

        enterFormDetails(reviewId, button);
    });
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
    });
}

function enterFormDetails(reviewId, button){
    /**
     * Retrieves necessary values and sets them into the Review form for editing.
     * 
     * Sets retrieved review values and sets them into the appropriate form fields.
     * Dynamically sets the update_review URL.
     */
    const form = document.getElementById("re-review");
    const title = button.dataset.reviewTitle;
    const comment = button.dataset.reviewComment;
    const rating = button.dataset.reviewRating;

    const formTitle = document.getElementById("id_title");
    const formRating = document.getElementById("id_rating");
    const formComment = document.getElementById("id_comment");

    formTitle.value = title;
    formRating.value = rating;
    formComment.value = comment;

    form.setAttribute("action", `update_review/${reviewId}/`);
}