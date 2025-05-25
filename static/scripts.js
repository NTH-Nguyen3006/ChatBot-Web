
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
        sendMessageReq(prompt.value, "")
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

appendUserMessageBox("ádbasdbaskdjkjdfhlakdjfhalkdsjfhaslkdfjh");

// var divUserBox;
function appendMessageBox(message, objectName = "user") {
    const divBox = document.createElement("div");
    const chatbox = document.getElementById("chat-box");
    divBox.className = `${objectName}-box p-3`;
    divBox.innerHTML = `<p class="m-0 text-tertiary" id="${objectName}-message">${message}</p>`;
    chatbox.appendChild(divUserBox);
    window.scrollTo(0, document.body.scrollHeight);
}

function writeText(textToWrite, elementAdopt, charIndex = 0) {
    elementAdopt.innerHTML = marked.parse(textToWrite);
    document.querySelectorAll("#bot-message>*").forEach((item, index) => {
        console.log(item);
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
        if (data.message) {
            appendMessageBox(data.message, "bot");
        }
    });
}

const delay = ms => new Promise(res => setTimeout(res, ms));

const message = `Chào bạn! Tôi là một trợ lý ảo.
Đây là một **tin nhắn mẫu** với _một vài_ định dạng.
Bạn có thể thấy hiệu ứng gõ chữ của tôi.

\`Đây là một đoạn code inline\`

Đây là một khối code:
\`\`\`C#
public static void Main() {
    Console.Writeline("Hello World!");
}
\`\`\`

Cảm ơn bạn đã theo dõi!
`;

writeText(message, document.getElementById("bot-message"))