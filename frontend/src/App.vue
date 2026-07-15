<script setup lang="ts">
import { watchEffect } from 'vue'
import { RouterView } from 'vue-router'
import { useI18n } from 'vue-i18n'
import HeaderNav from '@/components/HeaderNav.vue'
import FooterSection from '@/components/FooterSection.vue'
import FloatingMascotButton from '@/components/FloatingMascotButton.vue'
import ChatPanel from '@/components/ChatPanel.vue'
import { useUIStore } from '@/stores/uiStore'

const ui = useUIStore()
const { locale } = useI18n()

watchEffect(() => {
  const isKorean = locale.value === 'ko'
  document.documentElement.lang = isKorean ? 'ko' : 'en'
  document.title = isKorean
    ? 'Local Hub - 서울 로컬 정보 공유 커뮤니티'
    : 'Local Hub - Seoul Local Travel Community'

  const description = isKorean
    ? '서울 여행자들이 로컬 정보, 숨은 명소, 맛집, 여행 후기를 함께 공유하는 커뮤니티입니다.'
    : 'A community where Seoul travelers share local tips, hidden gems, restaurants, and travel reviews.'

  document.querySelector('meta[name="description"]')?.setAttribute('content', description)
  document.querySelector('meta[property="og:title"]')?.setAttribute('content', document.title)
  document.querySelector('meta[property="og:description"]')?.setAttribute('content', description)
  document.querySelector('meta[property="og:locale"]')?.setAttribute('content', isKorean ? 'ko_KR' : 'en_US')
  document.querySelector('meta[name="twitter:title"]')?.setAttribute('content', document.title)
  document.querySelector('meta[name="twitter:description"]')?.setAttribute('content', description)
})
</script>

<template>
  <div id="app" class="min-h-screen flex flex-col bg-white">
    <!-- Header Navigation (투명) -->
    <HeaderNav />

    <!-- Main Content -->
    <main class="flex-1">
      <RouterView />
    </main>

    <!-- Footer -->
    <FooterSection />

    <!-- Floating AI button -->
    <FloatingMascotButton v-if="!ui.showChat" />
    <ChatPanel />
  </div>
</template>

<style scoped>
/* Global styles */
</style>
