$(document).ready(function() {
    if (document.querySelector(".btn-submit") !== null){
        fetchAttempts(content_num)
        if (document.querySelector("#input-Text") === null){
            setBtnMultipleChoice() 
        }else{
            setBtnInputText()
        }
        hideError()
    }
})

async function fetchAttempts(content_num) {
    try {
        const response = await fetch(`${base_url}/get-attempts?content=${encodeURIComponent(content_num)}`); // Make a GET request to the backend
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json(); // Parse the JSON response
        console.log(data)
        if(data.isComplete){
            displayNext()
            hideSubmit()
            displayCorrect("You are correct!")
            if (document.querySelector("#input-Text") === null){
                disableRadio()
                setCorrectOption(data.selected)
            }else{
                disableInput()
                setInput(data.answer)
            }
            document.getElementById('attempts').textContent = ''; // Update the DOM
        }
        else if(data.attempts > 0) {
            document.getElementById('attempts').textContent = `${data.attempts}/3`; // Update the DOM
        }
        else if(data.attempts == 0){
            displayError("You've used all attempts!")
            hideSubmit()
            displayNext()
            if (document.querySelector("#input-Text") === null){
                disableRadio()
                setWrongOption(data.selected)
                showCorrectAnswer(data.correctAnswer, "multiple-choice");
            }else{
                disableInput()
                setInput(data.answer)
                showCorrectAnswer(data.correctAnswer, "input-text");
            }
        }else{
            document.getElementById('attempts').textContent = ''; // Update the DOM
        }
    } catch (error) {
        console.error('Error fetching attempts:', error);
        document.getElementById('attempts').textContent = ''; // Show error in the DOM
    }
}

function setBtnInputText(){
    document.querySelector('.btn-submit').addEventListener('click', async (event) => {
        event.preventDefault()
        const input_text = document.querySelector('#input-Text');
        
        if (!input_text.value) {
            displayError("Please input an answer.")
            return;
        }else{
            hideError()
        }
        
        const input_value = input_text.value;
        
        try {
            const response = await fetch(`${base_url}/check`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: "input_text",
                    answer: input_value,
                    content: content_num
                }),
            })
            
            const result = await response.json();
            
            if (result.status === true) {
                displayCorrect("You are correct!")
                hideSubmit()
                displayNext()
                disableRadio()
            }
            if (result.status === false){
                displayError("Wrong answer!")
            }
    
        } catch (error) {
            console.error('Error:', error);
            displayError("An error occurred. Please try again.")
        }
        fetchAttempts(content_num)
    });
}

function setBtnMultipleChoice(){
    document.querySelector('.btn-submit').addEventListener('click', async (event) => {
        event.preventDefault()
        const input_text = document.querySelector('input[name="answer"]:checked');
        
        if (!input_text) {
            displayError("Please select an answer.")
            return;
        }else{
            hideError()
        }
        
        const selectedValue = input_text.value;
        
        try {
            const response = await fetch(`${base_url}/check`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: "options",
                    answer: selectedValue,
                    content: content_num
                }),
            })
            
            const result = await response.json();
            console.log(result)
            
            if (result.status === true) {
                displayCorrect("You are correct!")
                hideSubmit()
                displayNext()
                disableRadio()
            }
            if (result.status === false){
                displayError("Wrong answer!")
            }
            if (result.status === "error"){
                displayError(result.error)
            }
    
        } catch (error) {
            console.error('Error:', error);
            displayError("An error occurred. Please try again.")
        }
        fetchAttempts(content_num)
    });
}

function disableRadio(){
    document.querySelectorAll('.form-check-input').forEach(radio => {
        radio.setAttribute('disabled', '')
    })
    document.querySelectorAll('.form-check-label').forEach(radio => {
        radio.classList.remove('label-hover')
    })
}

function disableInput(){
    document.querySelector('#input-Text').setAttribute('disabled', '')
}

function setInput(option_text){
    document.querySelector('#input-Text').value = option_text
}

function displayNext(){
    let button_next = document.querySelector('.btn-next')
    button_next.classList.remove('disabled')
    button_next.classList.add('active')
}

function hideNext(){
    let button_next = document.querySelector('.btn-next')
    button_next.classList.remove('active')
    button_next.classList.add('disabled')
}

function displaySubmit(){
    let button_submit = document.querySelector('.btn-submit')
    button_submit.classList.remove('disabled')
    button_submit.classList.add('active')
}

function hideSubmit(){
    let button_submit = document.querySelector('.btn-submit')
    button_submit.classList.remove('active')
    button_submit.classList.add('disabled')
}

function displayError(message){
    let errors = document.querySelector('#challengeError')
    errors.classList.remove('disabled')
    errors.classList.add('active')
    errors.textContent = message
    errors.style.color = "red"
}

function displayCorrect(message){
    let errors = document.querySelector('#challengeError')
    errors.classList.remove('disabled')
    errors.classList.add('active')
    errors.textContent = message
    errors.style.color = "var(--hard-green)"
}

function hideError(){
    let errors = document.querySelector('#challengeError')
    errors.classList.remove('active')
    errors.classList.add('disabled')
}

function setCorrectOption(option){
    const elem = document.querySelector(`#opt-${option}`)
    
    const parent = elem.parentElement;
    parent.classList.add('correct-option');
    
    const check = parent.querySelector('.check');
    check.classList.remove('disabled');
    check.classList.add('active');
}

function setWrongOption(option){
    const elem = document.querySelector(`#opt-${option}`)
    elem.setAttribute('checked', '')

    const parent = elem.parentElement;
    parent.classList.add('wrong-option');
    
    const cross = parent.querySelector('.cross');
    cross.classList.remove('disabled');
    cross.classList.add('active');
}

function showCorrectAnswer(data, type){
    if (type === "input-text") {
        const correct_infos = document.getElementsByClassName("correct-info");
        for (const elem of correct_infos){
            elem.classList.remove('disabled')
            elem.classList.add('active')
        }
        let answer = document.getElementById("correctAnswer")
        answer.textContent = `${data}`
    }
    if (type === "multiple-choice") {
        setCorrectOption(data)
    }
}
