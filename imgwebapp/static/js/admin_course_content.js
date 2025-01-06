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




// ======= MOVE UP + DOWN ========
document.addEventListener('click', function (e) {
    // up
    if (e.target.closest('.up')) {
        const currentPage = e.target.closest('.page');
        const previousPage = currentPage?.previousElementSibling;

        if (previousPage && previousPage.classList.contains('page')) {
            currentPage.parentNode.insertBefore(currentPage, previousPage); // swap
            swapPageNumbers(currentPage, previousPage);
        }
    }

    // down
    if (e.target.closest('.down')) {
        const currentPage = e.target.closest('.page');
        const nextPage = currentPage?.nextElementSibling;

        if (nextPage && nextPage.classList.contains('page')) {
            currentPage.parentNode.insertBefore(nextPage, currentPage); // swap
            swapPageNumbers(currentPage, nextPage);
        }
    }
});

/**
 * @param {HTMLElement} page1 - The first .page element
 * @param {HTMLElement} page2 - The second .page element
 */
function swapPageNumbers(page1, page2) {
    const page1NumberElement = page1.querySelector('p.accordion');
    const page2NumberElement = page2.querySelector('p.accordion');

    if (page1NumberElement && page2NumberElement) {
        // Extract the current page numbers
        const page1Number = page1NumberElement.childNodes[0].textContent.trim();
        const page2Number = page2NumberElement.childNodes[0].textContent.trim();

        // Swap the page numbers
        page1NumberElement.childNodes[0].textContent = page2Number;
        page2NumberElement.childNodes[0].textContent = page1Number;
    }
}



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



// ===== EDIT OPTIONS (soon) =====
document.addEventListener('click', function (e) {
    if (e.target.matches('[contenteditable="true"]')) {
        e.preventDefault(); // Prevent default behavior if necessary
        e.target.focus();   // Set focus to the clicked label
    }
});



// ======= ADD OPTIONS (soon) =======
const addOptionButton = document.querySelector(".add-option-btn");

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


// add more page options toggle
addMorePageBtn.addEventListener('click', function (e) {
    e.stopPropagation(); // Prevent click from bubbling up
    optionsContainer.classList.toggle('d-none'); // Show or hide the options
});

// close options container when clicking outside
document.addEventListener('click', function (e) {
    if (!addMorePageBtn.contains(e.target) && !optionsContainer.contains(e.target)) {
        optionsContainer.classList.add('d-none'); // Hide the options
    }
});

// add the page
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

            // Parse the content into a DOM element
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = content; // Insert the fetched HTML

            // Count existing .page elements to determine the page number
            const currentPageCount = document.querySelectorAll('.page').length;
            const newPageNumber = currentPageCount + 1;

            // Update the <p> tag with the new page number
            const newAccordion = tempDiv.querySelector('p.accordion');
            if (newAccordion) {
                newAccordion.childNodes[0].textContent = `Page ${newPageNumber} `;
            }

            switch (target.id) {
                case 'learning-option':
                    randomizeLearningId(tempDiv);
                    break;
                case 'challenge-code-option':
                    randomizeChallengeCodeId(tempDiv);
                    break;
                case 'challenge-option-option':
                    url = 'material_challenge_option';
                    break;
                default:
                    console.error('Unknown option selected!');
                    return;
            }
            

            // Insert the updated content before the .button-wrapper
            buttonWrapper.parentNode.insertBefore(tempDiv.firstElementChild, buttonWrapper);
        }
        
        else {
            console.error(`Failed to load content: ${response.statusText}`);
        }
    }
    
    catch (err) {
        console.error('Error fetching content:', err);
    }

    // hide the options after selection
    optionsContainer.classList.add('d-none');
});

// generate random ID function
function generateRandomID() {
    return Date.now();
}

// RANDOMIZE ID
/**
 * @param {HTMLElement} container - The container element to randomize IDs for
 */
function randomizeLearningId(container) {
    // type
    const typeInput = container.querySelector('.type > input');
    const typeLabel = container.querySelector('.type > label');
    if (typeInput && typeLabel) {
        const randomID = `learning-${generateRandomID()}`;
        typeInput.id = randomID; // Update the input ID
        typeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // pic
    const learningPicInput = container.querySelector('.learning-pic > input');
    const learningPicLabels = container.querySelectorAll('.learning-pic > label');
    if (learningPicInput && learningPicLabels.length > 0) {
        const randomID = `learning-pic-${generateRandomID()}`;
        learningPicInput.id = randomID; // Update the input ID
        learningPicLabels.forEach(label => label.setAttribute('for', randomID));
    }

    // content learning
    const contentTextarea = container.querySelector('.content-learning > textarea');
    const contentLabel = container.querySelector('.content-learning > label');
    if (contentTextarea && contentLabel) {
        const randomID = `content-learning-${generateRandomID()}`;
        contentTextarea.id = randomID; // Update the textarea ID
        contentLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }
}

function randomizeChallengeCodeId(container){
    // type
    const typeInput = container.querySelector('.type > input');
    const typeLabel = container.querySelector('.type > label');
    if (typeInput && typeLabel) {
        const randomID = `challenge-code-${generateRandomID()}`;
        typeInput.id = randomID; // Update the input ID
        typeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // question
    const questionTextarea = container.querySelector('.question > textarea');
    const questionLabel = container.querySelector('.question > label');
    if (questionTextarea && questionLabel) {
        const randomID = `code-question-${generateRandomID()}`;
        questionTextarea.id = randomID; // Update the textarea ID
        questionLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // code area
    const codeTextarea = container.querySelector('.code-playground > textarea');
    const codeLabel = container.querySelector('.code > label');
    if (codeTextarea && codeLabel) {
        const randomID = `code-code-area-${generateRandomID()}`;
        codeTextarea.id = randomID; // Update the textarea ID
        codeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }
}

function randomizeChallengeOptionId(container){
    // type
    const typeInput = container.querySelector('.type > input');
    const typeLabel = container.querySelector('.type > label');
    if (typeInput && typeLabel) {
        const randomID = `challenge-option-${generateRandomID()}`;
        typeInput.id = randomID; // Update the input ID
        typeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // question
    const questionTextarea = container.querySelector('.question > textarea');
    const questionLabel = container.querySelector('.question > label');
    if (questionTextarea && questionLabel) {
        const randomID = `option-question-${generateRandomID()}`;
        questionTextarea.id = randomID; // Update the textarea ID
        questionLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    const codeTextarea = container.querySelector('.code-playground > textarea');
    const codeLabel = container.querySelector('.code > label');
    if (codeTextarea && codeLabel) {
        const randomID = `code-option-area-${generateRandomID()}`;
        codeTextarea.id = randomID; // Update the textarea ID
        codeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }
}