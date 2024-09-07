document.addEventListener("DOMContentLoaded", () => {
    fill_review();
    rating_fill();
})

function fill_review(){
    /**
     * Retrieves all relevant fields for amendment.
     * Filters list of options for selected and relevant field.
     * Removes/Adds 'selected' attribute as appropriate.
     * Sets placeholders.
     */
    const bookTitle = document.getElementById("reviewForm").dataset.bookTitle;

    const option = [...document.getElementsByTagName("option")].filter(option => option.hasAttribute("selected"))[0];
    const relevant_option = [...document.getElementsByTagName("option")].filter(option => option.innerText.includes(`${bookTitle}`))[0];

    if (option.hasAttribute("selected")){
        option.removeAttribute("selected");
    }

    relevant_option.setAttribute("selected", "selected");
}

function rating_fill(){
    /**
     * Retrives the user's book rating and sets the rating bar's width to be the rating as a percentage out of 10.
     */
    const rating_input = document.getElementById("id_rating");
    rating_input.addEventListener("change", () => {
        const barWidth = parseFloat(rating_input.value) * 10;
        document.getElementById("rating-bar-review").style.width = `${barWidth}%`;
    })
}
