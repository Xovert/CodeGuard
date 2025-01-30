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
// function showErrorModal(message, yesText, noText) {
//     // Get the modal element and the message container
//     const modalElement = document.getElementById('Error');
//     const messageElement = document.getElementById('message');
//     const yes = document.getElementById('yes');
//     const no = document.getElementById('no');

//     // Update the message dynamically
//     messageElement.textContent = message;
//     yes.textContent = yesText;
//     no.textContent = noText;

//     // Use Bootstrap's modal API to show the modal
//     const errorModal = new bootstrap.Modal(modalElement);
//     errorModal.show();
// }

// document.addEventListener('DOMContentLoaded', () => {
//     document.querySelectorAll('.icon-trash').forEach(button => {
//         button.addEventListener('click', () => {
//             // Customize the error message based on the clicked button or context
//             const moduleName = button.closest('.module')?.querySelector('.module-name')?.textContent.trim();
//             const message = moduleName
//                 ? `Are you sure you want to delete "${moduleName}"?`
//                 : 'Are you sure you want to delete this item?';

//             // Show the modal with the custom message
//             showErrorModal(message, "Yes", "No");
//         });
//     }); 
// })

function loadModalContent() {
    // Create the XMLHttpRequest object
    var xhttp = new XMLHttpRequest();

    // Define the callback for when the request completes
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            // Insert the fetched modal content into the modal container
            const modalContainer = document.getElementById("modal-container");

            if (modalContainer) {
                modalContainer.innerHTML = this.responseText;

                // Get the dynamically loaded modal
                const modalElement = document.getElementById("Error");

                // Ensure the modal element exists
                if (modalElement) {
                    // Initialize the modal using Bootstrap's modal API
                    const errorModal = new bootstrap.Modal(modalElement);

                    // Show the modal
                    errorModal.show();
                } else {
                    console.error("Modal element not found after loading content.");
                }
            } else {
                console.error("Modal container not found.");
            }
        }
    };

    // Send the GET request to fetch the modal content
    xhttp.open("GET", "confirm_changes", true); // Update the path to your modal.html file
    xhttp.send();
}

// Attach an event listener to the .icon-trash button
document.querySelectorAll(".icon-trash").forEach(button => {
    button.addEventListener("click", function () {
        loadModalContent();
    });
});

// document.addEventListener('DOMContentLoaded', () => {
//     // Load the modal HTML dynamically
//     function loadModal(callback) {
//         fetch('/admin/course/confirm_changes') // Adjust this path to the location of your modal.html
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Failed to load modal');
//                 }
//                 return response.text();
//             })
//             // PROBLEM HERE
//             .then(html => {
//                 // Append the modal to the body if it doesn't already exist
//                 const tempDiv = document.createElement('div');
//                 tempDiv.innerHTML = html;
//                 const modalElement = tempDiv.querySelector('#Error');
//                 if (modalElement) {
//                     // Check if the modal already exists in the DOM
//                     if (!document.body.contains(modalElement)) {
//                         // Find the `.content` element
//                         const contentElement = document.querySelector('.content');

//                         if (contentElement) {
//                             // Insert the modal before the `.content` element
//                             document.body.insertBefore(modalElement, contentElement);
//                         } else {
//                             // Fallback: Append to the body if `.content` is not found
//                             document.body.appendChild(modalElement);
//                         }
//                     }
//                 } else {
//                     console.error('Modal element not found in the fetched HTML.');
//                 }

//                 if (callback) callback();
//             })
//             .catch(error => console.error(error));
//             // PROBLEM HERE
//     }

//     // Function to show the modal with a custom message
//     function showErrorModal(message) {
//         const modalElement = document.getElementById('Error');
//         const messageElement = modalElement.querySelector('#message');

//         // Update the message dynamically
//         messageElement.textContent = message;

//         // Use Bootstrap's modal API to show the modal
//         const errorModal = new bootstrap.Modal(modalElement);
//         errorModal.show();
//     }

//     // Add click event listeners to all .icon-trash buttons
//     document.querySelectorAll('.icon-trash').forEach(button => {
//         button.addEventListener('click', () => {
//             const moduleName = button.closest('.module')?.querySelector('.module-name')?.textContent.trim();
//             const message = moduleName
//                 ? `Are you sure you want to delete "${moduleName}"?`
//                 : 'Are you sure you want to delete this item?';

//             // Load the modal and then show it with the message
//             loadModal(() => {
//                 showErrorModal(message);
//             });
//         });
//     });
// });




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