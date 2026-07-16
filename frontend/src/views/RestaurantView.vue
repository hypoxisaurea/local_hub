<template>
  <FoodListPage
    :title="t('list.restaurantTitle')"
    :placeholder="t('list.restaurantPlaceholder')"
    :search-query="searchQuery"
    :selected-tag="selectedTag"
    :items="paginatedRestaurants"
    :current-page="currentPage"
    :page-numbers="pageNumbers"
    :total-pages="totalPages"
    @page-change="movePage"
    @update:search-query="searchQuery = $event"
    @search="searchRestaurants"
    @tag-click="toggleTag"
    @keyword-click="searchKeyword"
  />
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import FoodListPage from '@/components/FoodListPage.vue'
import type { LocalPlace } from '@/types/local'

const { locale, t } = useI18n()
const searchQuery = ref('')
const selectedTag = ref('')
const restaurantItems = ref<LocalPlace[]>([])

// --- 페이지네이션 상태 추가 ---
const currentPage = ref(1)
const ITEMS_PER_PAGE = 9

// 필터링 로직
const filteredRestaurants = computed(() => {
  const query = searchQuery.value.toLowerCase().replace('#', '')
  const tag = selectedTag.value.replace('#', '')

  return restaurantItems.value.filter((restaurant) => {
    const text = [restaurant.title, restaurant.location, ...restaurant.tags]
      .join(' ')
      .toLowerCase()
      .replaceAll('#', '')
    return (!query || text.includes(query)) && (!tag || text.includes(tag))
  })
})

// --- 페이지네이션 계산 속성 ---
const totalPages = computed(() => Math.max(1, Math.ceil(filteredRestaurants.value.length / ITEMS_PER_PAGE)))

const paginatedRestaurants = computed(() => {
  const start = (currentPage.value - 1) * ITEMS_PER_PAGE
  return filteredRestaurants.value.slice(start, start + ITEMS_PER_PAGE)
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
}

interface RestaurantResponse {
  id: number
  title: string
  address?: string | null
  new_address?: string | null
  represent_menu?: string | null
  lang_code_id?: string | null
}

const toRestaurantPlace = (item: RestaurantResponse): LocalPlace => ({
  id: item.id,
  title: item.title,
  location: item.new_address || item.address || '',
  tags: [
    locale.value === 'ko' ? '#맛집' : '#Restaurants',
    ...(item.represent_menu ? item.represent_menu.split(/[,/\n]/).slice(0, 2).map((menu) => `#${menu.trim().replace(/\s+/g, '')}`) : []),
  ],
  image: '',
})

const fetchRestaurants = async () => {
  const params = new URLSearchParams({ lang: locale.value })
  if (searchQuery.value.trim()) {
    params.set('q', searchQuery.value.trim())
  }

  const response = await fetch(`/api/restaurants?${params.toString()}`)
  if (!response.ok) {
    restaurantItems.value = []
    return
  }

  const data = await response.json() as RestaurantResponse[]
  restaurantItems.value = data.map(toRestaurantPlace)
}

function searchRestaurants() {
  currentPage.value = 1
  fetchRestaurants()
}

function toggleTag(tag: string) {
  selectedTag.value = selectedTag.value === tag ? '' : tag
}

function searchKeyword(keyword: string) {
  searchQuery.value = keyword
  selectedTag.value = ''
  currentPage.value = 1
  fetchRestaurants()
}

watch(locale, () => {
  selectedTag.value = ''
  fetchRestaurants()
})

onMounted(fetchRestaurants)
</script>
