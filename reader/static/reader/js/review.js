document.addEventListener("DOMContentLoaded", () => {
    fill_review();
})

function fill_review(){
    /**
     * Retrieves all relevant fields for amendment.
     * Filters list of options for selected and relevant field.
     * Removes/Adds 'selected' attribute as appropriate.
     * Sets placeholders.
     */
    const review_rating_field = document.getElementById("id_rating");
    const book_title = document.getElementById("reviewForm").dataset.bookTitle;

    const option = [...document.getElementsByTagName("option")].filter(option => option.hasAttribute("selected"))[0];
    const relevant_option = [...document.getElementsByTagName("option")].filter(option => option.innerText.includes(`${book_title}`))[0];

    if (option.hasAttribute("selected")){
        option.removeAttribute("selected");
    }

    relevant_option.setAttribute("selected", "selected");
    review_rating_field.value = 6;
}