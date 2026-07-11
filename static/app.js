function updateStars(rating) {

    let stars = document.querySelectorAll(".star");

    stars.forEach((star, index) => {

        if (index < rating) {
            star.textContent = "★";
        } 
        else {
            star.textContent = "☆";
        }

    });

    document.getElementById("rating-display").textContent =
        "Rating: " + rating + "/10";
}


function setRating(rating) {

    document.getElementById("rating").value = rating;

    updateStars(rating);
}


function hoverRating(rating) {

    updateStars(rating);

}


function resetRating() {

    let current =
        document.getElementById("rating").value;

    updateStars(current);

}


function notSeen() {

    document.getElementById("rating").value = -1;

    document.getElementById("rating-display").textContent =
        "Haven't Seen";

    let stars = document.querySelectorAll(".star");

    stars.forEach(star => {
        star.textContent = "☆";
    });

}

window.onload = function () {

    const ratingInput =
        document.getElementById("rating");

    if (!ratingInput) return;

    const value =
        parseInt(ratingInput.value);

    if (value > 0) {
        setRating(value);
    }
};