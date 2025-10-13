const submit = document.getElementById('submit');
const chatbox = document.getElementById('chat-box');
const chat_list = document.getElementById('chat-list');
const new_chat = document.getElementById('new-chat');
const log_out = document.getElementById("logout");


const user = JSON.parse(localStorage.getItem("user"));

let uuid = "make new";

let current_chat_id = uuid;

chatbox.innerHTML = "";
const h1 = document.createElement("h1");
h1.textContent = "Hi there! How can I assist you today?";
h1.style.textAlign = "center";
chatbox.appendChild(h1);

new_chat.addEventListener('click', function () {
            current_chat_id = uuid;
            chatbox.innerHTML = "";
            const h1 = document.createElement("h1");
            h1.textContent = "Hi there! How can I assist you today?";
            h1.style.textAlign = "center";
            chatbox.appendChild(h1);
        });

const getAllChatFromUserID = async (id_user) => {
    const response = await fetch(`http://localhost:8000/c/u/${id_user}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: "include"
    });

    const data = await response.json();
    console.log(data)

    const id_chat_list = data.map(chat => `<li class="chat-item">${chat.id}</li>`).join('');
    chat_list.innerHTML = id_chat_list;

    const chat_items = document.querySelectorAll('.chat-item');
    chat_items.forEach(item => {
        item.addEventListener('click', function () {
            chatbox.innerHTML = '';
            current_chat_id = this.textContent; 
            getConversationFromChatID(current_chat_id);
        });
    });
};

const getConversationFromChatID = async (id_chat) => {
    const response = await fetch(`http://localhost:8000/c/${id_chat}`,
        {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: "include"
    }
    );
    const data = await response.json();
    const mes = data.conversation
    const messages = mes.map(msg =>
        `<div class="${msg.type === 'human' ? 'user-message' : 'bot-message'}">${msg.content}</div>`
    ).join('');
    chatbox.innerHTML = messages;
};

const getResponse = async (id_chat, message) => {
    const body = { message: message };
    const response = await fetch(`http://localhost:8000/c/${id_chat}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        credentials: "include"
    });
    const data = await response.json();
    return data;
};

if (submit) {
    submit.addEventListener('click', async function () {
        if (current_chat_id === uuid) {
            chatbox.innerHTML = "";
        }
        const messageInput = document.getElementById('user-input');
        const message = messageInput.value;
        if (!message || !current_chat_id) return;
        submit.disabled = true;
        messageInput.disabled = true;
        const userMessage = `<div class="user-message">${message}</div>`;
        chatbox.innerHTML += userMessage;
        messageInput.value = '';

        const data = await getResponse(current_chat_id, message);
        if (current_chat_id === uuid) {
            current_chat_id = data.chat_id;
            getAllChatFromUserID(user.id);
        }
        const botMessage = `<div class="bot-message">${data.response}</div>`;
        chatbox.innerHTML += botMessage;
        submit.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    });
}

getAllChatFromUserID(user.id);

log_out.addEventListener('click', async function () {
    await fetch("http://localhost:8000/auth/logout", {
        method: 'POST',
        credentials: "include"
    })
    window.location.href = "./login.html";
});

