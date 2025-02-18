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

document.addEventListener('click', function (e){
    if (e.target.closest('.up')){
        const current = e.target.closest('.module');
        const previous = current?.previousElementSibling;

        if (previous && previous.classList.contains('module')) {
            current.parentNode.insertBefore(current, previous);  
            swapOrder(current, previous);
        }
    }

    else if (e.target.closest('.down')){
        const current = e.target.closest('.module');
        const next = current?.nextElementSibling;

        if (next && next.classList.contains('module')){
            current.parentNode.insertBefore(next, current);
            swapOrder(current, next);
        }
    }
});



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
            const messageElement = document.getElementById("message");
            messageElement.innerHTML = `Are you sure you want to delete <strong>${moduleName}</strong> module?`;
        });
    });
});



// ======== CHANGES TO DOM =========
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

    const initialPairs = getCurrentPairs();

    // Function to check for changes in the pairs
    function checkPairChanges() {
        const currentPairs = getCurrentPairs();
        if (JSON.stringify(currentPairs) === JSON.stringify(initialPairs)) {
            saveChanges.setAttribute("disabled", "true");
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

    // Initial check to set the button state
    checkPairChanges();
})