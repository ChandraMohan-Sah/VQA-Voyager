
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
let isUserTurn = true;  // Variable to alternate between user and bot

// Function to create message rows
function createMessageRow(text, isUser) {
  const row = document.createElement('div');
  row.classList.add('message-row');

  const message = document.createElement('div');
  message.classList.add('message', isUser ? 'user' : 'bot');
  message.textContent = text;

  const avatar = document.createElement('img');
  avatar.src = isUser
    ? 'https://via.placeholder.com/40/4CAF50/ffffff?text=U'
    : 'https://via.placeholder.com/40/f1f1f1/000000?text=B';
  avatar.classList.add('message-avatar');

  if (isUser) {
    // User message: avatar goes on the right side
    row.appendChild(message);
    row.appendChild(avatar);
  } else {
    // Bot message: avatar goes on the left side
    row.appendChild(avatar);
    row.appendChild(message);
  }

  chatMessages.appendChild(row);
  chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
}

// Function to send a message and simulate a bot response
function sendMessage() {
  const messageText = messageInput.value.trim();

  if (messageText !== '') {
    createMessageRow(messageText, true); // User message

    messageInput.value = '';

    // Simulate bot response after 1 second
    setTimeout(() => {
      createMessageRow(`Bot: I received your message: "${messageText}"`, false); // Bot response
    }, 1000);
  }
}

// Preload some messages to showcase conversation
function preloadMessages() {
  createMessageRow("Hello!", true); // User message
  createMessageRow("Hi, how can I assist you?", false); // Bot message
  createMessageRow("I need help with my order.", true); // User message
  createMessageRow("Sure! What seems to be the problem?", false); // Bot message
}

// Alternating user and bot messages for preloaded messages
preloadMessages();