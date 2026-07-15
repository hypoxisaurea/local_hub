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
          {{ t('nav.community') }}
        </RouterLink>
        <RouterLink to="/travel" class="font-medium text-slate-900 transition-colors hover:text-rose-500">
          {{ t('nav.travel') }}
        </RouterLink>
        <RouterLink to="/restaurant" class="font-medium text-slate-900 transition-colors hover:text-rose-500">
          {{ t('nav.restaurant') }}
        </RouterLink>
        <RouterLink to="/festival" class="font-medium text-slate-900 transition-colors hover:text-rose-500">
          {{ t('nav.festival') }}
        </RouterLink>
      </nav>

      <div class="flex items-center gap-2">
        <div
          class="inline-flex items-center rounded-xl border border-slate-200 bg-white/70 p-1 text-xs font-black shadow-sm backdrop-blur-sm"
          role="group"
          aria-label="Language"
        >
          <button
            type="button"
            :aria-pressed="ui.currentLang === 'ko'"
            @click="ui.setChatLanguage('ko')"
            :class="[
              'inline-flex min-w-16 items-center justify-center gap-1.5 rounded-lg px-3 py-1.5 transition-all',
              ui.currentLang === 'ko'
                ? 'bg-white text-slate-950 shadow-sm ring-1 ring-slate-200'
                : 'text-slate-500 opacity-45 hover:opacity-80'
            ]"
          >
            <img src="/assets/icons/korean.png" alt="" class="h-4 w-4 object-contain" aria-hidden="true">
            KO
          </button>

          <button
            type="button"
            :aria-pressed="ui.currentLang === 'en'"
            @click="ui.setChatLanguage('en')"
            :class="[
              'inline-flex min-w-16 items-center justify-center gap-1.5 rounded-lg px-3 py-1.5 transition-all',
              ui.currentLang === 'en'
                ? 'bg-white text-slate-950 shadow-sm ring-1 ring-slate-200'
                : 'text-slate-500 opacity-45 hover:opacity-80'
            ]"
          >
            <img src="/assets/icons/english.png" alt="" class="h-4 w-4 object-contain" aria-hidden="true">
            EN
          </button>
        </div>

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
import { useI18n } from 'vue-i18n'
import { useUIStore } from '@/stores/uiStore'

const ui = useUIStore()
const { t } = useI18n()
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
