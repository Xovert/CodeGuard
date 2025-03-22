var view;

document.addEventListener("DOMContentLoaded", (event) => {
    let max_height = 1700;
    let height = 400;
    let options = {
        dark: true,
        styles: {
            "&":{
                "max-height": `${max_height}px`,
                backgroundColor: "var(--dark-blue)",
                border: "5px solid var(--dark-blue)",
                borderRadius: "5px",
            },
            ".cm-gutter": {
                backgroundColor: "var(--dark-blue)",
            },
            ".cm-content, .cm-gutter": {
                minHeight: `${height}px`,
            },
            ".cm-scroller": {
                overflow: "auto",
            },
            ".cm-scroller::-webkit-scrollbar:vertical": {
                display: "none",
            },
            ".cm-activeLineGutter": {
                backgroundColor: "var(--dark-blue)",
            },
        },
        lineWrapping: false,
    }
    let editor = document.querySelector("#code");
    view = cm6.load().textarea(editor, options);

    let labels = document.querySelectorAll('.form-label');
    labels.forEach((element) => {
        element.innerHTML += '<span class="asterisk">*</span>';
    })


})

document.querySelector('#exam-form').addEventListener('submit', function (e) {
    // e.preventDefault(); // if using async
    document.querySelectorAll('.timer-item').forEach((element) => {
        if (element.value === "") {
            element.value = 0
        }
    })
    // this.submit() // if using async
});

function checkAll(){
    let isNameCorrect = checkName();
    let isDurationCorrect = checkDuration();
    let isQuestionCorrect = checkQuestion();
    let isCodeCorrect = checkCode();
    let isTodoCorrect = checkTodo();
    if (isNameCorrect && isDurationCorrect && isQuestionCorrect && isCodeCorrect && isTodoCorrect) {
        return true;
    }
    return false;
}

function checkName(){
    let elem = document.getElementById('exam-name')
    let error = elem.parentElement.nextElementSibling;

    if (elem.value === "") {
        error.textContent = 'Exam Name must not be empty!';
        error.classList.add('d-inline-block');
        return false;
    } else {
        error.textContent = '';
        error.classList.remove('d-inline-block');
        return true;
    }
}

function checkDuration(){
    let duration = document.getElementById('duration');
    let hoursElem = document.getElementById('hours');
    let minutesElem = document.getElementById('minutes');
    let error = duration.nextElementSibling;

    if (hoursElem.value === "" && minutesElem.value === "") {
        return doError(error, "Duration cannot be empty!");
    }

    let hours = parseInt(hoursElem.value);
    let minutes = parseInt(minutesElem.value);

    if (hoursElem.value === "" && minutes === 0) {
        return doError(error, "Duration cannot be empty!");
    }

    if (hours === 0 && minutesElem.value === "") {
        return doError(error, "Duration cannot be empty!");
    }

    if ( hours === 0 && minutes === 0 ) {
        return doError(error, "Duration cannot be zero!");
    } 
    
    if ( hours < 0 || hours > 99 ) {
        return doError(error, "Hours must be between 0 and 99!");
    } 
    
    if ( minutes < 0 || minutes > 59 ) {
        return doError(error, "Minutes must be between 0 and 59!");
    } 

    return cleanError(error);
}

function checkQuestion(){
    let question = document.getElementById('question');
    let error = question.nextElementSibling;

    if ( question.value === "" ) {
        error.textContent = 'Question must not be empty!';
    } else if ( question.value.length > 500 ) {
        error.textContent = 'Question must not exceed 500 characters!';
    } else if ( question.value.length < 1 ) {
        error.textContent = 'Question cannot be less than 0 characters!';
    } else { 
        error.textContent = '';
        error.classList.remove('d-inline-block');
        return true;
    }
    error.classList.add('d-inline-block');
    return false;
}

function checkCode(){
    let code = view.state.doc.toString()
    let error = document.getElementById('playground').nextElementSibling;

    if (code === "") {
        error.textContent = 'Code must not be empty!';
    } else {
        error.textContent = ''
        error.classList.remove('d-inline-block');
        return true;
    }
    error.classList.add('d-inline-block');
    return false;
}

function checkTodo(){
    let elem = document.getElementById('todo');
    let error = elem.parentElement.nextElementSibling;

    if ( elem.value === "") {
        return doError(error, "Todo count must not be empty!");
    } 

    let todo = parseInt(elem.value);
    
    if ( todo === 0 ) {
        return doError(error, "Todo count cannot be zero!");
    } 
    
    if ( todo < 1 || todo > 10) {
        return doError(error, "Todo count must be between 1 and 10!");
    } 

    return cleanError(error);
}

