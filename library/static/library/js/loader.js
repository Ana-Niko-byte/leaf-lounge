document.addEventListener("DOMContentLoaded", () => {
    rating();
})

function rating(){
    /**
     * Retrives the book rating and sets the rating bar's width to be the rating as a percentage out of 10.
     */
    const box = document.getElementById("rating-box");
    const barWidth = parseFloat(box.dataset.rating) * 10;
    document.getElementById("rating-bar").style.width = `${barWidth}%`;
    document.getElementById("rating-mark").innerHTML = box.dataset.rating;
};