<template>
  <LocalListPage
    :title="t('list.festivalTitle')"
    :placeholder="t('list.festivalPlaceholder')"
    :search-query="searchQuery"
    :selected-tag="selectedTag"
    :items="paginatedFestivals"
    :current-page="currentPage"
    :page-numbers="pageNumbers"
    :total-pages="totalPages"
    @page-change="movePage"
    @update:search-query="searchQuery = $event"
    @search="searchFestivals"
    @tag-click="toggleTag"
    @keyword-click="searchKeyword"
  />
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import LocalListPage from '@/components/LocalListPage.vue'
import type { LocalPlace } from '@/types/local'

const { locale, t } = useI18n()
const searchQuery = ref('')
const selectedTag = ref('')
const festivalItems = ref<LocalPlace[]>([])
const DISPLAY_PAGE_COUNT = 10
const ITEMS_PER_PAGE = 10

// --- 페이지네이션 상태 ---
const currentPage = ref(1)
const ITEMS_PER_PAGE = 10

// 필터링 로직
const filteredFestivals = computed(() => {
  const query = searchQuery.value.toLowerCase().replace('#', '')
  const tag = selectedTag.value.replace('#', '')

  return festivalItems.value.filter((festival) => {
    const text = [festival.title, festival.location, ...festival.tags]
      .join(' ')
      .toLowerCase()
      .replaceAll('#', '')
    return (!query || text.includes(query)) && (!tag || text.includes(tag))
  })
})

<<<<<<< HEAD
// 페이지네이션 계산 속성
const totalPages = computed(() => Math.max(1, Math.ceil(filteredFestivals.value.length / ITEMS_PER_PAGE)))

const paginatedFestivals = computed(() => {
  const start = (currentPage.value - 1) * ITEMS_PER_PAGE
  return filteredFestivals.value.slice(start, start + ITEMS_PER_PAGE)
})

const DISPLAY_PAGE_COUNT = 10
const pageNumbers = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  let startPage = Math.max(1, current - Math.floor(DISPLAY_PAGE_COUNT / 2))
  let endPage = Math.min(total, startPage + DISPLAY_PAGE_COUNT - 1)
  startPage = Math.max(1, endPage - DISPLAY_PAGE_COUNT + 1)
  
  return Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i)
})

const movePage = (page: number) => {
  currentPage.value = page
=======
const totalPages = computed(() => Math.max(1, Math.ceil(filteredFestivals.value.length / ITEMS_PER_PAGE)))

const paginatedPlaces = computed(() => {
  const start = (currentPage.value - 1) * ITEMS_PER_PAGE

  return filteredFestivals.value.slice(start, start + ITEMS_PER_PAGE)
})

const currentPage = ref(1)

const pageNumbers = computed(() => {
  const total = totalPages.value
  const current = currentPage.value

  if (total <= DISPLAY_PAGE_COUNT) {
    return Array.from({ length: total }, (_, index) => index + 1)
  }

  let startPage = current - Math.floor(DISPLAY_PAGE_COUNT / 2)
  let endPage = current + Math.floor(DISPLAY_PAGE_COUNT / 2) - 1

  if (startPage < 1) {
    startPage = 1
    endPage = DISPLAY_PAGE_COUNT
  }

  if (endPage > total) {
    endPage = total
    startPage = total - DISPLAY_PAGE_COUNT + 1
  }

  return Array.from({ length: DISPLAY_PAGE_COUNT }, (_, index) => startPage + index)
})

const movePage = (page: number) => {
  currentPage.value = Math.min(Math.max(page, 1), totalPages.value)
}

function searchFestivals() {
  currentPage.value = 1
  fetchFestivals()
>>>>>>> origin/ai
}

// API 및 검색 함수
const fetchFestivals = async () => {
  const params = new URLSearchParams({ lang: locale.value })
  if (searchQuery.value.trim()) {
    params.set('q', searchQuery.value.trim())
  }
  const response = await fetch(`/api/travel-spots-simple/festivals?${params.toString()}`)
  if (!response.ok) { festivalItems.value = []; return }
  const data = await response.json() as any[]
  festivalItems.value = data.map((item, index) => ({
    id: Number(item.contentid) || index,
    title: item.title,
    location: item.addr1 || '',
    tags: [locale.value === 'ko' ? '#축제' : '#Festivals'],
    image: item.firstimage || '/banners/banner.png',
  }))
}

function searchFestivals() {
  currentPage.value = 1 // 검색 시 1페이지로!
  fetchFestivals()
}

function searchKeyword(keyword: string) {
  searchQuery.value = keyword
  selectedTag.value = ''
<<<<<<< HEAD
  currentPage.value = 1 // 검색 시 1페이지로!
=======
  currentPage.value = 1
>>>>>>> origin/ai
  fetchFestivals()
}

function toggleTag(tag: string) {
  selectedTag.value = selectedTag.value === tag ? '' : tag
}

watch(locale, () => {
  selectedTag.value = ''
  currentPage.value = 1
  fetchFestivals()
})

onMounted(fetchFestivals)
</script>
