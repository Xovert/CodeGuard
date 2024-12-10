document.querySelectorAll('[contenteditable="true"]').forEach(label => {
    label.addEventListener('click', function (e) {
        e.preventDefault();
        this.focus();
    });
});
