document.addEventListener("DOMContentLoaded", () => {
    rating();
})

function rating(){
    /**
     * Retrives the view's ratings array.
     * Maps Strings to Numbers + filters !Nan.
     * Calculates average percentage based on ratings and number of ratings.
     * Sets the rating bar's width to be the rating percentage.
     */
    const box = document.getElementById("rating-box");

    const initial = 0;
    let ratings = [...box.dataset.rating]
    ratings = ratings.map((x) => parseInt(x)).filter((x) => parseInt(x));
    const sum = ratings.reduce(
        (accumulator, currentValue) => accumulator + currentValue,
        initial
    );
    const length = ratings.length;
    const barWidth = (sum/length) * 10;
    document.getElementById("rating-amount").innerText = length;
    if (length == 0){
        document.getElementById("full-rating-review").innerHTML = 'No Reviews';
    }
    document.getElementById("rating-bar").style.width = `${barWidth}%`;
};