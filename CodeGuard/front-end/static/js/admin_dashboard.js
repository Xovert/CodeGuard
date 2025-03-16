// ====== SHOW OPTION =======
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

// option class toggle to prevent it overflow
document.addEventListener("DOMContentLoaded", () => {
    const courses = document.querySelectorAll(".course");

    courses.forEach((course) => {
        const moreButton = course.querySelector(".more");
        const option = course.querySelector(".option");

        moreButton.addEventListener("click", () => {
            // get the container and its boundary
            const container = course.closest(".course-wrapper").getBoundingClientRect();
            const optionBounds = option.getBoundingClientRect();

            // if it overflows to the right, move it to the left
            if (optionBounds.right > container.right) {
                option.classList.add("overflow-left");
            } 
            
            // it overflows to the left, move it to the left (keep it as it is)
            else {
                option.classList.remove("overflow-left");
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