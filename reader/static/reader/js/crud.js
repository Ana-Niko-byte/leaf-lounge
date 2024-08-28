document.addEventListener("DOMContentLoaded", () => {
    edit_review();
})
// Edit Reviews
function edit_review(){
    const editButtons = [...document.getElementsByClassName("btn-edit")];
    const slider = document.getElementById("review-slide");

    for (let button of editButtons){
        button.addEventListener('click', function(e){
            e.preventDefault();

            if (slider.classList.contains("d-none")){
                slider.classList.remove("d-none");
                slider.classList.add("d-block");
                enterFormDetails(button);
            } else if (slider.classList.contains("d-block")){
                slider.classList.remove("d-block");
                slider.classList.add("d-none");
            }
        })
    }
}

function enterFormDetails(button){
    const reviewId = button.dataset.reviewId;
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