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






// ======== CHANGES TO DOM =========
document.addEventListener("DOMContentLoaded", () => {
    // Select the target element to observe
    const moduleWrapper = document.querySelector(".module-wrapper");
    const actionButton = document.getElementById("save-changes"); // Replace with your button's ID or selector
  
    function getCurrentOrder() {
        return Array.from(moduleWrapper.querySelectorAll(".module .order")).map(span => span.textContent.trim());
    }

    // Store the initial order of the modules
    const initialOrder = getCurrentOrder();

    // Function to check for changes in the structure
    function checkOrderChanges() {
        const currentOrder = getCurrentOrder();
        if (JSON.stringify(currentOrder) === JSON.stringify(initialOrder)) {
            actionButton.setAttribute("disabled", "true");
        } else {
            actionButton.removeAttribute("disabled");
        }
    }

    // Create a MutationObserver to monitor structural changes
    const observer = new MutationObserver(() => {
        checkOrderChanges(); // Recheck structure changes when DOM mutations occur
    });

    // Start observing the module wrapper
    observer.observe(moduleWrapper, {
        childList: true, // Detect added/removed children
        subtree: true,   // Detect changes within children
    });

    // Initial check to set the button state
    checkOrderChanges();
})