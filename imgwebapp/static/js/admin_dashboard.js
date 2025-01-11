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