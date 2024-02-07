// Class definition for Chatbox
class Chatbox {
    // Constructor to initialize properties
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false; // Represents the open/close state of the chatbox
        this.messages = []; // Array to store chat messages
        this.welcomeMessageDisplayed = false; // Flag to track if the welcome message is displayed
    }

    // Method to set up event listeners and handle user interactions
    display() {
        const { openButton, chatBox, sendButton } = this.args;

        // Event listener for opening/closing the chatbox
        openButton.addEventListener('click', () => this.toggleState(chatBox));

        // Event listener for sending messages
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        // Event listener for sending messages when Enter key is pressed
        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
    this.state = !this.state;

    // Show or hide the chatbox based on the state
    if (this.state) {
        chatbox.classList.add('chatbox--active');
        if (!this.welcomeMessageDisplayed) {
            this.displayWelcomeMessage(chatbox);
            this.welcomeMessageDisplayed = true;
        }
       } else {
        chatbox.classList.remove('chatbox--active');
        }
    }

 // Method to display the welcome message
    displayWelcomeMessage(chatbox) {
        // Construct welcome message
        let welcomeMsg = {
            name: "Kamini",
            message: "Hi there! 👋 I’m your chat support virtual assistant. How can I help you today? <br><br> You can say things like: <br> <b>- How to use moodle?<br> - How to download lockdown browser? <br> - How to submit my assignment? <br>- How to find my teachers email? <br> - How to find my grades? </b>"
        };

        // Add welcome message to the messages array
        this.messages.push(welcomeMsg);

        // Update the chatbox with the new messages
        this.updateChatText(chatbox);
    }


    // Method to handle sending messages
  onSendButton(chatbox) {
    var textField = chatbox.querySelector('input');
    let text1 = textField.value;

    if (text1 === "") {
        return;
    }

    // Construct user message
    let msg1 = { name: "User", message: text1 };
    this.messages.push(msg1);

    // Simulate typing animation
    this.updateChatText(chatbox);

    // Delay before sending user message to the server
    setTimeout(() => {
        // Send user message to the server for prediction
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            // Process server response and construct Kamini's message
            let msg2 = { name: "Kamini", message: r.answer };
            this.messages.push(msg2);

            // Update the chatbox with the new messages
            this.updateChatText(chatbox);
            textField.value = '';
        }).catch((error) => {
            // Handle errors from the server
            console.error('Error:', error);

            // Update the chatbox with the new messages
            this.updateChatText(chatbox);
            textField.value = '';
        });
    }, 10); // Adjust the delay time (in milliseconds) as needed
    }


 updateChatText(chatbox) {
    var html = '';
    // Reverse the order of messages and construct HTML
    this.messages.slice().reverse().forEach(function (item, index) {
        if (item.name === "Kamini") {
            // Check if the message contains an image placeholder
            const imageRegex = /\[image\]\(([^)]+)\)/; // Matches [image](imageUrl)
            const imageMatch = item.message.match(imageRegex);

            // Check if the message contains a link placeholder
            const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/; // Matches [text](link)
            const linkMatch = item.message.match(linkRegex);

            // Get the message text without markdown syntax
            let messageText = item.message.replace(linkRegex, '').replace(imageRegex, '');

            // Construct HTML for the message
            let messageHtml = '<div class="messages__item messages__item--visitor">';
            messageHtml += messageText; // Add the message text without markdown syntax

            if (imageMatch) {
                // If an image is present, add the image HTML
                const imageUrl = imageMatch[1];
                messageHtml += `<br><img src="${imageUrl}" class="chatbox__image" alt="Image" style="width: 180px; height: 180px;" onclick="openImagePopup('${imageUrl}')"/>`;
            }

            if (linkMatch) {
                // If a link is present, add the link HTML
                const linkText = linkMatch[1];
                const linkUrl = linkMatch[2];
                // Check if the link text already exists in the message
                if (!messageText.includes(linkText)) {
                    messageHtml += `<br><a href="${linkUrl}" target="_blank">${linkText}</a>`;
                }
            }

            messageHtml += '</div>'; // Close the message container
            html += messageHtml; // Add the message HTML to the overall HTML
        }
        else {
            // Handle messages from the operator (if needed)
            html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
        }
    });

    // Update the chatbox messages container with the new HTML
    const chatmessage = chatbox.querySelector('.chatbox__messages');
    chatmessage.innerHTML = html;
}


 }

   // Function to open the image popup
function openImagePopup(imageUrl) {
    var popup = document.getElementById('imagePopup');
    var popupImage = document.getElementById('popupImage');

    popupImage.src = imageUrl;
    popup.style.display = 'flex'; // Display the popup
}

// Function to close the image popup
function closeImagePopup() {
    var popup = document.getElementById('imagePopup');
    popup.style.display = 'none'; // Hide the popup
}


// Create an instance of the Chatbox class and display the chatbox
const chatbox = new Chatbox();
chatbox.display();