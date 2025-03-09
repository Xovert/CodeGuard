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
    let moduleToDelete = null; // Stores the module to delete

    // Select all trash buttons
    document.querySelectorAll(".icon-trash").forEach(button => {
        button.addEventListener("click", function () {
            // Find the closest module container
            moduleToDelete = this.closest(".module");

            if (moduleToDelete) {
                // Get module name for the modal message
                const moduleName = moduleToDelete.querySelector(".module-name").textContent;

                // Update modal message
                const messageElement = document.getElementById("message");
                messageElement.innerHTML = `Are you sure you want to delete <strong>${moduleName}</strong> module?`;
            }
        });
    });

    // Handle delete confirmation
    document.getElementById("yes").addEventListener("click", function () {
        if (moduleToDelete) {
            // Get the deleted module's order number
            const deletedOrder = parseInt(moduleToDelete.querySelector(".order").textContent.replace("#", ""), 10);

            moduleToDelete.remove(); // Remove the module from the DOM
            moduleToDelete = null; // Reset the variable
            
            // update the order for all modules after the deleted one
            document.querySelectorAll(".module").forEach(module => {
                let orderElement = module.querySelector(".order");
                let currentOrder = parseInt(orderElement.textContent.replace("#", ""), 10);
    
                // Decrease the order number if it's greater than the deleted order
                if (currentOrder > deletedOrder) {
                    orderElement.textContent = `#${currentOrder - 1}`;
                }
            });
        }

        // Close the modal programmatically after deletion
        const modalElement = document.getElementById("delete");
        const deleteModal = bootstrap.Modal.getInstance(modalElement);
        deleteModal.hide(); // Hide the modal
    });
});



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


// ======= SEND DATA TO BACKEND ========
const saveButton = document.getElementById("save-changes");
saveButton.addEventListener("click", function () {
    let moduleOrder = [];
    document.querySelectorAll(".module").forEach((module, index) => {
        moduleOrder.push({
            order: module.querySelector('.order').textContent.replace('#', '').trim(),
            module_name: module.querySelector('.module-name').textContent.trim(),
        });
    });
    const course_name = encodeURIComponent(document.querySelector('.module-list-title').getAttribute('data-course-name'));
    
    fetch(`/admin/${course_name}/modules`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ modules: moduleOrder }),
    })
    .then(response => response.json())
    .then(data => {
        window.location.replace(data.url);
    })
    .catch(error => console.error("Fetch error:", error));
});