<template>
  <section class="w-full flex-1 flex flex-col animate-fadeIn">
    
    <!-- Hero Banner with Background Image -->
    <div 
      class="relative py-12 lg:py-24 px-6 lg:px-16 overflow-hidden"
      :style="{ 
        backgroundImage: 'url(/banners/banner.png)',
        backgroundSize: 'contain',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }"
    >
      
      <!-- Content -->
      <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
        
        <!-- Left Hero Column -->
        <div class="lg:col-span-7 space-y-6">
          <!-- Live Badge -->
          <div class="inline-flex items-center space-x-2 bg-white/80 backdrop-blur-sm px-3.5 py-1.5 rounded-full border border-slate-200/50 shadow-sm">
            <span class="flex h-2 w-2 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
            </span>
            <span class="text-xs font-bold text-slate-700">공공데이터 실시간 연동 완료</span>
          </div>
          
          <!-- Main Title (텍스트색 변경) -->
          <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-slate-900 leading-tight">
            서울, 우리끼리 <br class="hidden sm:inline">
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-rose-300 to-pink-300">로컬 정보 공유해요!</span>
          </h1>
          
          <!-- Description (텍스트색 변경) -->
          <p class="text-slate-700 text-sm sm:text-base max-w-xl font-medium leading-relaxed">
            여행자들의 생생한 리뷰와 꿀팁을 한 곳에서 만나보세요. <br class="hidden xs:inline">
            가입이나 로그인 절차 없이, 익명으로 자유롭게 소통하는 프리미엄 커뮤니티 공간입니다.
          </p>

          <!-- Hero Search Bar -->
          <div class="max-w-lg bg-white/95 backdrop-blur-sm p-2 rounded-2xl shadow-xl shadow-slate-900/20 border border-white/30 flex items-center space-x-2">
            <i class="fas fa-magnifying-glass text-slate-400 ml-3"></i>
            <input 
              v-model="searchQuery" 
              @keyup.enter="runSearch"
              type="text" 
              placeholder="어디를 찾고 있나요? (예: 을지로, 맛집, 성수동)" 
              class="flex-1 bg-transparent border-none text-sm text-slate-800 placeholder-slate-400 focus:outline-none"
            >
            <button @click="runSearch" class="bg-rose-500 hover:bg-rose-600 text-white px-5 py-2.5 rounded-xl text-xs font-bold shadow-md shadow-rose-100 transition-all">
              검색
            </button>
          </div>

          <!-- Trending Hashtags -->
          <div class="flex flex-wrap gap-2 pt-2 text-xs">
            <span class="text-slate-900 font-semibold self-center">추천 검색어:</span>
            <button @click="applyTag('#명동 카페')" class="bg-slate-100 hover:bg-slate-200 text-slate-900 hover:text-slate-900 border border-slate-200 px-3 py-1.5 rounded-full font-medium shadow-sm transition-all backdrop-blur-sm">#명동 카페</button>
            <button @click="applyTag('#남산 야경')" class="bg-slate-100 hover:bg-slate-200 text-slate-900 hover:text-slate-900 border border-slate-200 px-3 py-1.5 rounded-full font-medium shadow-sm transition-all backdrop-blur-sm">#남산 야경</button>
            <button @click="applyTag('#을지로 핫플')" class="bg-slate-100 hover:bg-slate-200 text-slate-900 hover:text-slate-900 border border-slate-200 px-3 py-1.5 rounded-full font-medium shadow-sm transition-all backdrop-blur-sm">#을지로 핫플</button>
            <button @click="applyTag('#실시간 혼잡도')" class="bg-slate-100 hover:bg-slate-200 text-slate-900 hover:text-slate-900 border border-slate-200 px-3 py-1.5 rounded-full font-medium shadow-sm transition-all backdrop-blur-sm">#실시간 혼잡도</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Map & Content Section -->
    <div class="max-w-7xl mx-auto w-full px-4 lg:px-8 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <!-- Left: Map Area (추후 지도 연동) -->
      <div class="lg:col-span-8">
        <div class="bg-gradient-to-br from-slate-100 to-slate-50 rounded-2xl border border-slate-200 p-8 min-h-[600px] flex flex-col items-center justify-center shadow-sm">
          <i class="fas fa-map text-6xl text-slate-300 mb-4"></i>
          <h3 class="text-2xl font-bold text-slate-700 mb-2">실시간 인기 게시글</h3>
          <p class="text-slate-500 text-center max-w-md">
            지도 기반 정보 공유 시스템<br>
            곧 지도를 통해 실시간 인기 게시글을 확인할 수 있습니다.
          </p>
          <div class="mt-6 flex gap-3">
            <button @click="ui.openWriteModal()" class="bg-rose-500 hover:bg-rose-600 text-white px-6 py-2.5 rounded-xl font-bold transition-all shadow-md shadow-rose-100">
              <i class="fas fa-pen-fancy mr-2"></i>
              글 작성하기
            </button>
            <RouterLink to="/community" class="bg-slate-200 hover:bg-slate-300 text-slate-800 px-6 py-2.5 rounded-xl font-bold transition-all">
              <i class="fas fa-comments mr-2"></i>
              커뮤니티 보기
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Right: Sidebar Widgets -->
      <div class="lg:col-span-4 space-y-6">
        <!-- Weather Widget -->
        <div class="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm">
          <h4 class="font-bold text-slate-800 mb-3 flex items-center">
            <i class="fas fa-cloud-sun text-yellow-500 mr-2"></i> 오늘의 날씨
          </h4>
          <p class="text-slate-500 text-sm">서울 중구 / 맑음 · 26°C</p>
        </div>

        <!-- Chatbot Card -->
        <div @click="ui.toggleChat()" class="bg-gradient-to-br from-rose-500 to-pink-600 rounded-2xl p-6 text-white cursor-pointer hover:shadow-lg shadow-md shadow-rose-100 transition-all">
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-bold">LocalHub AI</h4>
            <i class="fas fa-robot text-xl"></i>
          </div>
          <p class="text-sm text-rose-50">여행 계획 도와드려요! 클릭해서 시작하세요.</p>
        </div>

        <!-- Notices Widget -->
        <div class="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm">
          <h4 class="font-bold text-slate-800 mb-3 flex items-center">
            <i class="fas fa-bullhorn text-blue-500 mr-2"></i> 공지사항
          </h4>
          <ul class="space-y-2">
            <li class="text-xs text-slate-600 pb-2 border-b border-slate-100">
              <span class="font-semibold text-slate-800">커뮤니티 이용규칙 안내</span>
              <p class="text-slate-400 mt-1">7월 14일</p>
            </li>
            <li class="text-xs text-slate-600">
              <span class="font-semibold text-slate-800">서버 점검 예정</span>
              <p class="text-slate-400 mt-1">7월 20일 02:00~04:00</p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { usePortalStore } from '@/stores/portalStore'
import { useUIStore } from '@/stores/uiStore'

// Store 인스턴스
const portal = usePortalStore()
const ui = useUIStore()

// 로컬 상태
const searchQuery = ref('')

// 검색 실행
const runSearch = () => {
  portal.searchQuery = searchQuery.value
  if (searchQuery.value.trim()) {
    ui.showToast(`"${searchQuery.value}" 검색이 적용되었습니다.`)
  }
}

// 태그 적용
const applyTag = (tag: string) => {
  const cleaned = tag.replace('#', '').trim()
  searchQuery.value = cleaned
  portal.searchQuery = cleaned
  portal.selectedCategory = '전체'
}
</script>

<style scoped>
/* 애니메이션이 필요하면 여기 추가 */
</style>