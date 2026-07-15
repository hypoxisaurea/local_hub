<template>
  <header
    :class="[
      'fixed top-2 left-0 right-0 z-50 transition-all duration-300',
      isScrolled ? 'bg-white/95 backdrop-blur-md shadow-md' : 'bg-transparent',
    ]"
  >
    <nav
      class="relative flex items-center justify-between px-4 py-4 mx-auto max-w-7xl lg:px-8"
    >
      <RouterLink to="/" class="flex items-center space-x-2 group">
        <img src="/logos/logo.png" alt="LocalHub Logo" class="w-auto h-10" />
        <span class="text-2xl font-black text-slate-900"> LocalHub </span>
      </RouterLink>

      <nav class="items-center hidden space-x-8 md:flex">
        <RouterLink
          to="/community"
          class="font-medium transition-colors text-slate-900 hover:text-rose-500"
        >
          {{ t("nav.community") }}
        </RouterLink>
        <RouterLink
          to="/travel"
          class="font-medium transition-colors text-slate-900 hover:text-rose-500"
        >
          {{ t("nav.travel") }}
        </RouterLink>
        <RouterLink
          to="/restaurant"
          class="font-medium transition-colors text-slate-900 hover:text-rose-500"
        >
          {{ t("nav.restaurant") }}
        </RouterLink>
        <RouterLink
          to="/festival"
          class="font-medium transition-colors text-slate-900 hover:text-rose-500"
        >
          {{ t("nav.festival") }}
        </RouterLink>
      </nav>

      <div class="flex items-center gap-2">
        <div
          class="inline-flex items-center p-1 text-xs font-black border shadow-sm rounded-xl border-slate-200 bg-white/70 backdrop-blur-sm"
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
                : 'text-slate-500 opacity-45 hover:opacity-80',
            ]"
          >
            <img
              src="/assets/icons/korean.png"
              alt=""
              class="object-contain w-4 h-4"
              aria-hidden="true"
            />
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
                : 'text-slate-500 opacity-45 hover:opacity-80',
            ]"
          >
            <img
              src="/assets/icons/english.png"
              alt=""
              class="object-contain w-4 h-4"
              aria-hidden="true"
            />
            EN
          </button>
        </div>

        <button class="md:hidden">
          <i class="text-xl fas fa-bars text-slate-900"></i>
        </button>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { RouterLink } from "vue-router";
import { useI18n } from "vue-i18n";
import { useUIStore } from "@/stores/uiStore";

const ui = useUIStore();
const { t } = useI18n();
const isScrolled = ref(false);

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>
