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
            if (pageElement.classList.contains('study')) {
                // Get all .study elements after the current pageElement
                const studyPages = Array.from(
                    document.querySelectorAll('.page.study')
                );

                const currentIndex = studyPages.indexOf(pageElement);

                // Decrease the page number in p.accordion for all .study elements after the current one
                studyPages.slice(currentIndex + 1).forEach((studyPage) => {
                    const accordion = studyPage.querySelector('p.accordion');
                    if (accordion) {
                        // Extract the text content of the accordion (excluding buttons)
                        const textNode = Array.from(accordion.childNodes).find(
                            (node) => node.nodeType === Node.TEXT_NODE
                        );

                        if (textNode) {
                            // Extract and decrement the page number
                            const match = textNode.textContent.match(/Page (\d+)/);
                            if (match) {
                                const pageNumber = parseInt(match[1], 10);
                                textNode.textContent = textNode.textContent.replace(
                                    `Page ${pageNumber}`,
                                    `Page ${pageNumber - 1}`
                                );
                            }
                        }
                    }
                });
            }

            // UPDATE ALL THE PAGES ORDER VALUE
            const pages = Array.from(
                document.querySelectorAll('.page')
            );

            const currentOrder = pages.indexOf(pageElement);

            // decrease the order value in all pages after the current one
            pages.slice(currentOrder + 1).forEach((pages) => {
                const order = pages.querySelector('.hidden');
                if (order) {
                    order.value = order.value - 1;
                }
            });
            
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
            if (currentPage.classList.contains('study') && previousPage.classList.contains('study')){
                swapPageNumbers(currentPage, previousPage);
            }
        }
    }

    // down
    if (e.target.closest('.down')) {
        const currentPage = e.target.closest('.page');
        const nextPage = currentPage?.nextElementSibling;

        if (nextPage && nextPage.classList.contains('page')) {
            currentPage.parentNode.insertBefore(nextPage, currentPage); // swap
            if (currentPage.classList.contains('study') && nextPage.classList.contains('study')){
                swapPageNumbers(currentPage, nextPage);
            }
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

    const orderPage1Element = page1.querySelector('.hidden');
    const orderPage2Element = page2.querySelector('.hidden');

    if (page1NumberElement && page2NumberElement) {
        // Extract the current page numbers
        const page1Number = page1NumberElement.childNodes[0].textContent.trim();
        const page2Number = page2NumberElement.childNodes[0].textContent.trim();

        // Swap the page numbers
        page1NumberElement.childNodes[0].textContent = page2Number;
        page2NumberElement.childNodes[0].textContent = page1Number;

        let tmp = orderPage1Element.value;
        orderPage1Element.value = orderPage2Element.value;
        orderPage2Element.value = tmp;
    }
}



// ====== FILE IMAGE INPUT VALIDATION + PREVIEW + FILENAME CHANGES ======
const allowedExtensions = ['jpg', 'jpeg', 'png'];
const maxFileSize = 1 * 1024 * 1024; // max size 5mb

var errorCourseLogo = document.getElementById('error-course-logo');

// show element yg udah ada
document.querySelectorAll('.input-file-invi').forEach((fileInput) => {
    const parentContainer = fileInput.parentElement;

    const file = fileInput.files[0];
    const preview = parentContainer.querySelector('.preview');
    const filename = parentContainer.querySelector('.filename').textContent.trim();
    if (!file && preview && (filename != "No file chosen")) {
        preview.style.display = "block";
    }
});

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
                errorCourseLogo.textContent = 'Maximum file size is 1 MB!';
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
document.addEventListener("input", function (event) {
    // Check if the event target is a text input inside a radio-option
    if (event.target.matches(".radio-option label input[type='text']")) {
        const textInput = event.target;
        const radioButton = textInput.closest(".radio-option").querySelector("input[type='radio']");

        if (radioButton) {
            radioButton.value = textInput.value; // Update radio button value
            textInput.value = textInput.value;
        }
    }
});


// update the value
document.addEventListener("input", function (event) {
    // Check if the target is a contenteditable label
    if (event.target.matches('label[contenteditable="true"]')) {
        const label = event.target; // The label being edited
        const input = label.previousElementSibling; // The associated input element
        
        if (input && input.tagName === "INPUT") {
            input.setAttribute("value", label.textContent.trim()); // Update the value attribute
        }
    }
});



// ======= ADD OPTIONS =======
document.addEventListener("click", function (event) {
    if (event.target.closest(".add-option-btn")) {
        const button = event.target.closest(".add-option-btn");
        const optionContainer = button.closest(".option");

        // Find the last radio option in the container
        const radioOptions = optionContainer.querySelectorAll(".radio-option");
        let baseID;
        let nextCounter;
        let choicesID;

        // kalo ada last .radio-option, get it
        if (radioOptions.length > 0){
            const lastRadioOption = radioOptions[radioOptions.length - 1]; // Get the last .radio-option
            const lastInput = lastRadioOption.querySelector("input"); // Get the input inside the last .radio-option
    
            // Extract the base ID and counter from the last input's ID
            const idParts = lastInput.id.split("-"); // di split by -
            baseID = idParts.slice(0, -1).join("-"); // disambungin lagi, kecuali bagian terakhir (jadi base ID)
            const lastCounter = parseInt(idParts[idParts.length - 1], 10); // Convert the last part to a number
    
            choicesID = idParts.slice(0, 2).join("-");
            nextCounter = lastCounter + 1; // Calculate the next counter
        }

        // no .radio-option available
        else{
            // get the for attribute of the label
            const labelOption = optionContainer.querySelector("label");
            const forAttribute = labelOption?.getAttribute("for");

            baseID = `${forAttribute}` 
            choicesID = forAttribute.split('-').slice(0, 2).join("-");
            nextCounter = 0;
        }

        // Create the new .radio-option element
        const newRadioOption = document.createElement("div");
        newRadioOption.classList.add("radio-option");
        newRadioOption.innerHTML = `
            <input type="radio" id="${baseID}-${nextCounter}" name="${baseID}" value="Option ${nextCounter + 1}" required>
            <label for="${baseID}-${nextCounter}"><input type="text" id="${choicesID}-choices-${nextCounter}-choices" name="${choicesID}-choices-${nextCounter}-choices" value="Option ${nextCounter + 1}" required></label>
            <img src="/static/assets/icon_exit.svg" alt="">
        `;

        // Append the new .radio-option before the .add-option-btn
        optionContainer.insertBefore(newRadioOption, button);
    }
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
const error = document.getElementById('error-message');


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
            url = '/admin/course/material_learning';
            break;
        case 'challenge-option-option':
            url = '/admin/course/material_challenge_option';
            break;
        default:
            alert('Unknown option selected!');
            return;
    }

    try {
        const response = await fetch(url);
        if (response.ok) {
            const content = await response.text();

            // Parse the content into a DOM element
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = content; // Insert the fetched HTML

            // FOR PAGE COUNTTTTTT
            let currentPageCount;
            let prefixTitle;
            let newPageNumber;
            if (target.id === "learning-option" || target.id === "challenge-option-option"){
                currentPageCount = document.querySelectorAll('.study').length;
                prefixTitle = "Page ";
                newPageNumber = currentPageCount + 1;
            }

            // Update the <p> tag with the new page number
            const newAccordion = tempDiv.querySelector('p.accordion');
            if (newAccordion) {
                newAccordion.childNodes[0].textContent = `${prefixTitle}${newPageNumber} `;
            }

            // HITUNG ORDER PAGES
            const allPageCount = document.querySelectorAll('.page').length;
            const order = tempDiv.querySelector('.hidden');
            
            if(order){
                order.value = allPageCount + 1;
            }

            // GENERATE IDDDD
            let randID;

            switch (target.id) {
                case 'learning-option':
                    randID = generateID("learning");
                    randomizeLearningId(tempDiv, randID);
                    break;
                case 'challenge-option-option':
                    randID = generateID("challenge option");
                    randomizeChallengeOptionId(tempDiv, randID);
                    break;
                default:
                    alert("Unknown option selected!")
                    return;
            }

            // Insert the updated content before the .button-wrapper
            error.parentNode.insertBefore(tempDiv.firstElementChild, error);
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
function generateID(type) {
    const pages = document.querySelectorAll(".page");

    let maxIndex = 0;
    let avail = false;

    pages.forEach(page => {
        const span = page.querySelector(".type > span"); // Get the span inside .type

        // Check if it has 'Learning' type
        if (span && span.textContent.trim().toLowerCase() === type) {
            avail = true;
            const panel = page.querySelector(".panel"); // Select the .panel inside the page
            const secondChild = panel.children[2]; // second child, tidak terhitung hidden
            const inputLabel = secondChild.querySelector("label");

            if (inputLabel) {
                const forAttribute = inputLabel.getAttribute("for");
                const parts = forAttribute.split("-");
                const index = parseInt(parts[1], 10);

                if (index > maxIndex) {
                    maxIndex = index; // Update max index
                }
            }
        }
    });

    if(!avail){
        return maxIndex;
    }
    return maxIndex + 1;
}

// RANDOMIZE ID
/**
 * @param {HTMLElement} container - The container element to randomize IDs for
 */
function randomizeLearningId(container, randID) {
    // order
    const order = container.querySelector('.hidden');
    if (order){
        const randomID = `learning-${randID}-order`;
        order.id = order.name = randomID;
    }

    // pic
    const learningPicInput = container.querySelector('.learning-pic > input');
    const learningPicLabels = container.querySelectorAll('.learning-pic > label');
    if (learningPicInput && learningPicLabels.length > 0) {
        const randomID = `learning-${randID}-image`;
        learningPicInput.id = learningPicInput.name = randomID; // Update the input ID
        learningPicLabels.forEach(label => label.setAttribute('for', randomID));
    }

    // content learning
    const contentTextarea = container.querySelector('.content-learning > textarea');
    const contentLabel = container.querySelector('.content-learning > label');
    if (contentTextarea && contentLabel) {
        const randomID = `learning-${randID}-content_body`;
        contentTextarea.id = contentTextarea.name = randomID; // Update the textarea ID
        contentLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }
}

function randomizeChallengeOptionId(container, randID){
    // order
    const order = container.querySelector('.hidden');
    if (order){
        const randomID = `challenge_options-${randID}-order`;
        order.id = order.name = randomID;
    }

    // image
    const challengePicInput = container.querySelector('.challenge-pic > input');
    const challengePicLabels = container.querySelectorAll('.challenge-pic > label');
    if (challengePicInput && challengePicLabels.length > 0){
        const randomID = `challenge_options-${randID}-image`;
        challengePicInput.id = challengePicInput.name = randomID;
        challengePicLabels.forEach(label => label.setAttribute('for', randomID));
    }

    // question
    const questionTextarea = container.querySelector('.question > textarea');
    const questionLabel = container.querySelector('.question > label');
    if (questionTextarea && questionLabel) {
        const randomID = `challenge_options-${randID}-question`
        questionTextarea.id = questionTextarea.name = randomID; // Update the textarea ID
        questionLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // code area
    const codeTextarea = container.querySelector('.code-playground > textarea');
    const codeLabel = container.querySelector('.code > label');
    if (codeTextarea && codeLabel) {
        const randomID = `challenge_options-${randID}-code`;
        codeTextarea.id = codeTextarea.name = randomID; // Update the textarea ID
        codeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // option
    const optionsContainer = container.querySelector('.option');
    const randomID = `challenge_options-${randID}`;
    const optionID = `${randomID}-options`;
    const hiddenID = `${randomID}-choices`
    
    const optionsLabel = optionsContainer.querySelector("label");
    optionsLabel.setAttribute('for', optionID)

    const radioOptions = optionsContainer.querySelectorAll(".radio-option");
    let counter = 0; // Initialize counter

    radioOptions.forEach(radioOption => {
        const input = radioOption.querySelector("input[type='radio']");
        const radioLabel = radioOption.querySelector("label");
        const choice = radioOption.querySelector("input[type='text']");

        // Update name attribute
        // const name = `${randomID}-options`
        input.setAttribute("name", optionID);

        // Update ID attribute
        const newID = `${optionID}-${counter}`;
        input.setAttribute("id", newID);

        // Update label's for attribute
        radioLabel.setAttribute("for", newID);

        // update choices
        choice.id = choice.name = `${hiddenID}-${counter}-choices`;

        counter++; // Increment counter
    });

}

// MAU KIRIM DATA
const submitButton = document.querySelector('.submit-btn');

submitButton.addEventListener('click', async function (e) {
    // module name
    const moduleNameInput = document.querySelector('#module-name');
    const moduleName = moduleNameInput?.value.trim() || null;

    if (!moduleName){
        error.textContent = 'Please specify which module these pages belong to!';
        error.style.display = 'block'
        return;
    }
    
    error.textContent = '';
    error.style.display = ''
});