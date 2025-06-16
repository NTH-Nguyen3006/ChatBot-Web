const checkElement = document.getElementById("check-5");
document.getElementById("check-5").addEventListener("change", () => {
    let theme = (checkElement.checked) ? "light" : "dark";
    document.querySelector("[data-bs-theme]").setAttribute("data-bs-theme", theme);
    localStorage.setItem('theme', theme)
});

document.addEventListener("DOMContentLoaded", () => {
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        document.querySelector("[data-bs-theme]")
            .setAttribute('data-bs-theme', currentTheme);
        if (currentTheme == "dark") checkElement.checked = false;
        else checkElement.checked = true;
    } else {
        document.querySelector("[data-bs-theme]")
            .setAttribute('data-bs-theme', "light");
    }
});

const prompt = document.getElementById("prompt-text");

document.getElementById("form").addEventListener("submit", (e) => {
    e.preventDefault();
    if (prompt.value != "") {
        appendMessageBox(prompt.value, "user");
        sendMessageReq(prompt.value, "");
        prompt.value = "";
    }
    sendMessageBtn.classList.remove("show-send-btn");
});

const sendMessageBtn = document.getElementById("form");
prompt.addEventListener("keydown", (evt) => {
    if ((evt.key === "Enter" || evt.keyCode === 13) && !evt.shiftKey) {
        evt.preventDefault();
        document.getElementById("send-message").click();
    }
});

prompt.addEventListener("input", (evt) => {
    if (evt.target.value == "")
        sendMessageBtn.classList.remove("show-send-btn");
    else
        sendMessageBtn.classList.add("show-send-btn");
});

const copyBtns = document.querySelectorAll("#copy-code").forEach(btn => {
    btn.addEventListener("click", function () {
        console.log(this);

        const preElement = this.parentElement.parentElement.parentElement;
        const code_string = preElement.children.item(1).textContent;
        navigator.clipboard.writeText(code_string)
            .then(() => console.log('Text copied!'))
            .catch(() => console.log("copy faild"))
    });
});

function addImageEvent(img) {
    img.addEventListener("click", () => {
        document.querySelector(".image-modal").setAttribute("src", img.src);
        document.querySelector('button[data-bs-toggle="modal"]').click();
    });
}

function appendMessageBox(message, objectName = "user") {
    const divBox = document.createElement("div");
    const chatbox = document.getElementById("chat-box");
    divBox.className = `${objectName}-box`;
    if (objectName == "user")
        divBox.innerHTML = `<p class="p-3 text-tertiary" id="user-message">
            <span>${message}</span></p>`;
    else {
        // trường hợp là model
        divBox.id = "bot-message";
        divBox.innerHTML = marked.parse(message);
        if (divBox.querySelector("p>img")) {
            const imgEle = divBox.querySelector("p>img");
            imgEle.id = "bot-attchment";
            addImageEvent(imgEle);
        }
    }
    chatbox.appendChild(divBox);
    window.scrollTo(0, document.body.scrollHeight);
    return divBox;
}

function addToolBarCodeBox(title, element) {
    element.innerHTML += `<nav class="navbar"> 
            <div class="container"> <span>${title}</span>
            <button class="btn" aria-label="Copy" id="copy-code">
            <span><i class="bi bi-copy"></i></span></button></div></nav>`;
    element.insertBefore(element.lastChild, element.firstChild);
    const copy_btn = element.querySelector("#copy-code");
    copy_btn.addEventListener("click", () => {
        navigator.clipboard.writeText(element.lastChild.textContent)
            .then(() => {
                const copyIcon = copy_btn.cloneNode(true).innerHTML;
                const copySuccess_btn = '<span><i class="bi bi-check-lg"></i></span>';
                copy_btn.innerHTML = copySuccess_btn;
                setTimeout(() => copy_btn.innerHTML = copyIcon, 2000);
            });
    });
}

function selectPreElement(parentElement) {
    Array.from(parentElement.children).forEach((item) => {
        if (item.tagName == "PRE") {
            const firstChild = item.firstChild;
            if (firstChild?.tagName == "CODE") {
                console.log(firstChild.className);
                let language = firstChild.className.match(/language-[\w#.+]+/)[0].slice(9);
                language = (language == "undefined") ? "Kết quả" : language;
                addToolBarCodeBox(language, item);
            }
        }
        if (item.tagName == "UL" || item.tagName == "LI")
            selectPreElement(item);
    });
}

function botWriteText(textToWrite) {
    const divBotBox = appendMessageBox(textToWrite, "model");
    hljs.highlightAll();
    selectPreElement(divBotBox);
    Array.from(divBotBox.children).forEach((item, index) => {
        setTimeout(() => {
            item.classList.add('visible');
        }, index * 100);
    });
}

function sendMessageReq(userMessage, userAttachment) {
    fetch("/bot", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage, attchment: userAttachment })
    }).then(res => { if (res.ok) return res.json() })
        .then(data => {
            if (data.model) {
                let model_message = data.model.message;
                if (data.model.image)
                    model_message += "\n\n" + `![](${data.model.image})`;

                botWriteText(model_message);
                window.scrollTo(0, document.body.scrollHeight);
            }
        });
}

//



