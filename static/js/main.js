document.addEventListener('DOMContentLoaded', function() {
    // DOM元素
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const toggleVoiceButton = document.getElementById('toggle-voice-input');
    const recordingIndicator = document.getElementById('recording-indicator');
    const stopRecordingButton = document.getElementById('stop-recording');
    const settingsButton = document.querySelector('.settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeModalButton = document.querySelector('.close-modal');
    const saveSettingsButton = document.getElementById('save-settings');
    const emotionDisplay = document.getElementById('current-emotion');

    // 用户信息
    let userInfo = {
        name: '',
        birthday: '',
        interests: '',
        outputPreference: 'auto'
    };

    loadUserInfo();

    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    function sendMessage(message, isVoice = false, userAudioUrl = null) {
        if (!message.trim() && !isVoice) return;

        appendMessage(message, 'sent', userAudioUrl);
        messageInput.value = '';
        scrollToBottom();
        showTypingIndicator();

        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                user_name: userInfo.name,
                preferred_output: userInfo.outputPreference
            })
        })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator();
            appendMessage(data.message, 'received', data.audio_url);
            updateEmotionDisplay(data.emotion);
            scrollToBottom();
        })
        .catch(error => {
            console.error('Error:', error);
            removeTypingIndicator();
            appendMessage('抱歉，我遇到了一些问题，请稍后再试。', 'received');
            scrollToBottom();
        });
    }

    function appendMessage(message, type, audioUrl = null) {
        const messageContainer = document.createElement('div');
        messageContainer.className = 'message-container';

        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = message;

        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = formatTime(new Date());

        messageElement.appendChild(messageContent);
        messageContainer.appendChild(messageElement);
        messageContainer.appendChild(messageTime);

        if (audioUrl) {
            const audioPlayer = document.createElement('audio');
            audioPlayer.className = 'audio-player';
            audioPlayer.controls = true;
            audioPlayer.src = audioUrl;
            audioPlayer.autoplay = true;
            messageContainer.appendChild(audioPlayer);
        }

        chatMessages.appendChild(messageContainer);
    }

    function showTypingIndicator() {
        const typingContainer = document.createElement('div');
        typingContainer.className = 'message-container typing-indicator';

        const typingMessage = document.createElement('div');
        typingMessage.className = 'message received';

        const typingContent = document.createElement('div');
        typingContent.className = 'typing-animation';
        typingContent.innerHTML = '<span></span><span></span><span></span>';

        typingMessage.appendChild(typingContent);
        typingContainer.appendChild(typingMessage);
        chatMessages.appendChild(typingContainer);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) typingIndicator.remove();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function formatTime(date) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    function updateEmotionDisplay(emotion) {
        const emotionEmojis = {
            happy: '😊', excited: '😃', calm: '😌',
            sad: '😔', angry: '😠', flirty: '😘', cute: '🥰'
        };
        const emotionText = {
            happy: '开心', excited: '兴奋', calm: '平静',
            sad: '难过', angry: '生气', flirty: '撩人', cute: '可爱'
        };
        emotionDisplay.textContent = `${emotionText[emotion] || '开心'} ${emotionEmojis[emotion] || '😊'}`;
    }

    function loadUserInfo() {
        fetch('/api/get-memory')
            .then(response => response.json())
            .then(data => {
                if (data.name) userInfo.name = data.name;
                if (data.birthday) userInfo.birthday = data.birthday;
                if (data.interests) userInfo.interests = data.interests;
                if (data.outputPreference) userInfo.outputPreference = data.outputPreference;

                document.getElementById('user-name-input').value = userInfo.name;
                document.getElementById('user-birthday-input').value = userInfo.birthday;
                document.getElementById('user-interests-input').value = userInfo.interests;
                document.getElementById('output-preference').value = userInfo.outputPreference;
            });
    }

    function saveUserInfo() {
        const fields = ['name', 'birthday', 'interests', 'outputPreference'];
        fields.forEach(field => {
            userInfo[field] = document.getElementById(`user-${field}-input`)?.value || userInfo[field];
            fetch('/api/set-memory', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key: field, value: userInfo[field] })
            });
        });
        settingsModal.style.display = 'none';
    }

    function startRecording() {
        isRecording = true;
        audioChunks = [];

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

                mediaRecorder.onstop = () => {
                    const blob = new Blob(audioChunks, { type: 'audio/webm' });
                    const formData = new FormData();
                    formData.append('audio', blob);

                    recordingIndicator.style.display = 'none';

                    fetch('/api/speech-to-text', {
                        method: 'POST',
                        body: formData
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.text) {
                            const userAudioURL = URL.createObjectURL(blob);
                            sendMessage(data.text, true, userAudioURL);
                        }
                    });
                };

                mediaRecorder.start();
                recordingIndicator.style.display = 'flex';
            });
    }

    function stopRecording() {
        if (mediaRecorder && isRecording) {
            mediaRecorder.stop();
            isRecording = false;
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    }

    sendButton.addEventListener('click', () => sendMessage(messageInput.value));
    messageInput.addEventListener('keypress', e => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage(messageInput.value);
        }
    });
    toggleVoiceButton.addEventListener('click', () => !isRecording && startRecording());
    stopRecordingButton.addEventListener('click', stopRecording);
    settingsButton.addEventListener('click', () => settingsModal.style.display = 'flex');
    closeModalButton.addEventListener('click', () => settingsModal.style.display = 'none');
    saveSettingsButton.addEventListener('click', saveUserInfo);
    window.addEventListener('click', e => e.target === settingsModal && (settingsModal.style.display = 'none'));

    scrollToBottom();
});