// accordion
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function () {
        var panel = this.nextElementSibling;
        if (panel.style.display === "flex") {
            panel.style.display = "none";
            this.style.paddingBottom = "0px"
            this.style.borderBottom = "none"
        } else {
            panel.style.display = "flex";
            this.style.paddingBottom = ""
        }

        // rotate icon
        var dropdownIcon = this.querySelector(".dropdown-icon");
        dropdownIcon.classList.toggle("rotate");
    });
}


// edit options
document.querySelectorAll('[contenteditable="true"]').forEach(label => {
    label.addEventListener('click', function (e) {
        e.preventDefault();
        this.focus();
    });
});
