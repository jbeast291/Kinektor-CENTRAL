function sendMessage(){
    var msg = document.getElementById("MessageBox");
    console.log(msg.value);

    fetch('/api/webMessageIn/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: getCookie("token"),
            msg: msg.value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Response:', data);

        })
        .catch(error => {
            console.error('Request failed:', error);
        });
    msg.value = '';
}

document.getElementById('MessageBox').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        console.log('Enter key was pressed!');
        sendMessage();
    }
});

function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();

        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }

    return null;
}


function addMessage(platform, username, imageUrl, message) {
    const textMessageContainer = document.createElement('div');
    textMessageContainer.classList.add('TextMessageContianer');

    const userInfoContainer = document.createElement('div');
    userInfoContainer.classList.add('UserInfoContainer');

    const profilePic = document.createElement('div');
    profilePic.classList.add('profilePic');
    profilePic.style.backgroundImage = `url(${imageUrl})`;

    const usernameDiv = document.createElement('div');
    usernameDiv.classList.add('Username');
    usernameDiv.textContent = "[" + platform + "] " + username;

    userInfoContainer.appendChild(profilePic);
    userInfoContainer.appendChild(usernameDiv);

    const textMessageDiv = document.createElement('div');
    textMessageDiv.classList.add('TextMessage');
    textMessageDiv.textContent = message;

    textMessageContainer.appendChild(userInfoContainer);

    textMessageContainer.appendChild(textMessageDiv);
    const mainTextArea = document.getElementById('mainTextArea');

    mainTextArea.insertBefore(textMessageContainer, mainTextArea.firstChild);
}

const socket = io('http://localhost:80');

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
});

socket.on('message_response', (data) => {
    console.log('Received:', data.message);
});

// Listen for broadcast
socket.on('broadcast_message', function(data) {
    console.log('Received message:', data);
    addMessage(data["platform"], data["username"], "/resources/images/logo.png", data["message"]);
});

// Send message to server
socket.emit('message', 'Hello, server!');