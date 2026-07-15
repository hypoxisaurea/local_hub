<template>
  <FoodListPage
    :title="t('list.restaurantTitle')"
    :placeholder="t('list.restaurantPlaceholder')"
    :search-query="searchQuery"
    :selected-tag="selectedTag"
    :recommended-tags="recommendedTags"
    :items="filteredRestaurants"
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

const recommendedTags = computed(() =>
  locale.value === 'ko'
    ? ['#한식', '#카페', '#혼밥', '#데이트']
    : ['#KoreanFood', '#Cafe', '#SoloDining', '#Date']
)

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

function searchRestaurants() {
  fetchRestaurants()
}

function toggleTag(tag: string) {
  selectedTag.value = selectedTag.value === tag ? '' : tag
}

function searchKeyword(keyword: string) {
  searchQuery.value = keyword
  selectedTag.value = ''
  fetchRestaurants()
}

watch(locale, () => {
  selectedTag.value = ''
  fetchRestaurants()
})

onMounted(fetchRestaurants)
</script>
