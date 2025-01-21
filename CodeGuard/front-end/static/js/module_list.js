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