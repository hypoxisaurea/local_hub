<template>
  <div @click="$emit('click')" class="h-full flex flex-col bg-white rounded-2xl border border-slate-100 shadow-sm hover:shadow-lg hover:border-rose-200 transition-all cursor-pointer group overflow-hidden">
    <!-- Card Header -->
    <div class="flex items-center justify-between px-6 py-3 bg-gradient-to-r from-slate-50 to-transparent border-b border-slate-100">
      <div class="flex items-center space-x-3">
        <!-- Category Badge -->
        <span class="inline-flex items-center px-3 py-1 bg-rose-50 text-rose-600 rounded-full text-xs font-bold border border-rose-200">
          {{ categoryLabel(post.category) }}
        </span>
        <!-- Timestamp -->
        <span class="text-xs text-slate-400 font-medium">{{ formatTime(post.createdAt) }}</span>
      </div>
    </div>

    <!-- Card Body -->
    <div class="flex-1 px-6 py-4 space-y-2">
      <!-- Title -->
      <h3 class="text-base font-bold text-slate-800 line-clamp-2 group-hover:text-rose-600 transition-colors">
        {{ post.title }}
      </h3>
      <!-- Content Preview -->
      <p class="text-sm text-slate-600 line-clamp-2">
        {{ post.content }}
      </p>
    </div>

    <!-- Card Footer -->
      <div class="px-6 py-3 bg-slate-50 border-t border-slate-100 text-xs">
        <span class="text-slate-500 font-medium">
          <i class="fas fa-user-circle text-slate-400 mr-1"></i>
          {{ post.nickname }}
        </span>
      </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import type { Post } from '@/stores/portalStore'

const props = defineProps<{
  post: Post
}>()

const emit = defineEmits<{
  click: []
  like: []
}>()

const liked = ref(false)
const { locale, t } = useI18n()

const categoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    전체: t('categories.all'),
    여행지: t('categories.travel'),
    맛집: t('categories.restaurant'),
    축제: t('categories.festival'),
    카페: t('categories.cafe'),
  }

  return labels[category] ?? category
}

// 시간 포맷팅 (예: "2시간 전")
const formatTime = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (locale.value === 'en') {
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins} min ago`
    if (diffHours < 24) return `${diffHours} hr ago`
    if (diffDays < 7) return `${diffDays} days ago`

    return date.toLocaleDateString('en-US')
  }

  if (diffMins < 1) return '방금 전'
  if (diffMins < 60) return `${diffMins}분 전`
  if (diffHours < 24) return `${diffHours}시간 전`
  if (diffDays < 7) return `${diffDays}일 전`
  
  return date.toLocaleDateString('ko-KR')
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
