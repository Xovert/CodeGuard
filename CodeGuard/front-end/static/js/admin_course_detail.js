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



// ===== EDIT OPTIONS =====
document.querySelectorAll('[contenteditable="true"]').forEach(label => {
    label.addEventListener('click', function (e) {
        e.preventDefault();
        this.focus();
    });
});

// add option button
const addOptionButton = document.getElementById("add-option-btn");

// Counter to track new option numbers
let optionCounter = 4;

// Add event listener to the button
addOptionButton.addEventListener("click", function (e) {
    e.preventDefault();
    
    // container
    const container = addOptionButton.parentElement;

    // new element
    const newOption = document.createElement("div");
    newOption.classList.add("radio-option");
    newOption.innerHTML = `
        <input type="radio" id="option-${optionCounter}" name="option" value="Option ${optionCounter}">
        <label for="option-${optionCounter}" contenteditable="true">Option ${optionCounter}</label>
        <img src="../static/assets/icon_exit.svg" alt="">
    `;

    // Insert the new option before the "Add Option" button
    container.insertBefore(newOption, addOptionButton);

    // Increment the option counter
    optionCounter++;
});



// ===== DELETE OPTIONS =====
document.addEventListener("click", function (event) {
    // Check if the clicked element is an <img> inside a radio-option
    if (event.target.tagName === "IMG" && event.target.closest(".radio-option")) {
        const radioOption = event.target.closest(".radio-option"); // Get the parent .radio-option
        radioOption.remove(); // Remove the radio-option from the DOM
    }
});



// ===== ADD MORE PAGE =====
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