function doError(elem, message){
    elem.textContent = message;
    elem.classList.add('d-inline-block');
    return false;
}

function cleanError(elem){
    elem.textContent = '';
    elem.classList.remove('d-inline-block');
    return true;
}

function showError(message) {
    let elem = document.getElementById('error-all')
    elem.textContent = message;
    elem.classList.add('d-inline-block')
}

function closeError() {
    let elem = document.getElementById('error-all')
    elem.textContent = '';
    elem.classList.remove('d-inline-block')
}

function confirm(message, purpose){
    let elem = document.getElementById('confirmModal')
    let modal = bootstrap.Modal.getOrCreateInstance(elem)
    let confirmMessage = elem.querySelector('#confirmMessage')
    
    confirmMessage.textContent = message;
    elem.dataset.purpose = purpose;
    modal.show()
}

function closeModal(message){
    let elem = document.getElementById('confirmModal')
    let modal = bootstrap.Modal.getOrCreateInstance(elem)
    let confirmMessage = elem.querySelector('#confirmMessage')
    
    confirmMessage.textContent = '';
    modal.hide()
}

document.getElementById('submit-btn').addEventListener('click', (e) => {
    if ( !checkAll() ) {
        showError('There are still errors!')
    } else {
        closeError();
        confirm('Are you ready to save the new exam?', "submit");
    }
})

document.getElementById("cancel-btn").addEventListener("click", (e) => {
    confirm("You have unsaved changes. If you leave this page, your changes will be lost. Are you sure you want to continue?", "cancel");
})

document.getElementById('confirmButton').addEventListener('click', async (event) => {
    let elem = document.getElementById('confirmModal');
    let form = document.getElementById('exam-form');
    closeModal();
    var purpose = elem.dataset.purpose;
    delete elem.dataset.purpose;

    if ( purpose === "submit" ) {
        form.requestSubmit();
    } else if ( purpose === "cancel" ) {
        var btn = document.getElementById("cancel-btn");
        var replaceUrl = btn.dataset.backUrl;
        delete btn.dataset.backUrl;
        window.location.replace(replaceUrl);
    }
})


// ===== ACCORDION (AMAN) =====
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

// generate random ID function
function generateID(type) {
    // return Date.now();
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
                console.log(forAttribute)
                const parts = forAttribute.split("-");
                const index = parseInt(parts[1], 10);

                if (index > maxIndex) {
                    maxIndex = index; // Update max index
                    console.log(`max index now = ${maxIndex}`)
                }
            }
        }
    });

    if(!avail){
        console.log("gaada, not avail")
        console.log(maxIndex);
        return maxIndex;
    }
    console.log(maxIndex + 1)
    return maxIndex + 1;
}

// RANDOMIZE ID
/**
 * @param {HTMLElement} container - The container element to randomize IDs for
 */
