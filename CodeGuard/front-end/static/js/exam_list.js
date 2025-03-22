// ======= MOVE UP + DOWN =========
function swapOrder(element1, element2){
    const span1 = element1.querySelector('.order');
    const span2 = element2.querySelector('.order');

    if (span1 && span2){
        let temp = span1.textContent;
        span1.textContent = span2.textContent;
        span2.textContent = temp;
    }
}

// ======== DELETE ========
document.addEventListener("DOMContentLoaded", function () {
    // Select all the trash buttons
    const trashButtons = document.querySelectorAll(".icon-trash");
    
    // Add a click event listener to each trash button
    trashButtons.forEach((button) => {
        button.addEventListener("click", function () {
            // Find the parent .module element of the clicked button
            const moduleElement = button.closest(".module");
            
            // Get the module name from the .module-name element inside the module
            const moduleName = moduleElement.querySelector(".module-name").textContent.trim();

            // Update the modal's message with the module name
            confirmMessage(`Are you sure you want to delete <strong>${moduleName}</strong> exam?`);
        });
    });
});

document.getElementById('confirmModal').addEventListener('show.bs.modal', (event) => {
    let clickedButton = event.relatedTarget;
    let modal = event.currentTarget;

    if (clickedButton.classList.contains('icon-trash')){
        const examNumber = clickedButton.dataset.examNumber;
        modal.dataset.examNumber = examNumber;
        modal.dataset.action = 'delete'
    }else if (clickedButton.id === 'save-changes'){
        modal.dataset.action = 'save'
    }
})

document.getElementById('confirmButton').addEventListener('click', async (event) => {
    let modal = document.getElementById('confirmModal');
    let action = modal.dataset.action;
    delete modal.dataset.action;
    let confirmModal = bootstrap.Modal.getOrCreateInstance(modal)

    if (action === 'delete') {
        let examNumber = modal.dataset.examNumber;
        let examElement = document.getElementById(`exam-${examNumber}`)
        delete modal.dataset.examNumber;
        if (examElement) {
            examElement.remove();
        }
        confirmModal.hide()
    } else if (action === 'save') {
        let confirmButton = modal.querySelector('#confirmButton');
        let cancelButton = modal.querySelector('#no');
        let textSpan = document.getElementById('confirmButtonText');

        confirmButton.setAttribute('disabled', 'disabled')
        cancelButton.setAttribute('disabled', 'disabled')
        
        if (textSpan) {
            textSpan.textContent = ''
        }
        enableSpinner(confirmButton)
        
        try {
            var data = await deleteExam();
        } catch (error) {
            console.error('Error during exam deletion:', error);
            showInfo('An error has occurred while saving changes!');
        }
        
        removeSpinner(confirmButton)
        
        if(textSpan) {
            textSpan.textContent = 'Yes'
        }
        confirmButton.removeAttribute('disabled')
        cancelButton.removeAttribute('disabled')
        confirmModal.hide()
        
        if (data.status === 'success') {
            showInfo('Changes saved successfully!');
        }
        if (data.status === 'failed') {
            showInfo('Failed saving changes!');
        }
        // Reset Observer State so that you can't do save changes more.
        window.resetObserverState();
    }
})

async function deleteExam(){
    const headingText = document.querySelector('.title > h1').textContent;
    const course_name = headingText.substring(headingText.indexOf('for') +4 ).trim();
    const examNumbers = Array.from(document.querySelectorAll('.module button.icon-trash')).map(button => button.dataset.examNumber);

    if ( !window.hasChanged() ) {
        showInfo("Unable to save, no changes detected!");
        return Promise.resolve("No changes yet!");
    }

    return fetch(`/admin/${course_name}/exams/delete`,{
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({
            numbers:examNumbers
        })
    })
    .then(response=>{
        if(!response.ok){
            throw new Error('Network response was not ok!')
        }
        return response.json();
    })
    .then(data => {
        return data;
    })
    .catch(error => {
        throw error;
    })
}

// ======== CHANGES TO SAVE BUTTON =========
document.addEventListener("DOMContentLoaded", () => {
    // Select the target element to observe
    const moduleWrapper = document.querySelector(".module-wrapper");
    const saveChanges = document.getElementById("save-changes"); // Replace with your button's ID or selector
    
    function getCurrentPairs() {
        return Array.from(moduleWrapper.querySelectorAll(".module")).map(module => {
            const order = module.querySelector(".order")?.textContent.trim() || "";
            const moduleName = module.querySelector(".module-name")?.textContent.trim() || "";
            return `${order} ${moduleName}`;
        });
    }
    
    let initialPairs = getCurrentPairs();
    
    // Function to check for changes in the pairs
    function checkPairChanges() {
        const currentPairs = getCurrentPairs();
        if (JSON.stringify(currentPairs) === JSON.stringify(initialPairs)) {
            saveChanges.disabled = true;
        } else {
            saveChanges.removeAttribute("disabled");
        }
    }
    
    // Create a MutationObserver to monitor structural changes
    const observer = new MutationObserver(() => {
        checkPairChanges(); // Recheck pairs when DOM mutations occur
    });
    
    // Start observing the module wrapper
    observer.observe(moduleWrapper, {
        childList: true, // Detect added/removed children
        subtree: true,   // Detect changes within children
    });
    
    function resetObserverState() {
        initialPairs = getCurrentPairs();
        observer.takeRecords();
        checkPairChanges();
    }
    // Expose function globally
    window.resetObserverState = resetObserverState;
    window.hasChanged = () => (JSON.stringify(getCurrentPairs()) !== JSON.stringify(initialPairs) );

    // Initial check to set the button state
    checkPairChanges();
})

function showInfo(message){
    const elem = document.getElementById('examInfo');
    elem.querySelector('#infoText').textContent = message;
    let modalInstance = bootstrap.Modal.getInstance(elem);
    if(!modalInstance){
        modalInstance = new bootstrap.Modal(elem);
    }
    modalInstance.toggle();
}

// ======= SEND DATA TO BACKEND ========
document.getElementById('save-changes').addEventListener("click", function () {
    confirmMessage('Are you sure you want to save your changes?');
});

function confirmMessage(message){
    let modalText = document.getElementById('confirmMessage');
    modalText.innerHTML = message;
}

function enableSpinner(elem){
    const spinner = elem.querySelector('.spinner-border');
    const spinnerText = elem.querySelector('[role="status"]');
    if (spinner) {
        spinner.classList.remove('d-none');
    }
    if (spinnerText) {
        spinnerText.classList.remove('d-none');
    }
}

function removeSpinner(elem){
    const spinner = elem.querySelector('.spinner-border');
    const spinnerText = elem.querySelector('[role="status"]');
    if (spinner) {
        spinner.classList.add('d-none');
    }
    if (spinnerText) {
        spinnerText.classList.add('d-none');
    }
}