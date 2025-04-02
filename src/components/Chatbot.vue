<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div id="chatbot">
    <b-button size="lg" variant="warning" @click="toggleChat" class="mb-2 chat-toggle-button"
              :class="{ 'chat-open': isChatOpen }">
      <b-icon icon="question-circle-fill" aria-label="Help"/>
    </b-button>
    <div v-if="isChatOpen" id="chat-window">
      <div id="chat-body">
        <div v-for="message in messages" :key="message.id" :class="['message-box', message.type]">
          <div v-if="message.type === 'user'" class="message">{{ message.text }}</div>
          <div v-if="message.type === 'bot'" class="message" v-html="message.text"></div>

          <b-button @click="copyToClipboard(message.text)" class="copy-button"
                    :class="message.type === 'user' ? 'user-copy' : 'bot-copy'">
            <font-awesome-icon icon="copy"/>
          </b-button>
        </div>
      </div>

      <div id="chat-input-container">
        <textarea v-model="userInput" @keyup.enter="sendMessage" placeholder="Ask me anything!" class="chat-input"/>

        <div class="button-container">
          <b-button variant="warning" @click="startNewChat" class="icon-button new-chat-button">
            <b-icon icon="pencil-square"/>
          </b-button>
          <b-button variant="warning" @click="sendMessage" class="icon-button send-message-button">
            <font-awesome-icon :icon="isSending ? 'spinner' : 'paper-plane'" :spin="isSending"/>
          </b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {BButton, BIcon} from 'bootstrap-vue-next'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

export default {
  components: {
    BButton,
    BIcon,
    FontAwesomeIcon
  },
  data() {
    return {
      isChatOpen: true,
      userInput: '',
      isSending: false,
      initialMessage: {
        id: 1,
        text: 'Hello! How can I assist you today?',
        type: 'bot'
      },
      messages: [
        {
          id: 1,
          text: 'Hello! How can I assist you today?',
          type: 'bot'
        }
      ]
    }
  },
  methods: {
    toggleChat() {
      this.isChatOpen = !this.isChatOpen
    },
    startNewChat() {
      this.messages = [this.initialMessage]
      this.userInput = ''
    },
    async sendMessage() {
      if (this.userInput.trim()) {
        const userMessage = {id: Date.now(), text: this.userInput, type: 'user'}
        this.messages.push(userMessage)
        this.isSending = true

        try {
          const botResponse = await this.sendToBackend(this.userInput)
          this.messages.push({
            id: Date.now() + 1,
            text: botResponse,
            type: 'bot'
          })
        } catch (error) {
          console.error('There was a problem with the fetch operation:', error)
          this.messages.push({
            id: Date.now() + 1,
            text: 'Sorry, there was an error.',
            type: 'bot'
          })
        } finally {
          this.isSending = false
          this.userInput = ''
        }
      }
    },
    async sendToBackend(message) {
      try {
        const response = await fetch('http://localhost:5000/api/chat/send', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({message})
        })

        if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.statusText}`)
        }

        const data = await response.json()
        return data.response
      } catch (error) {
        console.error('Fetch error:', error)
        return 'Sorry, there was an error.'
      }
    },
    copyToClipboard(text) {
      navigator.clipboard.writeText(text).catch(err => {
        console.error('Failed to copy:', err)
      })
    }
  }
}
</script>

<style scoped>
#chatbot {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.chat-toggle-button {
  position: relative;
  width: 30px;
  height: 30px;
  padding: 0;
  background: none;
  border: none;
  cursor: pointer;
  outline: none;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7c7c7d;
}

.chat-toggle-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(250, 181, 21, 0);
  z-index: -1;
  transition: background-color 0.3s ease;
  border-radius: 4px;
}

.chat-toggle-button:hover::before {
  background-color: rgba(250, 181, 21, 1);
}

.chat-toggle-button.chat-open::before {
  background-color: rgba(250, 181, 21, 1);
}

.icon {
  color: #7c7c7d;
  font-size: 20px;
}

#chat-window {
  width: 360px;
  height: 500px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: white;
  display: flex;
  flex-direction: column;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

#chat-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  scrollbar-width: auto;
  scrollbar-color: #a0a0a0 #ffffff;
}

#chat-body::-webkit-scrollbar {
  width: 8px;
}

#chat-body::-webkit-scrollbar-track {
  background: #ffffff;
}

#chat-body::-webkit-scrollbar-thumb {
  background-color: #fab515;
  border-radius: 10px;
}

#chat-input-container {
  padding: 10px;
  border-top: 1px solid #ddd;
  display: flex;
  align-items: center;
}

.chat-input {
  min-width: 200px;
  max-width: 280px;
  width: 280px;
  height: 80px;
  padding: 6px;
  border: 1px solid #a0a0a0;
  border-radius: 5px;
  font-family: 'Ubuntu', sans-serif;
  font-size: 14px;
  color: #2a2a2a;
  line-height: 1.5;
  resize: none;
  outline: none;
}

.chat-input:focus {
  border-color: rgba(0, 123, 255, 0.35);
  border-width: 3px;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.icon-button {
  background-color: rgb(212, 212, 212);
  color: rgb(63, 63, 63);
  border: none;
  border-radius: 4px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 1;
  padding: 5px;
  margin: 8px;
}

.copy-button {
  margin-top: 5px;
  cursor: pointer;
  font-size: 15px;
  color: rgb(163, 163, 163);
  background: none;
  background-image: none;
  background-color: transparent;
  border: none;
  box-shadow: none;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-box {
  display: flex;
  flex-direction: column;
  margin: 5px 10px;
  animation: fadeIn 0.5s ease;
}

.user {
  align-items: flex-start;
  margin-left: 5px;
}

.user .message {
  background-color: #e7e7e7;
  color: #2a2a2a;
  font-family: 'Ubuntu', sans-serif;
  font-size: 14px;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  max-width: 280px;
  word-wrap: break-word;
}

.bot {
  align-items: flex-end;
  margin-right: 5px;
}

.bot .message {
  background-color: #fab515;
  color: #2a2a2a;
  font-family: 'Ubuntu', sans-serif;
  font-size: 14px;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  max-width: 280px;
  word-wrap: break-word;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>