function randomizeLearningId(container, randID) {
    // type
    // const typeInput = container.querySelector('.type > input');
    // const typeLabel = container.querySelector('.type > label');
    // if (typeInput && typeLabel) {
    //     const randomID = `learning-${randID}`;
    //     typeInput.id = randomID; // Update the input ID
    //     typeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    // }

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

function randomizeChallengeCodeId(container, randID){
    // type
    // const typeInput = container.querySelector('.type > input');
    // const typeLabel = container.querySelector('.type > label');
    // if (typeInput && typeLabel) {
    //     const randomID = `challenge-code-${randID}`;
    //     typeInput.id = randomID; // Update the input ID
    //     typeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    // }
    
    // order
    const order = container.querySelector('.hidden');
    if (order){
        const randomID = `challenge_code-${randID}-order`;
        order.id = order.name = randomID;
    }

    // question
    const questionTextarea = container.querySelector('.question > textarea');
    const questionLabel = container.querySelector('.question > label');
    if (questionTextarea && questionLabel) {
        const randomID = `challenge_code-${randID}-question`;
        questionTextarea.id = questionTextarea.name = randomID; // Update the textarea ID
        questionLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }

    // code area
    const codeTextarea = container.querySelector('.code-playground > textarea');
    const codeLabel = container.querySelector('.code > label');
    if (codeTextarea && codeLabel) {
        const randomID = `challenge_code-${randID}-code`;
        codeTextarea.id = codeTextarea.name = randomID; // Update the textarea ID
        codeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    }
}

function randomizeChallengeOptionId(container, randID){
    // type
    // const typeInput = container.querySelector('.type > input');
    // const typeLabel = container.querySelector('.type > label');
    // if (typeInput && typeLabel) {
    //     const randomID = `challenge-option-${randID}`;
    //     typeInput.id = randomID; // Update the input ID
    //     typeLabel.setAttribute('for', randomID); // Update the label's 'for' attribute
    // }

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

function randomizeExamCodeId(container, randID) {
    // const typeInput = container.querySelector(".type > input");
    // const typeLabel = container.querySelector(".type > label");
    // if (typeInput && typeLabel) {
    //     const newTypeID = `exam-code-type-${randID}`;
    //     typeInput.setAttribute("id", newTypeID);
    //     typeLabel.setAttribute("for", newTypeID);
    // }

    // order
    const order = container.querySelector('.hidden');
    if (order){
        const randomID = `exam_code-${randID}-order`;
        order.id = order.name = randomID;
    }

    // Randomize .timer > input and label
    const timerInput = container.querySelector(".timer > input");
    const timerLabel = container.querySelector(".timer > label");
    if (timerInput && timerLabel) {
        const newTimerID = `exam_code-${randID}-timer`;
        timerInput.setAttribute("id", newTimerID);
        timerInput.setAttribute("name", newTimerID);
        timerLabel.setAttribute("for", newTimerID);
    }

    // Randomize .question > textarea and label
    const questionTextarea = container.querySelector(".question > textarea");
    const questionLabel = container.querySelector(".question > label");
    if (questionTextarea && questionLabel) {
        const newQuestionID = `exam_code-${randID}-question`;
        questionTextarea.setAttribute("id", newQuestionID);
        questionTextarea.setAttribute("name", newQuestionID);
        questionLabel.setAttribute("for", newQuestionID);
    }

    // Randomize .code-playground > textarea and .code > label
    const codeTextarea = container.querySelector(".code-playground > textarea");
    const codeLabel = container.querySelector(".code > label");
    if (codeTextarea && codeLabel) {
        const newCodeID = `exam_code-${randID}-code`;
        codeTextarea.setAttribute("id", newCodeID);
        codeTextarea.setAttribute("name", newCodeID);
        codeLabel.setAttribute("for", newCodeID);
    }
}

function randomizeExamOptionId(container, randID){
    // const typeInput = container.querySelector(".type > input");
    // const typeLabel = container.querySelector(".type > label");
    // if (typeInput && typeLabel) {
    //     const newTypeID = `exam-option-type-${randID}`;
    //     typeInput.setAttribute("id", newTypeID);
    //     typeLabel.setAttribute("for", newTypeID);
    // }

    // order
    const order = container.querySelector('.hidden');
    if (order){
        const randomID = `exam_options-${randID}-order`;
        order.id = order.name = randomID;
    }

    // Randomize .timer > input and label
    const timerInput = container.querySelector(".timer > input");
    const timerLabel = container.querySelector(".timer > label");
    if (timerInput && timerLabel) {
        const newTimerID = `exam_options-${randID}-timer`;
        timerInput.setAttribute("id", newTimerID);
        timerInput.setAttribute("name", newTimerID);
        timerLabel.setAttribute("for", newTimerID);
    }

    // Randomize .question > textarea and label
    const questionTextarea = container.querySelector(".question > textarea");
    const questionLabel = container.querySelector(".question > label");
    if (questionTextarea && questionLabel) {
        const newQuestionID = `exam_options-${randID}-question`;
        questionTextarea.setAttribute("id", newQuestionID);
        questionTextarea.setAttribute("name", newQuestionID);
        questionLabel.setAttribute("for", newQuestionID);
    }

    // Randomize .code-playground > textarea and .code > label
    const codeTextarea = container.querySelector(".code-playground > textarea");
    const codeLabel = container.querySelector(".code > label");
    if (codeTextarea && codeLabel) {
        const newCodeID = `exam_options-${randID}-code`;
        codeTextarea.setAttribute("id", newCodeID);
        codeTextarea.setAttribute("name", newCodeID);
        codeLabel.setAttribute("for", newCodeID);
    }

    const optionsContainer = container.querySelector('.option');
    const randomID = `exam_options-${randID}`;
    const optionID = `${randomID}-options`;
    const hiddenID = `${randomID}-choices`;

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