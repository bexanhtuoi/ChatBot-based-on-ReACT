const submit = document.getElementById('submit');
const chatbox = document.getElementById('chat-box');
const chat_list = document.getElementById('chat-list');
const new_chat = document.getElementById('new-chat');
const log_out = document.getElementById("logout");


const user = JSON.parse(localStorage.getItem("user"));
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

let uuid = generateUUID();

let current_chat_id = uuid;

new_chat.addEventListener('click', function () {
            current_chat_id = generateUUID();
            chatbox.innerHTML = "";
        });

const getAllChatFromUserID = async (id_user) => {
    const response = await fetch(`http://localhost:8000/chats/u/${id_user}`, {
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
    const response = await fetch(`http://localhost:8000/chats/${id_chat}`,
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
    const body = { id_chat: id_chat, message: message };
    const response = await fetch('http://localhost:8000/chats', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        credentials: "include"
    });
    const data = await response.json();
    return data.response;
};

if (submit) {
    submit.addEventListener('click', async function () {
        const message = document.getElementById('user-input').value;
        if (!message || !current_chat_id) return;
        console.log(current_chat_id)
        const userMessage = `<div class="user-message">${message}</div>`;
        chatbox.innerHTML += userMessage;
        document.getElementById('user-input').value = '';

        const botResponse = await getResponse(current_chat_id, message);
        const botMessage = `<div class="bot-message">${botResponse}</div>`;
        chatbox.innerHTML += botMessage;
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

