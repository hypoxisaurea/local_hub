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
// 1. onMounted 임포트 추가
import { computed, ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import FoodListPage from '@/components/FoodListPage.vue'
import type { LocalPlace } from '@/types/local'

// 2. 인터페이스 이름 수정 (RestaurantRowRow -> RestaurantRow)
interface RestaurantRow {
  id: string
  title: string
  address?: string | null
}

const { locale, t } = useI18n()
const searchQuery = ref('')
const selectedTag = ref('')

// 3. 누락되었던 restaurants 반응형 변수 선언 추가
const restaurants = ref<LocalPlace[]>([])

const recommendedTags = computed(() =>
  locale.value === 'ko'
    ? ['#한식', '#카페', '#혼밥', '#데이트']
    : ['#KoreanFood', '#Cafe', '#SoloDining', '#Date']
)

const filteredRestaurants = computed(() => {
  const query = searchQuery.value.toLowerCase().replace('#', '')
  const tag = selectedTag.value.replace('#', '')

  return restaurants.value.filter((restaurant) => {
    const text = [restaurant.title, restaurant.location, ...restaurant.tags]
      .join(' ')
      .toLowerCase()
      .replaceAll('#', '')

    return (!query || text.includes(query)) && (!tag || text.includes(tag))
  })
})

async function fetchRestaurants() {
  try {
    const res = await fetch('/api/restaurants')
    if (!res.ok) throw new Error('failed to load restaurant')

    const rows: RestaurantRow[] = await res.json()
    restaurants.value = rows.map((row, index) => ({
      id: Number(row.id) || index + 1,
      title: row.title || '제목 없음',
      location: row.address || '서울',
      tags: ['#맛집', '#음식점', '#냠냠'],
    }))
  } catch (error) {
    console.error('Failed to load restaurants from DB', error)
    // 4. 오타 수정 (restaurant -> restaurants)
    restaurants.value = []
  }
}

onMounted(() => {
  fetchRestaurants()
})

function searchRestaurants() {
  console.log(searchQuery.value)
}

function toggleTag(tag: string) {
  selectedTag.value = selectedTag.value === tag ? '' : tag
}

function searchKeyword(keyword: string) {
  searchQuery.value = keyword
  selectedTag.value = ''
}
</script>