document.addEventListener("DOMContentLoaded", () => {
    const reviews = [...document.getElementsByClassName("review-container")];
    for (let review of reviews){
        const reviewRating = review.dataset.reviewRating;
        const loopCount = review.dataset.count;
        document.getElementById(`rating-bar-detail-${loopCount}`).style.width = `${(reviewRating * 10)}%`;
    }
});