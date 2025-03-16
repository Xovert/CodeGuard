// ======= RESIZE TEXTAREA =======
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

document.addEventListener("input", function (event) {
    if (event.target.tagName === "TEXTAREA") {
        autoResize(event.target);
    }
});



// ===== ACCORDION =====
document.addEventListener("click", function (event) {
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


// ====== MODAL (IF YES) ======
document.getElementById('yes').addEventListener('click', () => {
    let course = encodeURIComponent(document.querySelector('.title').dataset.courseName);
    course = encodeURIComponent(course)
    window.location.replace(`/admin/${course}/modules`);
});



// ====== DELETE THE RESPECTIVE PAGE ======
document.addEventListener('click', function (event) {
    if (event.target.closest('.icon-trash')) {
        const pageElement = event.target.closest('.page');
        if (pageElement) {
            if (pageElement.classList.contains('study')) {
                // get all .study elements after the current pageElement
                const studyPages = Array.from(
                    document.querySelectorAll('.page.study')
                );

                const currentIndex = studyPages.indexOf(pageElement);

                // Decrease the page number in p.accordion for all pages after the deleted one
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

            // decrease the order value after the deleted page
            pages.slice(currentOrder + 1).forEach((pages) => {
                const order = pages.querySelector('.hidden');
                if (order) {
                    order.value = order.value - 1;
                }
            });
            
            pageElement.remove();
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
 * @param {HTMLElement} page1
 * @param {HTMLElement} page2
 */
function swapPageNumbers(page1, page2) {
    const page1NumberElement = page1.querySelector('p.accordion');
    const page2NumberElement = page2.querySelector('p.accordion');

    const orderPage1Element = page1.querySelector('.hidden');
    const orderPage2Element = page2.querySelector('.hidden');

    if (page1NumberElement && page2NumberElement) {
        const page1Number = page1NumberElement.childNodes[0].textContent.trim();
        const page2Number = page2NumberElement.childNodes[0].textContent.trim();

        // swap the page numbers
        page1NumberElement.childNodes[0].textContent = page2Number;
        page2NumberElement.childNodes[0].textContent = page1Number;

        let tmp = orderPage1Element.value;
        orderPage1Element.value = orderPage2Element.value;
        orderPage2Element.value = tmp;
    }
}



// ====== FILE IMAGE INPUT VALIDATION + PREVIEW + FILENAME CHANGES ======
const allowedExtensions = ['jpg', 'jpeg', 'png'];
const maxFileSize = 1 * 1024 * 1024;

var errorCourseLogo = document.getElementById('error-course-logo');

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

                fileInput.value = '';
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

                fileInput.value = '';
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

// delete image
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('delete-img-btn')) {
        const container = event.target.parentElement;
        const filenameInput = container.querySelector('.filename');
        const preview = container.querySelector('.preview');
        const fileInput = container.querySelector('.input-file-invi');
        const errorCourseLogo = container.querySelector('.error-course-logo');

        filenameInput.textContent = "No file chosen";

        // remove the preview source
        preview.removeAttribute('src');
        preview.style.display = 'none';

        // clear file input
        fileInput.value = '';

        errorCourseLogo.textContent = '';
        errorCourseLogo.style.display = 'none';
    }
});





// ===== EDIT OPTIONS =====
document.addEventListener("input", function (event) {
    if (event.target.matches(".radio-option label input[type='text']")) {
        const textInput = event.target;
        const radioButton = textInput.closest(".radio-option").querySelector("input[type='radio']");

        if (radioButton) {
            radioButton.value = textInput.value; // update the value
            textInput.value = textInput.value;
        }
    }
});


// ======= ADD OPTIONS =======
document.addEventListener("click", function (event) {
    if (event.target.closest(".add-option-btn")) {
        const button = event.target.closest(".add-option-btn");
        const optionContainer = button.closest(".option");

        const radioOptions = optionContainer.querySelectorAll(".radio-option");
        let baseID;
        let nextCounter;
        let choicesID;

        // if there exists a .radio-option
        if (radioOptions.length > 0){
            // get the last .radio-option and extract its base ID
            const lastRadioOption = radioOptions[radioOptions.length - 1]; 
            const lastInput = lastRadioOption.querySelector("input");
    
            const idParts = lastInput.id.split("-");
            baseID = idParts.slice(0, -1).join("-");
            const lastCounter = parseInt(idParts[idParts.length - 1], 10);
    
            choicesID = idParts.slice(0, 2).join("-");
            nextCounter = lastCounter + 1;
        }

        // no .radio-option available
        else{
            // get the for attribute of the label
            const labelOption = optionContainer.querySelector("label");
            const forAttribute = labelOption?.getAttribute("for");

            baseID = forAttribute
            choicesID = forAttribute.split('-').slice(0, 2).join("-");
            nextCounter = 0;
        }

        // create the new .radio-option element
        const newRadioOption = document.createElement("div");
        newRadioOption.classList.add("radio-option");
        newRadioOption.innerHTML = `
            <input type="radio" id="${baseID}-${nextCounter}" name="${baseID}" value="Option ${nextCounter + 1}" required>
            <label for="${baseID}-${nextCounter}"><input type="text" id="${choicesID}-choices-${nextCounter}-choices" name="${choicesID}-choices-${nextCounter}-choices" value="Option ${nextCounter + 1}" required></label>
            <img src="/static/assets/icon_exit.svg" alt="">
        `;

        optionContainer.insertBefore(newRadioOption, button);
    }
});


// ===== DELETE OPTIONS =====
document.addEventListener("click", function (event) {
    if (event.target.tagName === "IMG" && event.target.closest(".radio-option")) {
        const radioOption = event.target.closest(".radio-option");
        radioOption.remove();
    }
});



// ===== ADD MORE PAGE (toggle) =====
const addMorePageBtn = document.querySelector('.add-more-page-btn');
const optionsContainer = document.querySelector('.add-page-options');
const error = document.getElementById('error-message');


// add more page options toggle
addMorePageBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    optionsContainer.classList.toggle('d-none');
});

// close options container when clicking outside
document.addEventListener('click', function (e) {
    if (!addMorePageBtn.contains(e.target) && !optionsContainer.contains(e.target)) {
        optionsContainer.classList.add('d-none');
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
        case 'challenge-input-option':
            url = '/admin/course/material_challenge_input';
            break;
        default:
            alert('Unknown option selected!');
            return;
    }

    try {
        const response = await fetch(url);
        if (response.ok) {
            // get the content
            const content = await response.text();
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = content;

            // page count
            let currentPageCount;
            let prefixTitle;
            let newPageNumber;
            if (target.id === "learning-option" || target.id === "challenge-option-option" || target.id === 'challenge-input-option'){
                currentPageCount = document.querySelectorAll('.study').length;
                prefixTitle = "Page ";
                newPageNumber = currentPageCount + 1;
            }

            const newAccordion = tempDiv.querySelector('p.accordion');
            if (newAccordion) {
                newAccordion.childNodes[0].textContent = `${prefixTitle}${newPageNumber} `;
            }

            // get order value
            const allPageCount = document.querySelectorAll('.page').length;
            const order = tempDiv.querySelector('.hidden');
            
            if(order){
                order.value = allPageCount + 1;
            }

            // generateID
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
                case 'challenge-input-option':
                    randID = generateID("challenge input");
                    randomizeChallengeInputId(tempDiv, randID);
                    break;
                default:
                    alert("Unknown option selected!")
                    return;
            }
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


function generateID(type) {
    const pages = document.querySelectorAll(".page");

    let maxIndex = 0;
    let avail = false;

    pages.forEach(page => {
        // count how many pages the type has
        const span = page.querySelector(".type > span");

        if (span && span.textContent.trim().toLowerCase() === type) {
            avail = true;
            const panel = page.querySelector(".panel");
            const secondChild = panel.children[2];
            const inputLabel = secondChild.querySelector("label");

            if (inputLabel) {
                const forAttribute = inputLabel.getAttribute("for");
                const parts = forAttribute.split("-");
                const index = parseInt(parts[1], 10);

                // update max index
                if (index > maxIndex) {
                    maxIndex = index;
                }
            }
        }
    });

    // no page with that type
    if(!avail){
        return maxIndex;
    }
    return maxIndex + 1;
}

// RANDOMIZE ID
/**
 * @param {HTMLElement} container
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
        learningPicInput.id = learningPicInput.name = randomID;
        learningPicLabels.forEach(label => label.setAttribute('for', randomID));
    }

    // content learning
    const contentTextarea = container.querySelector('.content-learning > textarea');
    const contentLabel = container.querySelector('.content-learning > label');
    if (contentTextarea && contentLabel) {
        const randomID = `learning-${randID}-content_body`;
        contentTextarea.id = contentTextarea.name = randomID; 
        contentLabel.setAttribute('for', randomID);
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
        questionTextarea.id = questionTextarea.name = randomID;
        questionLabel.setAttribute('for', randomID);
    }

    // code area
    const codeTextarea = container.querySelector('.code-playground > textarea');
    const codeLabel = container.querySelector('.code > label');
    if (codeTextarea && codeLabel) {
        const randomID = `challenge_options-${randID}-code`;
        codeTextarea.id = codeTextarea.name = randomID;
        codeLabel.setAttribute('for', randomID);
    }

    // option
    const optionsContainer = container.querySelector('.option');
    const randomID = `challenge_options-${randID}`;
    const optionID = `${randomID}-options`;
    const hiddenID = `${randomID}-choices`
    
    const optionsLabel = optionsContainer.querySelector("label");
    optionsLabel.setAttribute('for', optionID)

    const radioOptions = optionsContainer.querySelectorAll(".radio-option");
    let counter = 0;

    radioOptions.forEach(radioOption => {
        const input = radioOption.querySelector("input[type='radio']");
        const radioLabel = radioOption.querySelector("label");
        const choice = radioOption.querySelector("input[type='text']");

        // input[type='radio']
        input.setAttribute("name", optionID);
        const newID = `${optionID}-${counter}`;
        input.setAttribute("id", newID);

        // label
        radioLabel.setAttribute("for", newID);

        // choice
        choice.id = choice.name = `${hiddenID}-${counter}-choices`;

        counter++;
    });

}

function randomizeChallengeInputId(container, randID){
    // order
    const order = container.querySelector('.hidden');
    if (order){
        const randomID = `challenge_input-${randID}-order`;
        order.id = order.name = randomID;
    }

    // image
    const challengePicInput = container.querySelector('.input-pic > input');
    const challengePicLabels = container.querySelectorAll('.input-pic > label');
    if (challengePicInput && challengePicLabels.length > 0){
        const randomID = `challenge_input-${randID}-image`;
        challengePicInput.id = challengePicInput.name = randomID;
        challengePicLabels.forEach(label => label.setAttribute('for', randomID));
    }

    // question
    const questionTextarea = container.querySelector('.question > textarea');
    const questionLabel = container.querySelector('.question > label');
    if (questionTextarea && questionLabel) {
        const randomID = `challenge_input-${randID}-question`
        questionTextarea.id = questionTextarea.name = randomID;
        questionLabel.setAttribute('for', randomID);
    }

    // code area
    const codeTextarea = container.querySelector('.code-playground > textarea');
    const codeLabel = container.querySelector('.code > label');
    if (codeTextarea && codeLabel) {
        const randomID = `challenge_input-${randID}-code`;
        codeTextarea.id = codeTextarea.name = randomID;
        codeLabel.setAttribute('for', randomID);
    }

    // answer
    const answerInput = container.querySelector('.answer > input');
    const answerLabel = container.querySelector('.answer > label');
    if (answerInput && answerLabel){
        const randomID = `challenge_input-${randID}-answer`;
        answerInput.id = answerInput.name = randomID;
        answerLabel.setAttribute('for', randomID);
    }

}

// ====== SENDING DATA ======
const submitButton = document.querySelector('.submit-btn');

submitButton.addEventListener('click', async function (e) {
    // module name
    const moduleNameInput = document.querySelector('#module-name');
    const moduleName = moduleNameInput?.value.trim() || null;

    if (!moduleName){
        error.textContent = 'Please specify which module these pages belong to!';
        error.style.display = 'block';
        return;
    }
    
    error.textContent = '';
    error.style.display = '';
});