// ======= RESIZE TEXTAREA =======
function autoResize(textarea) {
    textarea.style.height = 'auto'; // Reset the height
    textarea.style.height = textarea.scrollHeight + 'px'; // Set the height to match the content
}

document.addEventListener("input", function (event) {
    if (event.target.tagName === "TEXTAREA") {
        autoResize(event.target);
    }
});



// ===== ACCORDION =====
document.addEventListener("click", function (event) {
    // Check if the clicked element has the 'accordion' class
    if (event.target.classList.contains("accordion")) {
        var panel = event.target.nextElementSibling;

        if (panel.classList.contains("close")) {
            panel.classList.remove("close");
            event.target.classList.remove("border-bottom-none");
        } else {
            panel.classList.add("close");
            event.target.classList.add("border-bottom-none");
        }

        // Rotate icon
        var dropdownIcon = event.target.querySelector(".dropdown-icon");
        if (dropdownIcon) {
            dropdownIcon.classList.toggle("rotate");
        }
    }
});



// ====== DELETE THE RESPECTIVE PAGE ======
document.addEventListener('click', function (event) {
    if (event.target.closest('.icon-trash')) {
        const pageElement = event.target.closest('.page');
        if (pageElement) {
            pageElement.remove(); // Remove the .page element
        }
    }
});



// ====== FILE IMAGE INPUT VALIDATION + PREVIEW + FILENAME CHANGES======
var save = true;

const allowedExtensions = ['jpg', 'jpeg', 'png', 'svg'];
const maxFileSize = 5 * 1024 * 1024; // max size 5mb

document.addEventListener('change', (event) => {
    if (event.target.classList.contains('input-file-invi')) {
        const fileInput = event.target;
        const container = fileInput.parentElement;
        const filenameSpan = container.querySelector('.filename');
        const errorCourseLogo = container.querySelector('.error-course-logo');
        const preview = container.querySelector('.preview');

        const file = fileInput.files[0];
        
        // if there is file
        if (file) {
            const fileExtension = file.name.split('.').pop().toLowerCase();

            // Invalid file type
            if (!allowedExtensions.includes(fileExtension)) {
                errorCourseLogo.textContent = `Invalid file type! Only ${allowedExtensions.join(', ')} are allowed.`;
                errorCourseLogo.style.display = 'block';

                fileInput.value = ''; // Reset the input
                filenameSpan.textContent = 'No file chosen';

                // No preview
                preview.src = '';
                preview.style.display = 'none';
                return;
            }

            // File size too large
            if (file.size > maxFileSize) {
                errorCourseLogo.textContent = 'Maximum file size is 5 MB!';
                errorCourseLogo.style.display = 'block';

                fileInput.value = ''; // Reset the input
                filenameSpan.textContent = 'No file chosen';

                // No preview
                preview.src = '';
                preview.style.display = 'none';
                return;
            }

            // Valid file
            filenameSpan.textContent = file.name;
            errorCourseLogo.textContent = '';
            errorCourseLogo.style.display = 'none';

            // Preview the image
            preview.src = URL.createObjectURL(file);
            preview.style.display = 'block';
        }
        
        // No file selected
        else {
            filenameSpan.textContent = 'No file chosen';
            errorCourseLogo.textContent = '';
            errorCourseLogo.style.display = 'none';
            preview.src = '';
            preview.style.display = 'none';
        }
    }
});



// ===== EDIT OPTIONS =====
document.addEventListener('click', function (e) {
    if (e.target.matches('[contenteditable="true"]')) {
        e.preventDefault(); // Prevent default behavior if necessary
        e.target.focus();   // Set focus to the clicked label
    }
});



// ======= ADD OPTIONS (soon) =======
const addOptionButton = document.getElementById("add-option-btn");

addOptionButton.addEventListener("click", function (e) {
    e.preventDefault();
    
    // Find all existing radio options and count them
    const container = addOptionButton.parentElement;
    const existingOptions = container.querySelectorAll(".radio-option");
    const nextOptionNumber = existingOptions.length + 1;

    // Create the new radio option element
    const newOption = document.createElement("div");
    newOption.classList.add("radio-option");
    newOption.innerHTML = `
        <input type="radio" id="option-${nextOptionNumber}" name="option" value="Option ${nextOptionNumber}">
        <label for="option-${nextOptionNumber}" contenteditable="true">Option ${nextOptionNumber}</label>
        <img src="../static/assets/icon_exit.svg" alt="">
    `;

    // Insert the new option before the "Add Option" button
    container.insertBefore(newOption, addOptionButton);
});


// ===== DELETE OPTIONS =====
document.addEventListener("click", function (event) {
    // Check if the clicked element is an <img> inside a radio-option
    if (event.target.tagName === "IMG" && event.target.closest(".radio-option")) {
        const radioOption = event.target.closest(".radio-option"); // Get the parent .radio-option
        radioOption.remove(); // Remove the radio-option from the DOM
    }
});



// ===== ADD MORE PAGE (toggle) =====
const addMorePageBtn = document.querySelector('.add-more-page-btn');
const optionsContainer = document.querySelector('.add-page-options');
const buttonWrapper = document.querySelector('.button-wrapper');


// Toggle visibility of the options container
addMorePageBtn.addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default behavior (if necessary)
    e.stopPropagation(); // Prevent click from bubbling up
    optionsContainer.classList.toggle('d-none'); // Show or hide the options
});

// Close options container when clicking outside
document.addEventListener('click', function (e) {
    if (!addMorePageBtn.contains(e.target) && !optionsContainer.contains(e.target)) {
        optionsContainer.classList.add('d-none'); // Hide the options
    }
});

// add the page (soon)
optionsContainer.addEventListener('click', async function (e) {
    const target = e.target.closest('p');
    if (!target) return;

    let url;
    switch (target.id) {
        case 'learning-option':
            url = 'material_learning';
            break;
        case 'challenge-code-option':
            url = 'material_challenge_code';
            break;
        case 'challenge-option-option':
            url = 'material_challenge_option';
            break;
        default:
            console.error('Unknown option selected!');
            return;
    }

    try {
        const response = await fetch(url);
        if (response.ok) {
            const content = await response.text();

            buttonWrapper.insertAdjacentHTML('beforebegin', content);
        }
        
        else {
            console.error(`Failed to load content: ${response.statusText}`);
        }
    }
    
    catch (err) {
        console.error('Error fetching content:', err);
    }

    // Optionally hide the options container after selection
    optionsContainer.classList.add('d-none');
});
