<template>
  <header
    :class="[
      'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
      isScrolled
        ? 'bg-white/95 backdrop-blur-md shadow-md'
        : 'bg-transparent'
    ]"
  >
    <nav class="relative max-w-7xl mx-auto px-4 lg:px-8 py-4 flex items-center justify-between">
      <RouterLink to="/" class="flex items-center space-x-2 group">
        <img src="/logos/mascot.png" alt="LocalHub Logo" class="h-10 w-auto" />
        <span class="font-bold text-xl text-slate-900">
          LocalHub
        </span>
      </RouterLink>

      <nav class="hidden md:flex items-center space-x-8">
        <RouterLink to="/community" class="font-medium text-slate-900 transition-colors hover:text-rose-500">
          {{ ui.currentLang === 'ko' ? '커뮤니티' : 'Community' }}
        </RouterLink>
        <RouterLink to="/travel" class="font-medium text-slate-900 transition-colors hover:text-rose-500">
          {{ ui.currentLang === 'ko' ? '여행지' : 'Places' }}
        </RouterLink>
        <RouterLink to="/restaurant" class="font-medium text-slate-900 transition-colors hover:text-rose-500">
          {{ ui.currentLang === 'ko' ? '맛집' : 'Restaurants' }}
        </RouterLink>
        <RouterLink to="/festival" class="font-medium text-slate-900 transition-colors hover:text-rose-500">
          {{ ui.currentLang === 'ko' ? '축제' : 'Festivals' }}
        </RouterLink>
      </nav>

      <div class="flex items-center gap-2">
        <button
          @click="ui.toggleLang()"
          class="px-3 py-2 rounded-lg border border-slate-300 text-sm font-medium text-slate-700 hover:bg-slate-50"
        >
          {{ ui.currentLang === 'ko' ? 'EN' : 'KO' }}
        </button>

        <button class="md:hidden">
          <i class="fas fa-bars text-xl text-slate-900"></i>
        </button>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useUIStore } from '@/stores/uiStore'

const ui = useUIStore()
const isScrolled = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>