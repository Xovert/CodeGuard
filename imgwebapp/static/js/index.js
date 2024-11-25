document.getElementById("change-tab").addEventListener("click", function () {
    var targetPaneId = this.getAttribute('data-target')
    var targetTabId = this.getAttribute('tab-target')
    var activeTab = document.querySelector('.tab-pane.active')
    var activeButton = document.querySelector('.nav-link.active')
    var targetTab = document.querySelector(targetTabId)
    var targetPane = document.querySelector(targetPaneId)

    document.querySelectorAll('.tab-pane').forEach(function(tab){
        tab.classList.remove('active', 'show')
    })

    document.querySelectorAll('.nav-link').forEach(function(link){
        link.classList.remove('active')
    })

    targetTab.classList.add('active')
    targetPane.classList.add('show', 'active')
})

$(document).ready(function(){
    $("#Error").modal('toggle');
});

function handleFileChange(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const image = document.querySelector('.profile-picture');
            image.src = e.target.result; // Update the image source
        };
        reader.readAsDataURL(file);
    }
}


function handleFileChange(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const image = document.querySelector('.profile-picture');
            image.src = e.target.result; // Update the image source
        };
        reader.readAsDataURL(file);
    }
}


function handleFileChange(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const image = document.querySelector('.profile-picture');
            image.src = e.target.result; // Update the image source
        };
        reader.readAsDataURL(file);
    }
}


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

// for navbar showing and hiding
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-72px";
  }
  prevScrollpos = currentScrollPos;
}