<template>
  <div class="share-wrap" :aria-label="t('share.label')">
    <button
      v-if="canNativeShare"
      type="button"
      class="share-button"
      :title="t('share.native')"
      :aria-label="t('share.native')"
      @click="shareNative"
    >
      <i class="fa-solid fa-share-nodes"></i>
    </button>

    <a
      class="share-button"
      :href="facebookUrl"
      target="_blank"
      rel="noopener noreferrer"
      :title="t('share.facebook')"
      :aria-label="t('share.facebook')"
    >
      <i class="fa-brands fa-facebook-f"></i>
    </a>

    <a
      class="share-button"
      :href="xUrl"
      target="_blank"
      rel="noopener noreferrer"
      :title="t('share.x')"
      :aria-label="t('share.x')"
    >
      <i class="fa-brands fa-x-twitter"></i>
    </a>

    <a
      class="share-button"
      :href="kakaoUrl"
      target="_blank"
      rel="noopener noreferrer"
      :title="t('share.kakao')"
      :aria-label="t('share.kakao')"
    >
      <i class="fa-solid fa-comment"></i>
    </a>

    <button
      type="button"
      class="share-button"
      :title="copyLabel"
      :aria-label="copyLabel"
      @click="copyLink"
    >
      <i :class="copied ? 'fa-solid fa-check' : 'fa-solid fa-link'"></i>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { getShareText, getShareUrl } from '@/utils/seo'

const route = useRoute()
const { locale, t } = useI18n()
const copied = ref(false)

const shareUrl = computed(() => getShareUrl(route.fullPath))
const shareText = computed(() => getShareText(route, locale.value === 'en' ? 'en' : 'ko'))
const encodedUrl = computed(() => encodeURIComponent(shareUrl.value))
const encodedTitle = computed(() => encodeURIComponent(shareText.value.title))
const copyLabel = computed(() => copied.value ? t('share.copied') : t('share.copy'))
const canNativeShare = computed(() => typeof navigator !== 'undefined' && 'share' in navigator)

const facebookUrl = computed(() => `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl.value}`)
const xUrl = computed(() => `https://twitter.com/intent/tweet?url=${encodedUrl.value}&text=${encodedTitle.value}`)
const kakaoUrl = computed(() => `https://story.kakao.com/share?url=${encodedUrl.value}`)

const shareNative = async () => {
  if (!navigator.share) return

  await navigator.share({
    title: shareText.value.title,
    text: shareText.value.description,
    url: shareUrl.value,
  })
}

const copyLink = async () => {
  await navigator.clipboard.writeText(shareUrl.value)
  copied.value = true

  window.setTimeout(() => {
    copied.value = false
  }, 1800)
}
</script>

<style scoped>
.share-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.share-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 0;
  border-radius: 9999px;
  background: #555;
  color: #fff;
  cursor: pointer;
  text-decoration: none;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.share-button:hover {
  background: #e11d48;
  color: #fff;
  transform: translateY(-1px);
}
</style>
