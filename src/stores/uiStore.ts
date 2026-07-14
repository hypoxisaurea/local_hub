import { defineStore } from 'pinia'
import { ref } from 'vue'

export type ViewType = 'portal' | 'explorer' | 'saved' | 'post-detail'

export const useUIStore = defineStore('ui', () => {
  const currentView = ref<ViewType>('portal')
  const showWriteModal = ref(false)
  const showAuthModal = ref(false)
  const showChat = ref(false)
  const currentLang = ref<'ko' | 'en'>('ko')
  const toastMessage = ref('')
  const isTyping = ref(false)

  // 뷰 전환
  const setView = (view: ViewType) => {
    currentView.value = view
  }

  // 토스트 메시지 표시
  const showToast = (msg: string, duration = 2500) => {
    toastMessage.value = msg
    setTimeout(() => {
      toastMessage.value = ''
    }, duration)
  }

  // 언어 전환
  const toggleLang = () => {
    currentLang.value = currentLang.value === 'ko' ? 'en' : 'ko'
    showToast(currentLang.value === 'ko' ? '한국어로 변경되었습니다.' : 'Switched to English.')
  }

  // 쓰기 모달 열기
  const openWriteModal = () => {
    showWriteModal.value = true
  }

  // 쓰기 모달 닫기
  const closeWriteModal = () => {
    showWriteModal.value = false
  }

  // 인증 모달 열기
  const openAuthModal = () => {
    showAuthModal.value = true
  }

  // 인증 모달 닫기
  const closeAuthModal = () => {
    showAuthModal.value = false
  }

  // 채팅 토글
  const toggleChat = () => {
    showChat.value = !showChat.value
  }

  return {
    currentView,
    showWriteModal,
    showAuthModal,
    showChat,
    currentLang,
    toastMessage,
    isTyping,
    setView,
    showToast,
    toggleLang,
    openWriteModal,
    closeWriteModal,
    openAuthModal,
    closeAuthModal,
    toggleChat
  }
})