// ======= RESIZE TEXTAREA =======
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

document.addEventListener("input", function (event) {
    if (event.target.tagName === "TEXTAREA") {
        autoResize(event.target);
    }
});


// ======= FILENAME CHANGES ====== + filename validation + PREVIEW
var save = true;

const fileInput = document.getElementById('course-logo');
const filenameSpan = document.querySelector('.filename');
const allowedExtensions = ['jpg', 'jpeg', 'png'];
const maxFileSize = 1 * 1024 * 1024;

var errorCourseLogo = document.getElementById('error-course-logo');

let file = fileInput.files[0];
const preview = document.getElementById("preview");
const filename = document.getElementById("filename").textContent.trim();

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0]

    // if there is file
    if (file) {
        const fileExtension = file.name.split('.').pop().toLowerCase();

        // if the ext is not in the list
        if (!allowedExtensions.includes(fileExtension)) {
            errorCourseLogo.textContent = `Invalid file type! Only ${allowedExtensions.join(', ')} are allowed.`;
            errorCourseLogo.style.display = 'block';

            fileInput.value = '';
            filenameSpan.textContent = 'No file chosen';

            // no preview
            preview.src = "";
            preview.style.display = "none";
            return;
        }

        // if file size is too large
        if (file.size > maxFileSize){
            errorCourseLogo.textContent = "Maximum file size is 1 MB!";
            errorCourseLogo.style.display = 'block';

            fileInput.value = '';
            filenameSpan.textContent = 'No file chosen';

            // no preview
            preview.src = "";
            preview.style.display = "none";
            return;
        }
        
        // Update span
        filenameSpan.textContent = file.name;
        errorCourseLogo.textContent = "";
        errorCourseLogo.style.display = "none";
        
        // preview image
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    }

    // no file chosen
    else if (!file){
        filenameSpan.textContent = 'No file chosen';
        errorCourseLogo.textContent = "";
        errorCourseLogo.style.display = 'none';
        preview.src = "";
        preview.style.display = 'none';
    }
});


// ====== more validation + sanitation ======
document.getElementById("submit-btn").addEventListener("click", function (event) {
    event.preventDefault();
    save = true;

    // clear previous errors
    document.querySelectorAll(".error-message").forEach(p => {
        p.style.display = "none";
        p.textContent = "";
    });

    // get values
    const title = document.getElementById("course-title").value.trim();
    const desc = document.getElementById("desc").value.trim();

    const errorTitle = document.getElementById("error-title");
    const errorDesc = document.getElementById("error-desc");

    // no empty validation
    if (!title){
        errorTitle.textContent = "Title cannot be empty!";
        errorTitle.style.display = "block";
        save = false;
    }

    if (fileInput.files.length === 0){
        errorCourseLogo.textContent = "Course image cannot be empty!";
        errorCourseLogo.style.display = "block";
        save = false;
    }

    if (!desc){
        errorDesc.textContent = "Description cannot be empty!";
        errorDesc.style.display = "block";
        save = false;
    }
    
    // submit if passes the validation
    if (save === true){
        document.querySelector("form").submit();
    }
});