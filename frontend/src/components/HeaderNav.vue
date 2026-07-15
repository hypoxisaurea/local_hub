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
      <!-- Logo -->
      <RouterLink to="/" class="flex items-center space-x-2 group">
        <img 
          src="/logos/mascot.png"
          alt="LocalHub Logo"
          class="h-10 w-auto"
        />
        <span class="font-bold text-xl text-slate-900">
          LocalHub
        </span>
      </RouterLink>

      <!-- Desktop Navigation -->
      <nav class="hidden md:flex items-center space-x-8">
        <RouterLink 
          to="/community" 
          class="font-medium text-slate-900 transition-colors hover:text-rose-500"
        >
          커뮤니티
        </RouterLink>
        <RouterLink 
          to="/travel" 
          class="font-medium text-slate-900 transition-colors hover:text-rose-500"
        >
          여행지
        </RouterLink>
        <RouterLink 
          to="/restaurant" 
          class="font-medium text-slate-900 transition-colors hover:text-rose-500"
        >
          맛집
        </RouterLink>
        <RouterLink 
          to="/festival" 
          class="font-medium text-slate-900 transition-colors hover:text-rose-500"
        >
          축제
        </RouterLink>
      </nav>

      <!-- Mobile Menu Button -->
      <button class="md:hidden">
        <i class="fas fa-bars text-xl text-slate-900"></i>
      </button>
    </nav>
  </header>

</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'

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

<style scoped>
/* 스타일은 template에서 동적으로 처리 */
</style>