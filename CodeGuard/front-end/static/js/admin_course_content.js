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

            else if (pageElement.classList.contains('exam')) {
                // Get all .study elements after the current pageElement
                const examPages = Array.from(
                    document.querySelectorAll('.page.exam')
                );

                const currentIndex = examPages.indexOf(pageElement);

                // Decrease the page number in p.accordion for all .study elements after the current one
                examPages.slice(currentIndex + 1).forEach((examPage) => {
                    const accordion = examPage.querySelector('p.accordion');
                    if (accordion) {
                        // Extract the text content of the accordion (excluding buttons)
                        const textNode = Array.from(accordion.childNodes).find(
                            (node) => node.nodeType === Node.TEXT_NODE
                        );

                        if (textNode) {
                            // Extract and decrement the page number
                            const match = textNode.textContent.match(/Exam (\d+)/);
                            if (match) {
                                const pageNumber = parseInt(match[1], 10);
                                textNode.textContent = textNode.textContent.replace(
                                    `Exam ${pageNumber}`,
                                    `Exam ${pageNumber - 1}`
                                );
                            }
                        }
                    }
                });
            }

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
            if ((currentPage.classList.contains('study') && previousPage.classList.contains('study')) || (currentPage.classList.contains('exam') && previousPage.classList.contains('exam'))){
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
            if ((currentPage.classList.contains('study') && nextPage.classList.contains('study')) || (currentPage.classList.contains('exam') && nextPage.classList.contains('exam'))){
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



// ===== EDIT OPTIONS =====
document.addEventListener('click', function (e) {
    if (e.target.matches('[contenteditable="true"]')) {
        e.preventDefault(); // Prevent default behavior if necessary
        e.target.focus();   // Set focus to the clicked label
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

// blur event > triggered when element loses its focus, i dont think this part of the code is necessary
// document.addEventListener("blur", function (event) {
//     if (event.target.matches('label[contenteditable="true"]')) {
//         const label = event.target;
//         const input = label.previousElementSibling;

//         if (input && input.tagName === "INPUT") {
//             input.setAttribute("value", label.textContent.trim());
//         }
//     }
// }, true); // Use capture phase to ensure blur is captured



// ======= ADD OPTIONS =======
document.addEventListener("click", function (event) {
    if (event.target.closest(".add-option-btn")) {
        const button = event.target.closest(".add-option-btn");
        const optionContainer = button.closest(".option");

        // Find the last radio option in the container
        const radioOptions = optionContainer.querySelectorAll(".radio-option");
        let baseID;
        let nextCounter;

        // kalo ada last .radio-option, get it
        if (radioOptions.length > 0){
            const lastRadioOption = radioOptions[radioOptions.length - 1]; // Get the last .radio-option
            const lastInput = lastRadioOption.querySelector("input"); // Get the input inside the last .radio-option
    
            // Extract the base ID and counter from the last input's ID
            const idParts = lastInput.id.split("-"); // di split by -
            baseID = idParts.slice(0, -1).join("-"); // option-{{randomID}}
            const lastCounter = parseInt(idParts[idParts.length - 1], 10); // Convert the last part to a number
    
            nextCounter = lastCounter + 1; // Calculate the next counter
        }

        // no .radio-option available
        else{
            const panel = optionContainer.closest(".panel");
            const typeInput = panel.querySelector('.type > input');

            const idParts = typeInput.id.split("-");
            if (idParts.length === 3){
                baseID = `${idParts[1]}-${idParts[2]}`;
            }
            else if (idParts.length === 4){
                baseID = `${idParts[0]}-${idParts[1]}-${idParts[3]}`;
            }
            
            nextCounter = 1;
        }

        // Create the new .radio-option element
        const newRadioOption = document.createElement("div");
        newRadioOption.classList.add("radio-option");
        newRadioOption.innerHTML = `
            <input type="radio" id="${baseID}-${nextCounter}" name="${baseID}" value="Option ${nextCounter}">
            <label for="${baseID}-${nextCounter}" contenteditable="true">Enter Option ${nextCounter}</label>
            <img src="../static/assets/icon_exit.svg" alt="">
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
        case 'exam-code-option':
            url = 'material_exam_code';
            break;
        case 'exam-option-option':
            url = 'material_exam_option';
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

            let currentPageCount;
            let prefixTitle;
            let newPageNumber;
            if (target.id === "learning-option" || target.id === "challenge-code-option" || target.id === "challenge-option-option"){
                currentPageCount = document.querySelectorAll('.study').length;
                prefixTitle = "Page ";
                newPageNumber = currentPageCount + 1;
            }

            else if(target.id === "exam-code-option" || target.id === "exam-option-option"){
                currentPageCount = document.querySelectorAll('.exam').length;
                prefixTitle = "Exam ";
                newPageNumber = currentPageCount + 1;
            }
            // Count existing .page elements to determine the page number
            
            

            // Update the <p> tag with the new page number
            const newAccordion = tempDiv.querySelector('p.accordion');
            if (newAccordion) {
                newAccordion.childNodes[0].textContent = `${prefixTitle}${newPageNumber} `;
            }

            const randID = generateRandomID();

            switch (target.id) {
                case 'learning-option':
                    randomizeLearningId(tempDiv, randID);
                    break;
                case 'challenge-code-option':
                    randomizeChallengeCodeId(tempDiv, randID);
                    break;
                case 'challenge-option-option':
                    randomizeChallengeOptionId(tempDiv, randID);
                    break;
                case 'exam-code-option':
                    randomizeExamCodeId(tempDiv, randID);
                    break;
                case 'exam-option-option':
                    randomizeExamOptionId(tempDiv, randID);
                    break;
                default:
                    alert("Unknown option selected!")
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
function randomizeLearningId(container, randID) {
    // type
    const typeInput = container.querySelector('.type > input');
    const typeLabel = container.querySelector('.type > label');
    if (typeInput && typeLabel) {
        const randomID = `learning-${randID}`;
        typeInput.id = randomID; // Update the input ID
        typeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // pic
    const learningPicInput = container.querySelector('.learning-pic > input');
    const learningPicLabels = container.querySelectorAll('.learning-pic > label');
    if (learningPicInput && learningPicLabels.length > 0) {
        const randomID = `learning-pic-${randID}`;
        learningPicInput.id = randomID; // Update the input ID
        learningPicLabels.forEach(label => label.setAttribute('for', randomID));
    }

    // content learning
    const contentTextarea = container.querySelector('.content-learning > textarea');
    const contentLabel = container.querySelector('.content-learning > label');
    if (contentTextarea && contentLabel) {
        const randomID = `content-learning-${randID}`;
        contentTextarea.id = randomID; // Update the textarea ID
        contentLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }
}

function randomizeChallengeCodeId(container, randID){
    // type
    const typeInput = container.querySelector('.type > input');
    const typeLabel = container.querySelector('.type > label');
    if (typeInput && typeLabel) {
        const randomID = `challenge-code-${randID}`;
        typeInput.id = randomID; // Update the input ID
        typeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // question
    const questionTextarea = container.querySelector('.question > textarea');
    const questionLabel = container.querySelector('.question > label');
    if (questionTextarea && questionLabel) {
        const randomID = `code-question-${randID}`;
        questionTextarea.id = randomID; // Update the textarea ID
        questionLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // code area
    const codeTextarea = container.querySelector('.code-playground > textarea');
    const codeLabel = container.querySelector('.code > label');
    if (codeTextarea && codeLabel) {
        const randomID = `code-code-area-${randID}`;
        codeTextarea.id = randomID; // Update the textarea ID
        codeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }
}

function randomizeChallengeOptionId(container, randID){
    // type
    const typeInput = container.querySelector('.type > input');
    const typeLabel = container.querySelector('.type > label');
    if (typeInput && typeLabel) {
        const randomID = `challenge-option-${randID}`;
        typeInput.id = randomID; // Update the input ID
        typeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // question
    const questionTextarea = container.querySelector('.question > textarea');
    const questionLabel = container.querySelector('.question > label');
    if (questionTextarea && questionLabel) {
        const randomID = `option-question-${randID}`;
        questionTextarea.id = randomID; // Update the textarea ID
        questionLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // code area
    const codeTextarea = container.querySelector('.code-playground > textarea');
    const codeLabel = container.querySelector('.code > label');
    if (codeTextarea && codeLabel) {
        const randomID = `code-option-area-${randID}`;
        codeTextarea.id = randomID; // Update the textarea ID
        codeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // option
    const optionsContainer = container.querySelector('.option');
    const randomID = `option-${randID}`;

    const radioOptions = optionsContainer.querySelectorAll(".radio-option");
    let counter = 1; // Initialize counter

    radioOptions.forEach(radioOption => {
        const input = radioOption.querySelector("input");
        const radioLabel = radioOption.querySelector("label");

        // Update name attribute
        input.setAttribute("name", randomID);

        // Update ID attribute
        const newID = `${randomID}-${counter}`;
        input.setAttribute("id", newID);

        // Update label's for attribute
        radioLabel.setAttribute("for", newID);

        counter++; // Increment counter
    });

}

function randomizeExamCodeId(container, randID) {
    const typeInput = container.querySelector(".type > input");
    const typeLabel = container.querySelector(".type > label");
    if (typeInput && typeLabel) {
        const newTypeID = `exam-code-type-${randID}`;
        typeInput.setAttribute("id", newTypeID);
        typeLabel.setAttribute("for", newTypeID);
    }

    // Randomize .timer > input and label
    const timerInput = container.querySelector(".timer > input");
    const timerLabel = container.querySelector(".timer > label");
    if (timerInput && timerLabel) {
        const newTimerID = `exam-code-timer-${randID}`;
        timerInput.setAttribute("id", newTimerID);
        timerLabel.setAttribute("for", newTimerID);
    }

    // Randomize .question > textarea and label
    const questionTextarea = container.querySelector(".question > textarea");
    const questionLabel = container.querySelector(".question > label");
    if (questionTextarea && questionLabel) {
        const newQuestionID = `exam-code-question-${randID}`;
        questionTextarea.setAttribute("id", newQuestionID);
        questionLabel.setAttribute("for", newQuestionID);
    }

    // Randomize .code-playground > textarea and .code > label
    const codeTextarea = container.querySelector(".code-playground > textarea");
    const codeLabel = container.querySelector(".code > label");
    if (codeTextarea && codeLabel) {
        const newCodeID = `exam-code-area-${randID}`;
        codeTextarea.setAttribute("id", newCodeID);
        codeLabel.setAttribute("for", newCodeID);
    }
}

function randomizeExamOptionId(container, randID){
    const typeInput = container.querySelector(".type > input");
    const typeLabel = container.querySelector(".type > label");
    if (typeInput && typeLabel) {
        const newTypeID = `exam-option-type-${randID}`;
        typeInput.setAttribute("id", newTypeID);
        typeLabel.setAttribute("for", newTypeID);
    }

    // Randomize .timer > input and label
    const timerInput = container.querySelector(".timer > input");
    const timerLabel = container.querySelector(".timer > label");
    if (timerInput && timerLabel) {
        const newTimerID = `exam-option-timer-${randID}`;
        timerInput.setAttribute("id", newTimerID);
        timerLabel.setAttribute("for", newTimerID);
    }

    // Randomize .question > textarea and label
    const questionTextarea = container.querySelector(".question > textarea");
    const questionLabel = container.querySelector(".question > label");
    if (questionTextarea && questionLabel) {
        const newQuestionID = `exam-option-question-${randID}`;
        questionTextarea.setAttribute("id", newQuestionID);
        questionLabel.setAttribute("for", newQuestionID);
    }

    // Randomize .code-playground > textarea and .code > label
    const codeTextarea = container.querySelector(".code-playground > textarea");
    const codeLabel = container.querySelector(".code > label");
    if (codeTextarea && codeLabel) {
        const newCodeID = `exam-option-area-${randID}`;
        codeTextarea.setAttribute("id", newCodeID);
        codeLabel.setAttribute("for", newCodeID);
    }

    const optionsContainer = container.querySelector('.option');
    const randomID = `exam-option-${randID}`;

    const radioOptions = optionsContainer.querySelectorAll(".radio-option");
    let counter = 1; // Initialize counter

    radioOptions.forEach(radioOption => {
        const input = radioOption.querySelector("input");
        const radioLabel = radioOption.querySelector("label");

        // Update name attribute
        input.setAttribute("name", randomID);

        // Update ID attribute
        const newID = `${randomID}-${counter}`;
        input.setAttribute("id", newID);

        // Update label's for attribute
        radioLabel.setAttribute("for", newID);

        counter++; // Increment counter
    });
}

const error = document.getElementById('error-message');

// MAU KIRIM DATA
const submitButton = document.querySelector('.submit-btn');

submitButton.addEventListener('click', async function (e) {
    // Prevent form submission for validation
    e.preventDefault();


    // Prepare FormData to handle both JSON data and files
    const formData = new FormData();

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

    let studyCounter = 1;
    let order = 1;

    // Convert all .page data to JSON while also handling file uploads
    const pages = Array.from(document.querySelectorAll('.page')).map((page) => {
        // Determine the ID format based on the class
        let id;
        if (page.classList.contains('study')) {
            id = `study-${studyCounter++}`;
        } else if (page.classList.contains('exam')) {
            id = "exam";
        } else {
            alert('Error: Invalid page!');
            throw new Error('Invalid page!'); // Stop further processing
        }

        const type = page.querySelector('.content-type')?.value || null;
        const content = page.querySelector('.content-learning')?.value || null;
        const question = page.querySelector('.question > textarea')?.value || null;
        const code = page.querySelector('.code-area')?.value || null;

        const optionContainer = page.querySelector('.option');
        let options = {}
        if (optionContainer){
            options = Array.from(page.querySelectorAll('.radio-option')).map(option => {
                return {
                    id: option.querySelector('input')?.id || '',
                    value: option.querySelector('input')?.value || '',
                    is_correct: option.querySelector('input')?.checked || false,
                };
            });
        }

        const timer = page.querySelector('.timer > input[type="time"]')?.value || null;

        // Handle file inputs (images)
        const fileInput = page.querySelector('.input-file-invi');
        const files = fileInput?.files;
        if (files && files.length > 0) {
            // Append the file to FormData
            formData.append(`file-page-${order}`, files[0]); // Unique key for each file
        }

        return {
            id: id,
            order: order++,
            type: type,
            content: content,
            question: question,
            code: code,
            options: options,
            duration: timer,
        };
    });

    const moduleData = {
        moduleName: moduleName,
        pages: pages
    };

    // Add JSON data to FormData
    formData.append('data', JSON.stringify(moduleData));

    // Submit FormData to the backend
    // try {  // SUBMIT KEMANA NIH
    //     const response = await fetch('/add-new-module', {
    //         method: 'POST',
    //         body: formData,
    //     });

    //     if (response.ok) {
    //         const data = await response.json();
    //         alert(data.message + '\nNew module has been successfully added');
    //     } 
        
    //     else {
    //         const data = await response.json();
    //         alert(data.message + '\nFailed to add a new module. Please try again.')
    //     }
    // } catch (error) {
    //     console.error('Error submitting form:', error);
    //     alert('An error occurred while submitting the form. Please try again.');
    // }
});


    // alert('Validation Passed. Form will be submitted.');
    // Replace the line below with actual form submission logic if needed
    // e.target.closest('form').submit();

    /*
        learning            : type, pic, content
        challenge code      : type, question, code
        challenge options   : type, question, code, options
        exam code           : type, question, code, timer
        exam options        : type, question, code, options, timer

        jadi: module name, type, order, pic, content, question, code, options, timer


[
  {
    "id": "page-1",
    "type": "Learning",
    "question": "What is this about?",
    "options": [],
    "timer": null,
    "file": blob of data here
  },
  {
    "id": "page-2",
    "type": "Challenge Code",
    "question": "What is the correct syntax?",
    "options": [],
    "timer": null
  },
  {
    "id": "page-3",
    "type": "Challenge Option",
    "question": "Choose the correct answer.",
    "options": [
      {
        "id": "option-3-1",
        "value": "Option 1",
        "text": "Answer 1"
      },
      {
        "id": "option-3-2",
        "value": "Option 2",
        "text": "Answer 2"
      }
    ],
    "timer": null
  },
  {
    "id": "page-4",
    "type": "Exam Code",
    "question": "Write a function to calculate the sum.",
    "options": [],
    "timer": "00:30:00"
  }
]

    */