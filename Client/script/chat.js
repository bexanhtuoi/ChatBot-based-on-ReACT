const submit = document.getElementById('submit');
const chatbox = document.getElementById('chat-box');
const chat_list = document.getElementById('chat-list');
const chat_item = document.getElementsByClassName('chat-item');

const user = JSON.parse(localStorage.getItem("user"));

const getConversationFromChatID = async (id_chat) => {
    const response = await fetch(`http://localhost:8000/chats/${id_chat}`);
    const data = await response.json();
    const messages = data.map(msg => `<div class="${msg.conversation.type === 'human' ? 'user-message' : 'bot-message'}">${msg.content}</div>`).join('');
    chatbox.innerHTML = messages;
}

const getAllChatFromUserID = async (id_user) => {
    const response = await fetch(`http://localhost:8000/chats/u/${id_user}`);
    const data = await response.json();
    const id_chat = data.map(chat => `<li class="chat-item">${chat.id}</li>`).join('');
    chat_list.innerHTML = id_chat;
}

getAllChatFromUserID(user.id);

const getResponse = async (id_chat, message) => {
    const body = {id_chat: id_chat, message: message};
    const response = await fetch('http://localhost:8000/chats', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await response.json();
    return data.response;
}

if (chat_item) {
    chat_item.addEventListener('click', function() {
    chatbox.innerHTML = '';
    const id_chat = this.textContent;
    getConversationFromChatID(id_chat);
    });
}

if (submit) {
    submit.addEventListener('click', async function() {
        const message = document.getElementById('user-input').value;
        if (!message) return;
        const id_chat = chat_item.textContent;
        const userMessage = `<div class="user-message">${message}</div>`;
        chatbox.innerHTML += userMessage;
        document.getElementById('user-input').value = '';
        const botResponse = await getResponse(id_chat, message);
        const botMessage = `<div class="bot-message">${botResponse}</div>`;
        chatbox.innerHTML += botMessage;
    });
}