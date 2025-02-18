var view;

document.addEventListener("DOMContentLoaded", async (event) => {
    let response = await getContent()
    timetime(response.duration, response.elapsed, document.querySelector('.progress-bar'))
    let content = response.code
    const lines = (String(content).match(/\n/g) || '').length + 1
    const height = Math.round((lines)*22.39)
    const max_height = Math.round((lines+20)*22.39)
    
    let options = {
        dark: true,
        styles: {
            "&":{
                "max-height": `${max_height}px`,
                width: "60vw",
                backgroundColor: "var(--dark-blue)",
                border: "5px solid var(--dark-blue)",
                borderRadius: "5px",
            },
            ".cm-gutter": {
                backgroundColor: "var(--dark-blue)",
            },
            ".cm-content, .cm-gutter": {
                minHeight: `${height}px`,
            },
            ".cm-scroller": {
                overflow: "auto",
            },
            ".cm-scroller::-webkit-scrollbar:vertical": {
                display: "none",
            },
            ".cm-activeLineGutter": {
                backgroundColor: "var(--dark-blue)",
            },
        },
        lineWrapping: false,
        save_keymap: {
            key: "Mod-s",
            run: saveState,
        },
    }
    let editor = document.querySelector("#editor")
    
    view = cm6.load().newEditor(editor, content, options);
    const initialState = view.state

    let resetEl = document.querySelector('#reset')
    resetEl.addEventListener('click', (event) => {
        view.setState(initialState)
    });

    let submitEl = document.querySelector('#btnSubmit')
    submitEl.addEventListener('click', (event) => {
        submit(view)
    })
});

function submit(view){
    let answer = view.state.doc.toString()
    fetch(baseURL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: answer }),
    })
    .then(response => {
        if (!response.ok){
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        window.location.replace(data.url)
    })
    .catch(error => console.error('An error occured:', error));
}

async function saveState(view){
    await fetch(statusURL, {
        method: "POST",
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(view.state.toJSON())
    })

    const toastContainer = document.querySelector('.toast-container')
    let toastId = "toast-" + Date.now();
    let toastHTML = `
    <div id="${toastId}" class="toast align-items-center fade" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
          <div class="toast-body d-flex align-items-center gap-3">
            <svg width="24" height="24" xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" clip-rule="evenodd" image-rendering="optimizeQuality" shape-rendering="geometricPrecision" text-rendering="geometricPrecision" viewBox="0 0 1778.69 1778.68" id="check">
                <path fill-rule="nonzero" d="M1254.85 558.21c28.97,-28.97 75.96,-28.97 104.93,0 28.97,28.98 28.97,75.97 0,104.94l-557.28 557.3c-28.98,28.97 -75.97,28.97 -104.94,0l-278.65 -278.65c-28.97,-28.97 -28.97,-75.96 0,-104.93 28.98,-28.98 75.97,-28.98 104.94,0l226.18 226.18 504.82 -504.84zm-365.51 -558.21c245.55,0 467.91,99.56 628.85,260.5 160.94,160.93 260.5,383.3 260.5,628.84 0,245.58 -99.55,467.91 -260.5,628.85 -160.94,160.94 -383.3,260.5 -628.85,260.5 -245.57,0 -467.91,-99.55 -628.84,-260.5 -160.96,-160.94 -260.5,-383.27 -260.5,-628.85 0,-245.54 99.56,-467.91 260.5,-628.84 160.93,-160.96 383.27,-260.5 628.84,-260.5zm523.92 365.43c-134.07,-134.06 -319.31,-216.99 -523.92,-216.99 -204.62,0 -389.86,82.93 -523.91,216.99 -134.06,134.06 -216.99,319.31 -216.99,523.91 0,204.63 82.93,389.87 216.99,523.92 134.05,134.06 319.29,216.98 523.91,216.98 204.61,0 389.85,-82.92 523.92,-216.98 134.06,-134.05 216.98,-319.29 216.98,-523.92 0,-204.6 -82.92,-389.85 -216.98,-523.91z" fill="#54cc52" class="color000000 svgShape"></path>
            </svg>
            <strong>Your code has been saved!</strong>
          </div>
          <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    </div>
    `
    toastContainer.insertAdjacentHTML("beforeend", toastHTML);
    let toastEl = document.getElementById(toastId);

    const theToast = bootstrap.Toast.getOrCreateInstance(toastEl, {delay: 3000})
    theToast.show()

    toastEl.addEventListener("hidden.bs.toast", () =>{
        toastEl.remove();
    })

    return true;
}

async function getContent(){
    try {
        const response = await fetch(statusURL);
        const data = await response.json();
        // Do something with content here
        return data
    } catch (error) {
        console.error('Error fetching exam content', error);
    }
}


function startTimer(duration, elapsed, display) {
    var start = Date.now();
    var end = start + (duration - elapsed) * 1000;
    var progressBar = document.querySelector('.progress-bar');

    function updateTimer() {
        var now = Date.now();
        var remaining = Math.max(0, Math.floor((end - now) / 1000));

        var hours = Math.floor(remaining / 3600);
        var remainder = remaining % 3600;
        var minutes = Math.floor(remainder / 60);
        var seconds = remainder % 60;

        hours = formatTime(hours);
        minutes = formatTime(minutes);
        seconds = formatTime(seconds);

        display.textContent = hours + ":" + minutes + ":" + seconds;

        var currElapsed = duration - remaining;
        var progress = (currElapsed / duration) * 100;
        progressBar.style.width = `${progress}%`;

        if (remaining <= 0) {
            progressBar.style.width = '100%';
            progressBar.addEventListener('transitionend', function handler() {
                progressBar.removeEventListener('transitionend', handler);
                submit(view)
            });
        } else {
            requestAnimationFrame(updateTimer);
        }
    }

    updateTimer();
}

function timetime (time, elapsed, bar) {
    var display = document.querySelector('#timerDisplay');
    if (elapsed < 0){
        display.textContent = "00:00:00";
        return
    }
    bar.style.width = (elapsed / time) * 100;
    startTimer(time, elapsed, display);
};


function formatTime(num) {
    return num.toLocaleString('en-US', {
        minimumIntegerDigits: 2, 
        useGrouping:false
    });
}