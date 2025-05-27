document.addEventListener("DOMContentLoaded", () => {
    const chatSocket = new WebSocket(
        "ws://" + window.location.host + "/ws/chat/" + chat_id + "/"
    );

    const messages = document.querySelector('.chat-messages');
    const messageInput = document.querySelector('#message');
    const chatForm = document.querySelector('#chat-form');

    function addMessageToChat(data) {
        const messageElement = document.createElement('p');
        messageElement.classList.add('message');
        messageElement.classList.add(data.sender_id == user_id ? 'sent' : 'received');
        messageElement.textContent = data.message;
        messages.appendChild(messageElement);
        messages.scrollTop = messages.scrollHeight; // Scroll to the bottom
    }

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        addMessageToChat(data);
    };

    chatSocket.onopen = function() {
        console.log('WebSocket connected');
    };

    chatSocket.onclose = function(e) {
        console.error('WebSocket zamknięty.');
    };

    chatForm.onsubmit = function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            chatSocket.send(JSON.stringify({
                'message': message,
                'sender_id': user_id
            }));
            messageInput.value = '';
        }
    };
});