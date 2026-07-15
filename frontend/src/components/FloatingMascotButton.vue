<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useUIStore } from '@/stores/uiStore'

const ui = useUIStore()
const footerOffset = ref(0)

let frameId = 0

const updateFooterOffset = () => {
  if (frameId) {
    cancelAnimationFrame(frameId)
  }

  frameId = requestAnimationFrame(() => {
    const footer = document.querySelector<HTMLElement>('footer.footer')

    if (!footer) {
      footerOffset.value = 0
      return
    }

    const footerTop = footer.getBoundingClientRect().top
    footerOffset.value = Math.max(0, window.innerHeight - footerTop)
  })
}

onMounted(() => {
  updateFooterOffset()
  window.addEventListener('scroll', updateFooterOffset, { passive: true })
  window.addEventListener('resize', updateFooterOffset)
})

onBeforeUnmount(() => {
  if (frameId) {
    cancelAnimationFrame(frameId)
  }

  window.removeEventListener('scroll', updateFooterOffset)
  window.removeEventListener('resize', updateFooterOffset)
})
</script>

<template>
  <button
    type="button"
    class="floating-mascot-button"
    :style="{ '--floating-footer-offset': `${footerOffset}px` }"
    aria-label="LocalHub AI 열기"
    title="LocalHub AI"
    @click="ui.toggleChat()"
  >
    <span class="floating-mascot-button__glow" aria-hidden="true"></span>
    <span class="floating-mascot-button__image-wrap" aria-hidden="true">
      <img src="/assets/floating_button.png" alt="" class="floating-mascot-button__image">
    </span>
  </button>
</template>

<style scoped>
.floating-mascot-button {
  position: fixed;
  right: max(50px, env(safe-area-inset-right));
  bottom: calc(max(18px, env(safe-area-inset-bottom)) + var(--floating-footer-offset, 0px));
  z-index: 60;
  width: clamp(72px, 8vw, 92px);
  height: clamp(72px, 8vw, 92px);
  padding: 0;
  border: 0;
  border-radius: 9999px;
  background: radial-gradient(circle at 32% 24%, #ffd7e8 0 18%, #ff80b2 52%, #f0468a 100%);
  box-shadow:
    0 16px 34px rgba(225, 29, 104, 0.32),
    0 0 0 4px rgba(255, 255, 255, 0.95),
    inset 0 3px 10px rgba(255, 255, 255, 0.55);
  cursor: pointer;
  overflow: visible;
  transition:
    transform 180ms ease,
    box-shadow 180ms ease,
    filter 180ms ease;
}

.floating-mascot-button:hover {
  transform: translateY(-4px) scale(1.04);
  box-shadow:
    0 20px 42px rgba(225, 29, 104, 0.4),
    0 0 0 4px rgba(255, 255, 255, 1),
    inset 0 3px 10px rgba(255, 255, 255, 0.62);
}

.floating-mascot-button:active {
  transform: translateY(-1px) scale(0.98);
}

.floating-mascot-button:focus-visible {
  outline: 3px solid #14b8a6;
  outline-offset: 5px;
}

.floating-mascot-button__glow {
  position: absolute;
  inset: -10px;
  z-index: -1;
  border-radius: inherit;
  background: rgba(244, 114, 182, 0.28);
  filter: blur(12px);
}

.floating-mascot-button__image-wrap {
  position: absolute;
  inset: 0;
  display: block;
  border-radius: inherit;
  overflow: hidden;
}

.floating-mascot-button__image-wrap::before {
  position: absolute;
  inset: 3px;
  z-index: 1;
  content: "";
  border-radius: inherit;
  border: 2px solid rgba(255, 190, 216, 0.72);
  box-shadow: inset 5px 8px 14px rgba(255, 255, 255, 0.36);
  pointer-events: none;
}

.floating-mascot-button__image {
  position: absolute;
  left: 50%;
  bottom: -18%;
  width: 108%;
  max-width: none;
  transform: translateX(-50%);
  pointer-events: none;
  user-select: none;
}

@media (max-width: 640px) {
  .floating-mascot-button {
    right: max(14px, env(safe-area-inset-right));
    bottom: calc(max(14px, env(safe-area-inset-bottom)) + var(--floating-footer-offset, 0px));
  }
}
</style>
