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
        var dropdownIcon = event.target.querySelector("img");
        if (dropdownIcon) {
            dropdownIcon.classList.toggle("rotate");
        }
    }
});



// ====== FILE IMAGE INPUT VALIDATION + PREVIEW + FILENAME CHANGES======
var save = true;

const allowedExtensions = ['jpg', 'jpeg', 'png', 'svg'];
const maxFileSize = 5 * 1024 * 1024; // max size 5mb

document.addEventListener('change', (event) => {
    if (event.target.classList.contains('input-file-invi')) {
        const fileInput = event.target; // The file input element
        const filenameSpan = fileInput.nextElementSibling.querySelector('.filename');
        const errorCourseLogo = fileInput.nextElementSibling.querySelector('.error-course-logo');
        const preview = fileInput.nextElementSibling.querySelector('.preview');

        // Validation logic
        const file = fileInput.files[0];

        if (file) {
            const fileExtension = file.name.split('.').pop().toLowerCase();

            // Invalid file type
            if (!allowedExtensions.includes(fileExtension)) {
                errorCourseLogo.textContent = `Invalid file type! Only ${allowedExtensions.join(', ')} are allowed.`;
                errorCourseLogo.style.display = 'block';

                fileInput.value = ''; // Reset the input
                filenameSpan.textContent = 'No file chosen';

                // no preview
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

                // no preview
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
        
        else {
            // No file selected
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



// ===== ADD MORE PAGE (soon) =====
const addPageButton = document.querySelector(".add-more-page-btn");

// Add an event listener to the button
addPageButton.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent form submission or page reload

    // Select the parent form to append the new page
    const form = document.querySelector(".course-content");

    // Create a new page div
    const newPage = document.createElement("div");
    newPage.classList.add("page");

    // Populate the new page with HTML content for a Learning Page
    newPage.innerHTML = `
        <p class="d-flex accordion">New Page
            <img src="../static/assets/icon_dropdown.svg" alt="" class="ms-auto">
        </p>
        <div class="panel">
            <div class="type">
                <label for="content-type" class="d-inline-block">Type</label>
                <select name="content-type" id="content-type">
                    <option value="Learning">Learning</option>
                    <option value="Challenge Code">Challenge Code</option>
                    <option value="Challenge Option">Challenge Option</option>
                </select>
            </div>
            <div class="position-relative">
                <label for="learning-pic">Picture</label>
                <label for="learning-pic" class="input-file">
                    <img src="../static/assets/icon_upload.svg" alt="">
                    Add File
                </label>
                <input type="file" name="learning-pic" id="learning-pic">
            </div>
            <div>
                <label for="content-learning">Content</label>
                <textarea name="content-learning" id="content-learning" rows="4"
                    placeholder="Enter learning content here..."></textarea>
            </div>
        </div>
    `;

    // Append the new page to the form before the button wrapper
    const buttonWrapper = document.querySelector(".button-wrapper");
    form.insertBefore(newPage, buttonWrapper);
});
