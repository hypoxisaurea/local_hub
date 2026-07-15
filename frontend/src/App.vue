<script setup lang="ts">
import { RouterView } from 'vue-router'
import HeaderNav from '@/components/HeaderNav.vue'
import FooterSection from '@/components/FooterSection.vue'
import FloatingMascotButton from '@/components/FloatingMascotButton.vue'
import ChatPanel from '@/components/ChatPanel.vue'
import { useUIStore } from '@/stores/uiStore'
/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}


const ui = useUIStore()
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
