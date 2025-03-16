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

                // Decrease the page number in p.accordion for pages after the deleted one
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

// show existing image
document.querySelectorAll('.input-file-invi').forEach((fileInput) => {
    const parentContainer = fileInput.parentElement;

    const file = fileInput.files[0];
    const preview = parentContainer.querySelector('.preview');
    const filename = parentContainer.querySelector('.filename').value.trim();
    if (!file && preview && (filename != "No file chosen")) {
        preview.style.display = "block";
    }
});

// preview image
document.addEventListener('change', (event) => {
    if (event.target.classList.contains('input-file-invi')) {
        const fileInput = event.target;
        const container = fileInput.parentElement;
        const filename = container.querySelector('.filename');
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
                filename.value = 'No file chosen';

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
                filename.value = 'No file chosen';

                // No preview
                preview.src = '';
                preview.style.display = 'none';
                return;
            }

            // Valid file
            filename.value = file.name;
            errorCourseLogo.textContent = '';
            errorCourseLogo.style.display = 'none';

            // Preview the image
            preview.src = URL.createObjectURL(file);
            preview.style.display = 'block';
        }
        
        // No file selected
        else {
            filename.value = filename.dataset.originalFilename.trim();
            errorCourseLogo.textContent = '';
            errorCourseLogo.style.display = 'none';
            
            const originalPreviewSrc = preview.dataset.urlPreview.trim();
            if (originalPreviewSrc == ''){
                preview.style.display = 'none';
                preview.src = '';
            }
            else{
                preview.style.display = 'block';
                preview.src = originalPreviewSrc;
            }
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

        // remove the filename
        filenameInput.value = "No file chosen";
        filenameInput.dataset.originalFilename = "No file chosen";

        // remove the preview source
        preview.removeAttribute('src');
        preview.dataset.urlPreview = '';
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

            baseID = `${forAttribute}`
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


// ===== DELETE OPTIONS (AMAN) =====
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
            url = '/admin/course/detail_material_learning';
            break;
        case 'challenge-option-option':
            url = '/admin/course/detail_material_challenge_option';
            break;
        case 'challenge-input-option':
            url = '/admin/course/detail_material_challenge_input';
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
    // in this case, the type doesnt really matter because its using a unified form
    pages.forEach(page => {
        const span = page.querySelector(".type > span");
        
        if (span) {
            avail = true;
            const panel = page.querySelector(".panel");
            const secondChild = panel.children[2];
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

    // no existing page/content
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
    const baseID = `content-${randID}`;

    // order
    const order = container.querySelector('.hidden');
    if (order){
        order.id = order.name = `${baseID}-order`;
    }

    // pic
    const filename = container.querySelector('.learning-pic > input[type="text"]');
    const learningPicInput = container.querySelector('.learning-pic > input[type="file"]');
    const learningPicLabels = container.querySelectorAll('.learning-pic > label');
    if (filename && learningPicInput && learningPicLabels.length > 0) {
        filename.id = filename.name = `${baseID}-original_filename`;
        learningPicInput.id = learningPicInput.name = `${baseID}-image`;
        learningPicLabels.forEach(label => label.setAttribute('for', `${baseID}-image`));
    }

    // content learning
    const contentTextarea = container.querySelector('.content-learning > textarea');
    const contentLabel = container.querySelector('.content-learning > label');
    if (contentTextarea && contentLabel) {
        contentTextarea.id = contentTextarea.name = `${baseID}-content_body`;
        contentLabel.setAttribute('for', `${baseID}-content_body`);
    }

    // content_id
    const contentId = container.querySelector('.content-id');
    if (contentId){
        contentId.id = contentId.name = `${baseID}-content_id`
    }
}

function randomizeChallengeOptionId(container, randID){
    const baseID = `content-${randID}`;

    // order
    const order = container.querySelector('.hidden');
    if (order){
        order.id = order.name = `${baseID}-order`;
    }

    // image
    const filename = container.querySelector('.challenge-pic > input[type="text"]');
    const challengePicInput = container.querySelector('.challenge-pic > input[type="file"]');
    const challengePicLabels = container.querySelectorAll('.challenge-pic > label');
    if (challengePicInput && challengePicLabels.length > 0){
        filename.id = filename.name = `${baseID}-original_filename`;
        challengePicInput.id = challengePicInput.name = `${baseID}-image`;
        challengePicLabels.forEach(label => label.setAttribute('for', `${baseID}-image`));
    }

    // question
    const questionTextarea = container.querySelector('.question > textarea');
    const questionLabel = container.querySelector('.question > label');
    if (questionTextarea && questionLabel) {
        questionTextarea.id = questionTextarea.name = `${baseID}-question`;
        questionLabel.setAttribute('for', `${baseID}-question`);
    }

    // code area
    const codeTextarea = container.querySelector('.code-playground > textarea');
    const codeLabel = container.querySelector('.code > label');
    if (codeTextarea && codeLabel) {
        codeTextarea.id = codeTextarea.name = `${baseID}-code`;
        codeLabel.setAttribute('for', `${baseID}-code`);
    }

    // option
    const optionsContainer = container.querySelector('.option');
    const optionID = `${baseID}-options`;
    const hiddenID = `${baseID}-choices`
    
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

    // content_id
    const contentId = container.querySelector('.content-id');
    if (contentId){
        contentId.id = contentId.name = `${baseID}-content_id`
    }
}

function randomizeChallengeInputId(container, randID){
    const baseID = `content-${randID}`;

    // order
    const order = container.querySelector('.hidden');
    if (order){
        order.id = order.name = `${baseID}-order`;
    }

    // image
    const filename = container.querySelector('.input-pic > input[type="text"]');
    const challengePicInput = container.querySelector('.input-pic > input[type="file"]');
    const challengePicLabels = container.querySelectorAll('.input-pic > label');
    if (challengePicInput && challengePicLabels.length > 0){
        filename.id = filename.name = `${baseID}-original_filename`;
        challengePicInput.id = challengePicInput.name = `${baseID}-image`;
        challengePicLabels.forEach(label => label.setAttribute('for', `${baseID}-image`));
    }

    // question
    const questionTextarea = container.querySelector('.question > textarea');
    const questionLabel = container.querySelector('.question > label');
    if (questionTextarea && questionLabel) {
        questionTextarea.id = questionTextarea.name = `${baseID}-question`;
        questionLabel.setAttribute('for', `${baseID}-question`);
    }

    // code area
    const codeTextarea = container.querySelector('.code-playground > textarea');
    const codeLabel = container.querySelector('.code > label');
    if (codeTextarea && codeLabel) {
        codeTextarea.id = codeTextarea.name = `${baseID}-code`;
        codeLabel.setAttribute('for', `${baseID}-code`);
    }

    // answer
    const answerInput = container.querySelector('.answer > input');
    const answerLabel = container.querySelector('.answer > label');
    if (answerInput && answerLabel){
        answerInput.id = answerInput.name = `${baseID}-answer`;
        answerLabel.setAttribute('for', `${baseID}-answer`);
    }

    // content_id
    const contentId = container.querySelector('.content-id');
    if (contentId){
        contentId.id = contentId.name = `${baseID}-content_id`
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