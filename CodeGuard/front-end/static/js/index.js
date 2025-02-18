// SCROLL FUNCTION
$(document).ready(function () {
    // for all a tag
    $("a").on('click', function (event) {
        // if a tag is not empty
        if (this.hash !== "") {
            event.preventDefault();

            // Store hash
            var hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function () {
                window.location.hash = hash;
            });
        }
    });
});