document.addEventListener("DOMContentLoaded", () => {
    rating_fill();
});

function rating_fill(){
    /**
     * Retrives the user's book rating and sets the rating bar's width to be the rating as a percentage out of 10.
     */
    const rating_input = document.getElementById("id_rating");
    rating_input.addEventListener("change", () => {
        const barWidth = parseFloat(rating_input.value) * 10;
        document.getElementById("rating-bar-review").style.width = `${barWidth}%`;
    });
}
