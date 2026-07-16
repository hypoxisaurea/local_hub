<script setup lang="ts">
import { watchEffect } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import HeaderNav from '@/components/HeaderNav.vue'
import FooterSection from '@/components/FooterSection.vue'
import FloatingMascotButton from '@/components/FloatingMascotButton.vue'
import ChatPanel from '@/components/ChatPanel.vue'
import { useUIStore } from '@/stores/uiStore'
import { updateSeo } from '@/utils/seo'

const ui = useUIStore()
const route = useRoute()
const { locale } = useI18n()

watchEffect(() => {
  updateSeo(route, locale.value === 'en' ? 'en' : 'ko')
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
