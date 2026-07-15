import { defineStore } from 'pinia'
import { ref } from 'vue'
import { i18n, setLocale } from '@/i18n'

export type ViewType = 'portal' | 'explorer' | 'saved' | 'post-detail'
export type ChatRole = 'user' | 'assistant'

export interface ChatMessage {
  id: number
  role: ChatRole
  content: string
  createdAt: string
}

const CHAT_HISTORY_KEY = 'localhub_chat_history'
const CHAT_LANGUAGE_KEY = 'localhub_chat_language'

const loadChatLanguage = (): 'ko' | 'en' => {
  const savedLanguage = sessionStorage.getItem(CHAT_LANGUAGE_KEY)
  return savedLanguage === 'en' ? 'en' : 'ko'
}

const detectRequestedLanguage = (message: string): 'ko' | 'en' | null => {
  const normalizedMessage = message.toLowerCase()

  if (
    normalizedMessage.includes('영어로') ||
    normalizedMessage.includes('영어 모드') ||
    normalizedMessage.includes('english') ||
    normalizedMessage.includes('speak english')
  ) {
    return 'en'
  }

  if (
    normalizedMessage.includes('한국어로') ||
    normalizedMessage.includes('한국어 모드') ||
    normalizedMessage.includes('korean') ||
    normalizedMessage.includes('speak korean')
  ) {
    return 'ko'
  }

  return null
}

const createWelcomeMessage = (): ChatMessage => ({
  id: 1,
  role: 'assistant',
  content: i18n.global.t('chat.welcome'),
  createdAt: new Date().toISOString()
})

const loadChatHistory = (): ChatMessage[] => {
  try {
    const savedHistory = sessionStorage.getItem(CHAT_HISTORY_KEY)

    if (savedHistory) {
      return JSON.parse(savedHistory) as ChatMessage[]
    }
  } catch {
    sessionStorage.removeItem(CHAT_HISTORY_KEY)
  }

  return [createWelcomeMessage()]
}

export const useUIStore = defineStore('ui', () => {
  const currentView = ref<ViewType>('portal')
  const showWriteModal = ref(false)
  const showAuthModal = ref(false)
  const showChat = ref(false)
  const currentLang = ref<'ko' | 'en'>(loadChatLanguage())
  setLocale(currentLang.value)
  const toastMessage = ref('')
  const isTyping = ref(false)
  const chatMessages = ref<ChatMessage[]>(loadChatHistory())

  const saveChatHistory = () => {
    sessionStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(chatMessages.value))
  }

  const setChatLanguage = (language: 'ko' | 'en') => {
    currentLang.value = language
    setLocale(language)
    sessionStorage.setItem(CHAT_LANGUAGE_KEY, language)
  }

  const setView = (view: ViewType) => {
    currentView.value = view
  }

  const showToast = (msg: string, duration = 2500) => {
    toastMessage.value = msg
    setTimeout(() => {
      toastMessage.value = ''
    }, duration)
  }

  const toggleLang = () => {
    setChatLanguage(currentLang.value === 'ko' ? 'en' : 'ko')
    showToast(i18n.global.t(currentLang.value === 'ko' ? 'toast.switchedKo' : 'toast.switchedEn'))
  }

  const openWriteModal = () => {
    showWriteModal.value = true
  }

  const closeWriteModal = () => {
    showWriteModal.value = false
  }

  const openAuthModal = () => {
    showAuthModal.value = true
  }

  const closeAuthModal = () => {
    showAuthModal.value = false
  }

  const toggleChat = () => {
    showChat.value = !showChat.value
  }

  const openChat = () => {
    showChat.value = true
  }

  const closeChat = () => {
    showChat.value = false
  }

  const addChatMessage = (role: ChatRole, content: string) => {
    chatMessages.value.push({
      id: Date.now() + chatMessages.value.length,
      role,
      content,
      createdAt: new Date().toISOString()
    })
    saveChatHistory()
  }

  const sendChatMessage = async (content: string) => {
    const message = content.trim()

    if (!message || isTyping.value) {
      return
    }

    const requestedLanguage = detectRequestedLanguage(message)
    if (requestedLanguage) {
      setChatLanguage(requestedLanguage)
    }

    addChatMessage('user', message)
    isTyping.value = true

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message,
          history: chatMessages.value
            .slice(0, -1)
            .map(chatMessage => ({
              role: chatMessage.role,
              content: chatMessage.content
            })),
          language: requestedLanguage || currentLang.value
        })
      })

      if (!response.ok) {
        throw new Error('Chat request failed')
      }

      const data = await response.json() as { answer?: string }
      addChatMessage('assistant', data.answer || i18n.global.t('chat.fallback'))
    } catch {
      addChatMessage('assistant', i18n.global.t('chat.offline'))
    } finally {
      isTyping.value = false
    }
  }

  const clearChatHistory = () => {
    chatMessages.value = [createWelcomeMessage()]
    saveChatHistory()
  }

  return {
    currentView,
    showWriteModal,
    showAuthModal,
    showChat,
    currentLang,
    toastMessage,
    isTyping,
    chatMessages,
    setView,
    showToast,
    toggleLang,
    setChatLanguage,
    openWriteModal,
    closeWriteModal,
    openAuthModal,
    closeAuthModal,
    toggleChat,
    openChat,
    closeChat,
    sendChatMessage,
    clearChatHistory
  }
})
