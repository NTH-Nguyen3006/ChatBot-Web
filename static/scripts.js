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
});

const sendMessageBtn = document.getElementById("form");
prompt.addEventListener("keydown", (evt) => {
    if ((evt.key === "Enter" || evt.keyCode === 13) && !evt.shiftKey) {
        evt.preventDefault();
        document.getElementById("send-message").click();
        sendMessageBtn.classList.remove("show-send-btn");
    }
});

prompt.addEventListener("input", (evt) => {
    if (evt.target.value == "")
        sendMessageBtn.classList.remove("show-send-btn");
    else
        sendMessageBtn.classList.add("show-send-btn");
});

function appendMessageBox(message, objectName = "user") {
    const divBox = document.createElement("div");
    const chatbox = document.getElementById("chat-box");
    divBox.className = `${objectName}-box p-3`;

    if (objectName == "user")
        divBox.innerHTML = `<p class="p-3 text-tertiary" id="user-message">
            <span>${message}</span></p>`;
    else {
        // trường hợp là model
        divBox.id = "bot-message";
        divBox.innerHTML = marked.parse(message);
    }
    chatbox.appendChild(divBox);
    window.scrollTo(0, document.body.scrollHeight);
    return divBox;
}

function botWriteText(textToWrite) {
    appendMessageBox(textToWrite, "model");
    const bot_messages = document.querySelectorAll("#bot-message");
    Array.from(bot_messages[bot_messages.length - 1].children)
        .forEach((item, index) => {
            console.log("item: ", item);
            setTimeout(() => {
                item.classList.add('visible');
            }, index * 150);
        });
}

function sendMessageReq(userMessage, userAttachment) {
    const formData = new FormData();
    formData.append("message", userMessage);
    formData.append("attchment", userAttachment);

    fetch("/bot", {
        method: "POST",
        body: formData
    }).then(res => { if (res.ok) return res.json() }
    ).then(data => {
        if (data.model) {
            botWriteText(data.model)
            hljs.highlightAll();
        }
    });
}

function addToolBarCodeBox() {
    document.querySelector('code.hljs[data-highlighted="yes"]')
}

const delay = ms => new Promise(res => setTimeout(res, ms));

const message = `
Chào bạn! Tôi là một trợ lý ảo.
Đây là một **tin nhắn mẫu** với _một vài_ định dạng.
Bạn có thể thấy hiệu ứng gõ chữ của tôi.

\`Đây là một đoạn code inline\`

Đây là một khối code:
\`\`\`CS
public static void Main() {
    Console.Writeline("Hello World!");
}
\`\`\`

Cảm ơn bạn đã theo dõi!
`;

// botWriteText(message, null)
botWriteText(message)

