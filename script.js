function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    appendMessage('user', userInput);

    fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `user_input=${encodeURIComponent(userInput)}`
    })
    .then(response => response.json())
    .then(data => {
        const botReply = data.answer;
        appendMessage('bot', botReply);
    })
    .catch(error => console.error('Error:', error));

    document.getElementById('user-input').value = '';
}

function appendMessage(sender, text) {
    const chatLog = document.getElementById('chat-log');
    const messageElement = document.createElement('div');
    messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    messageElement.textContent = text;
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight;
}
