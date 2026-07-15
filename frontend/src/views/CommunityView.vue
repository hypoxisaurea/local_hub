<template>
  <section class="w-full flex-1 flex flex-col animate-fadeIn py-12">
    <div class="max-w-7xl mx-auto w-full px-4 lg:px-8">
      
      <!-- Page Header -->
      <div class="mb-12">
        <h1 class="text-4xl font-black text-slate-900 mb-3">{{ pageTitle }}</h1>
        <p class="text-slate-500 text-lg">{{ pageSubtitle }}</p>
      </div>

      <!-- Category & Search Section -->
      <div class="space-y-6 mb-8">
        <!-- Category Buttons -->
        <div class="grid grid-cols-3 sm:grid-cols-6 gap-3">
          <!-- 전체보기 버튼 -->
          <button 
            @click="portal.selectedCategory = '전체'" 
            :class="[
              'p-4 rounded-2xl flex flex-col items-center justify-center border transition-all hover:shadow-md',
              portal.selectedCategory === '전체' 
                ? 'bg-rose-500 text-white border-rose-500 shadow-md shadow-rose-100' 
                : 'bg-white text-slate-600 border-slate-100'
            ]"
          >
            <div :class="['w-10 h-10 rounded-xl flex items-center justify-center mb-2', portal.selectedCategory === '전체' ? 'bg-rose-400 text-white' : 'bg-slate-50']">
              <i class="fas fa-grid-2 text-lg"></i>
            </div>
            <span class="text-xs font-bold">전체보기</span>
          </button>

          <!-- 카테고리 버튼들 -->
          <button 
            v-for="cat in categories" 
            :key="cat"
            @click="portal.selectedCategory = cat"
            :class="[
              'p-4 rounded-2xl flex flex-col items-center justify-center border transition-all hover:shadow-md',
              portal.selectedCategory === cat 
                ? 'bg-rose-500 text-white border-rose-500 shadow-md shadow-rose-100' 
                : 'bg-white text-slate-600 border-slate-100'
            ]"
          >
            <div :class="['w-10 h-10 rounded-xl flex items-center justify-center mb-2', portal.selectedCategory === cat ? 'bg-rose-400 text-white' : 'bg-slate-50']">
              <i :class="getCategoryIcon(cat)"></i>
            </div>
            <span class="text-xs font-bold">{{ cat }}</span>
          </button>
        </div>

        <!-- Search Bar -->
        <div class="bg-white p-3 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-2">
          <i class="fas fa-magnifying-glass text-slate-400 ml-3"></i>
          <input 
            v-model="searchQuery" 
            @keyup.enter="runSearch"
            type="text" 
            :placeholder="searchPlaceholder"
            class="flex-1 bg-transparent border-none text-sm text-slate-800 placeholder-slate-400 focus:outline-none"
          >
          <button @click="runSearch" class="bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded-xl text-xs font-bold transition-all">
            {{ searchLabel }}
          </button>
        </div>
      </div>

      <!-- Posts Section -->
      <div>
        <h3 class="text-lg font-black text-slate-800 flex items-center mb-4">
          <span class="w-2 h-5 bg-rose-500 rounded-full mr-2"></span>
          전체 게시글
        </h3>

        <!-- Posts Grid -->
        <div v-if="portal.filteredPosts.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <PostCard 
            v-for="post in portal.filteredPosts" 
            :key="post.id"
            :post="post"
            @click="viewPost(post)"
            @like="likePost(post.id)"
          />
        </div>

        <!-- No Posts Message -->
        <div v-else class="bg-slate-50 border border-slate-200 rounded-2xl p-16 text-center">
          <i class="fas fa-inbox text-4xl text-slate-300 mb-3"></i>
          <p class="text-slate-500 font-semibold">{{ emptyLabel }}</p>
          <p class="text-slate-400 text-sm mt-1">{{ emptyHint }}</p>
          <button @click="ui.openWriteModal()" class="bg-rose-500 hover:bg-rose-600 text-white px-6 py-2.5 rounded-xl font-bold mt-4 transition-all shadow-md shadow-rose-100">
            <i class="fas fa-pen-fancy mr-2"></i>
              {{ writeLabel }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { usePortalStore } from '@/stores/portalStore'
import { useUIStore } from '@/stores/uiStore'
import type { Post } from '@/stores/portalStore'
import PostCard from '@/components/PostCard.vue'

const portal = usePortalStore()
const ui = useUIStore()

const searchQuery = ref('')


const pageTitle = computed(() => ui.currentLang === 'ko' ? '커뮤니티' : 'Community')
const pageSubtitle = computed(() =>
  ui.currentLang === 'ko' ? '지역 커뮤니티와 소통하세요' : 'Connect with your local community'
)
const searchPlaceholder = computed(() =>
  ui.currentLang === 'ko' ? '게시글 검색...' : 'Search posts...'
)
const searchLabel = computed(() => ui.currentLang === 'ko' ? '검색' : 'Search')
const allPostsLabel = computed(() => ui.currentLang === 'ko' ? '전체 게시글' : 'All posts')
const writeLabel = computed(() => ui.currentLang === 'ko' ? '글 작성하기' : 'Write a post')
const emptyLabel = computed(() => ui.currentLang === 'ko' ? '게시글이 없습니다.' : 'No posts yet.')

// 검색 실행
const runSearch = () => {
  portal.searchQuery = searchQuery.value
  if (searchQuery.value.trim()) {
    ui.showToast(`"${searchQuery.value}" 검색이 적용되었습니다.`)
  }
}

// 카테고리 아이콘 반환
const getCategoryIcon = (cat: string): string => {
  const icons: Record<string, string> = {
    '여행지': 'fas fa-map-location-dot text-rose-500',
    '맛집': 'fas fa-utensils text-rose-500',
    '카페': 'fas fa-mug-hot text-rose-500',
    '축제': 'fas fa-wand-magic-sparkles text-rose-500',
    '팁/후기': 'fas fa-lightbulb text-rose-500'
  }
  return icons[cat] || 'fas fa-circle-info text-rose-500'
}

// 게시글 상세보기
const viewPost = (post: Post) => {
  ui.setView('post-detail')
  console.log('선택된 게시글:', post)
}

// 좋아요
const likePost = (postId: number) => {
  portal.likePost(postId)
  ui.showToast('❤️ 좋아요!')
}
</script>