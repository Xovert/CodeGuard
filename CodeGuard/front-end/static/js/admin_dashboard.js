document.querySelectorAll('.more').forEach(more => {
    more.addEventListener('click', function (event) {
        const option = more.nextElementSibling; // Finds the sibling .option

        // Toggle the visibility of the current .option
        if (option && option.classList.contains('option')) {
            option.classList.toggle('d-none');
        }

        // Close other .option elements
        document.addEventListener('click', function (e) {
            if (!more.contains(e.target) && !option.contains(e.target)) {
                option.classList.add('d-none'); // Hide the current .option
            }
        });
    });
});

// melebihi container
document.addEventListener("DOMContentLoaded", () => {
    const courses = document.querySelectorAll(".course");

    courses.forEach((course) => {
        const moreButton = course.querySelector(".more");
        const option = course.querySelector(".option");

        moreButton.addEventListener("click", () => {
            // Get the container and element boundaries
            const container = course.closest(".course-wrapper").getBoundingClientRect();
            const optionBounds = option.getBoundingClientRect();

            // Check if the `.option` element overflows the container on the right
            if (optionBounds.right > container.right) {
                option.classList.add("overflow-left"); // Move to the left
            } else {
                option.classList.remove("overflow-left"); // Keep the default position
            }
        });
    });
});

// ===== DELETE COURSE =====
let courseToDelete = null;

// show modal
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('delete-btn')) {
        const courseElement = event.target.closest('.course');
        courseToDelete = courseElement.getAttribute('data-course-name');

        // Update the modal message
        document.getElementById('message').textContent = `Are you sure you want to delete "${courseToDelete}"?`;

        const option = courseElement.querySelector('.option');
        if(option && !option.classList.contains('d-none')){
            option.classList.add('d-none');
        }
    }
});

// if yes
document.getElementById('yes').addEventListener('click', () => {
    if (!courseToDelete) return;

    courseToDelete = encodeURIComponent(courseToDelete);
    fetch(`/admin/delete_course/${courseToDelete}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ course_name: courseToDelete })
    })
    .then(response => response.json())
    .then(data => {
        window.location.replace(data.url);
    })
    .catch(error => {
        console.error('Error:', error);
        courseToDelete = null;
    });
});

// if no
document.getElementById('no').addEventListener('click', () => {
    courseToDelete = null;
});