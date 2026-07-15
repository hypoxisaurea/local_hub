<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUIStore } from '@/stores/uiStore'

const ui = useUIStore()
const { locale, t } = useI18n()
const draft = ref('')
const messagesRef = ref<HTMLElement | null>(null)

const quickPrompts = computed(() => [
  t('chat.prompts.0'),
  t('chat.prompts.1'),
  t('chat.prompts.2'),
  t('chat.prompts.3'),
])

const isOpen = computed(() => ui.showChat)

const scrollToBottom = async () => {
  await nextTick()
  messagesRef.value?.scrollTo({
    top: messagesRef.value.scrollHeight,
    behavior: 'smooth'
  })
}

const formatTime = (value: string) => {
  return new Intl.DateTimeFormat(locale.value === 'ko' ? 'ko-KR' : 'en-US', {
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(value))
}

const sendMessage = async (message = draft.value) => {
  const content = message.trim()

  if (!content) {
    return
  }

  draft.value = ''
  await ui.sendChatMessage(content)
  await scrollToBottom()
}

watch(
  () => ui.chatMessages.length,
  () => {
    scrollToBottom()
  }
)

watch(isOpen, async (open) => {
  document.body.classList.toggle('chat-panel-open', open)

  if (open) {
    await scrollToBottom()
  }
})

onBeforeUnmount(() => {
  document.body.classList.remove('chat-panel-open')
})
</script>

<template>
  <Transition name="chat-panel">
    <section v-show="ui.showChat" class="chat-panel" aria-label="LocalHub Chatbot">
      <header class="chat-panel__header">
        <div class="chat-panel__identity">
          <div>
            <h2>해치 HAECHI</h2>
          </div>
        </div>

        <div class="chat-panel__actions">
          <button type="button" :aria-label="t('chat.reset')" :title="t('chat.reset')" @click="ui.clearChatHistory()">
            <i class="fas fa-rotate-right" aria-hidden="true"></i>
          </button>
          <button type="button" :aria-label="t('chat.close')" :title="t('common.close')" @click="ui.closeChat()">
            <i class="fas fa-xmark" aria-hidden="true"></i>
          </button>
        </div>
      </header>

      <div ref="messagesRef" class="chat-panel__messages">
        <article
          v-for="message in ui.chatMessages"
          :key="message.id"
          class="chat-panel__message-row"
          :class="`chat-panel__message-row--${message.role}`"
        >
          <img
            v-if="message.role === 'assistant'"
            src="/assets/floating_button.png"
            alt=""
            class="chat-panel__message-avatar"
          >
          <div class="chat-panel__bubble-wrap">
            <div class="chat-panel__bubble">{{ message.content }}</div>
            <time :datetime="message.createdAt">{{ formatTime(message.createdAt) }}</time>
          </div>
        </article>

        <article v-if="ui.isTyping" class="chat-panel__message-row chat-panel__message-row--assistant">
          <img src="/assets/floating_button.png" alt="" class="chat-panel__message-avatar">
          <div class="chat-panel__bubble chat-panel__bubble--typing" :aria-label="t('chat.typing')">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </article>
      </div>

      <div class="chat-panel__quick-prompts" :aria-label="t('chat.quickLabel')">
        <button
          v-for="prompt in quickPrompts"
          :key="prompt"
          type="button"
          @click="sendMessage(prompt)"
        >
          {{ prompt }}
        </button>
      </div>

      <form class="chat-panel__composer" @submit.prevent="sendMessage()">
        <input
          v-model="draft"
          type="text"
          :placeholder="t('chat.placeholder')"
          autocomplete="off"
          :disabled="ui.isTyping"
        >
        <button type="submit" :aria-label="t('chat.send')" :disabled="!draft.trim() || ui.isTyping">
          <i class="fas fa-paper-plane" aria-hidden="true"></i>
        </button>
      </form>

      <p class="chat-panel__hint">
        <i class="fas fa-lock" aria-hidden="true"></i>
        {{ t('chat.hint') }}
      </p>
    </section>
  </Transition>
</template>

<style scoped>
.chat-panel {
  position: fixed;
  right: 32px;
  bottom: 32px;
  z-index: 70;
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto auto auto;
  width: min(340px, calc(100vw - 32px));
  height: min(600px, calc(100vh - 64px));
  overflow: hidden;
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid rgba(251, 113, 133, 0.24);
  border-radius: 18px;
  box-shadow: 0 26px 80px rgba(148, 68, 92, 0.2);
  backdrop-filter: blur(18px);
}

.chat-panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  min-height: 70px;
  padding: 14px 18px;
  border-bottom: 1px solid rgba(251, 113, 133, 0.18);
  background: linear-gradient(180deg, #fff7fa 0%, rgba(255, 247, 250, 0.72) 100%);
}

.chat-panel__identity {
  display: flex;
  align-items: center;
  min-width: 0;
  gap: 12px;
}

.chat-panel__avatar,
.chat-panel__message-avatar {
  flex: 0 0 auto;
  width: 42px;
  height: 42px;
  object-fit: cover;
  border-radius: 50%;
  background: #ffe4ef;
  box-shadow: 0 0 0 3px #fff;
}

.chat-panel__identity h2 {
  margin: 0;
  color: #263238;
  font-size: 16px;
  font-weight: 800;
  line-height: 1.2;
}

.chat-panel__identity p {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 4px 0 0;
  color: #475569;
  font-size: 12px;
  font-weight: 600;
}

.chat-panel__identity p span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22c55e;
}

