function handleFileChange(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const image = document.querySelector('.profile-picture');
            image.src = e.target.result; // Update the image source
        };
        reader.readAsDataURL(file);
    }
}