.chat-panel__actions {
  display: flex;
  gap: 8px;
}

.chat-panel__actions button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border: 0;
  border-radius: 50%;
  color: #334155;
  background: transparent;
  cursor: pointer;
  transition: background 160ms ease, color 160ms ease;
}

.chat-panel__actions button:hover {
  color: #be185d;
  background: rgba(244, 114, 182, 0.14);
}

.chat-panel__messages {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 0;
  padding: 18px;
  overflow-y: auto;
  background:
    radial-gradient(circle at 10% 12%, rgba(252, 231, 243, 0.62), transparent 26%),
    linear-gradient(180deg, #fff 0%, #fff9fb 100%);
}

.chat-panel__message-row {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.chat-panel__message-row--user {
  justify-content: flex-end;
}

.chat-panel__bubble-wrap {
  display: flex;
  flex-direction: column;
  max-width: min(78%, 330px);
}

.chat-panel__message-row--user .chat-panel__bubble-wrap {
  align-items: flex-end;
}

.chat-panel__bubble {
  width: fit-content;
  max-width: 100%;
  padding: 12px 14px;
  color: #334155;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.5;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  background: #f1f5f9;
  border-radius: 16px 16px 16px 5px;
}

.chat-panel__message-row--user .chat-panel__bubble {
  color: #7f1d45;
  background: #ffe4ef;
  border-radius: 16px 16px 5px 16px;
}

.chat-panel__bubble-wrap time {
  margin-top: 4px;
  color: #94a3b8;
  font-size: 10px;
  font-weight: 700;
}

.chat-panel__bubble--typing {
  display: flex;
  width: 62px;
  gap: 5px;
}

.chat-panel__bubble--typing span {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #fb7185;
  animation: typing-dot 900ms infinite ease-in-out;
}

.chat-panel__bubble--typing span:nth-child(2) {
  animation-delay: 120ms;
}

.chat-panel__bubble--typing span:nth-child(3) {
  animation-delay: 240ms;
}

.chat-panel__quick-prompts {
  display: flex;
  gap: 8px;
  padding: 12px 16px 8px;
  overflow-x: auto;
  border-top: 1px solid rgba(251, 113, 133, 0.12);
}

.chat-panel__quick-prompts button {
  flex: 0 0 auto;
  min-height: 34px;
  padding: 0 14px;
  border: 1px solid rgba(251, 113, 133, 0.22);
  border-radius: 999px;
  color: #ec4899;
  background: #fff7fa;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
}

.chat-panel__composer {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 16px;
  padding: 8px 8px 8px 16px;
  border: 1px solid rgba(251, 113, 133, 0.18);
  border-radius: 999px;
  background: #fff;
  box-shadow: 0 8px 26px rgba(148, 68, 92, 0.08);
}

.chat-panel__composer input {
  flex: 1;
  min-width: 0;
  height: 34px;
  border: 0;
  color: #334155;
  background: transparent;
  font-size: 13px;
  outline: none;
}

.chat-panel__composer input::placeholder {
  color: #94a3b8;
}

.chat-panel__composer button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border: 0;
  border-radius: 50%;
  color: #fff;
  background: #f4518d;
  cursor: pointer;
  transition: transform 160ms ease, opacity 160ms ease;
}

.chat-panel__composer button:hover {
  transform: translateY(-1px);
}

.chat-panel__composer button:disabled {
  cursor: not-allowed;
  opacity: 0.48;
  transform: none;
}

.chat-panel__hint {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0;
  padding: 8px 18px 14px;
  color: #94a3b8;
  font-size: 11px;
  font-weight: 600;
}

.chat-panel-enter-active,
.chat-panel-leave-active {
  transition: opacity 180ms ease, transform 180ms ease;
}

.chat-panel-enter-from,
.chat-panel-leave-to {
  opacity: 0;
  transform: translateY(18px) scale(0.98);
}

@keyframes typing-dot {
  0%,
  80%,
  100% {
    transform: translateY(0);
    opacity: 0.45;
  }

  40% {
    transform: translateY(-4px);
    opacity: 1;
  }
}

@media (max-width: 640px) {
  .chat-panel {
    inset: 0;
    width: 100vw;
    height: 100dvh;
    border: 0;
    border-radius: 0;
  }

  .chat-panel__header {
    min-height: 66px;
    padding: max(12px, env(safe-area-inset-top)) 16px 12px;
  }

  .chat-panel__messages {
    padding: 16px 14px;
  }

  .chat-panel__bubble-wrap {
    max-width: 82%;
  }

  .chat-panel__quick-prompts {
    padding-inline: 14px;
  }

  .chat-panel__composer {
    margin-inline: 14px;
  }

  .chat-panel__hint {
    padding-bottom: max(12px, env(safe-area-inset-bottom));
  }
}
</style>
