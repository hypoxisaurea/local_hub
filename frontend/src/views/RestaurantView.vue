<template>
  <FoodListPage
    title="어떤 맛집을 찾고 있나요?"
    placeholder="지역, 음식 종류, 분위기를 검색하세요"
    :search-query="searchQuery"
    :selected-tag="selectedTag"
    :recommended-tags="recommendedTags"
    :items="filteredRestaurants"
    ai-description="당신의 취향과 현재 위치에 맞는 맛집을 추천해드려요!"
    @update:search-query="searchQuery = $event"
    @search="searchRestaurants"
    @tag-click="toggleTag"
    @keyword-click="searchKeyword"
    @recommend="recommendRestaurant"
  />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import LocalListPage from '@/components/FoodListPage.vue'
import type { LocalPlace } from '@/types/local'

const searchQuery = ref('')
const selectedTag = ref('')

const recommendedTags = ['#한식', '#카페', '#혼밥', '#데이트']

const restaurants: LocalPlace[] = [
  {
    id: 1,
    title: '을지면옥',
    location: '서울특별시 중구',
    tags: ['#평양냉면', '#노포', '#한식'],
    image: '/images/euljimyeonok.jpg',
  },
  {
    id: 2,
    title: '성수 베이커리',
    location: '서울특별시 성동구',
    tags: ['#베이커리', '#카페', '#데이트'],
    image: '/images/seongsu-bakery.jpg',
  },
]

const filteredRestaurants = computed(() => {
  const query = searchQuery.value.toLowerCase().replace('#', '')
  const tag = selectedTag.value.replace('#', '')

  return restaurants.filter((restaurant) => {
    const text = [restaurant.title, restaurant.location, ...restaurant.tags]
      .join(' ')
      .toLowerCase()
      .replaceAll('#', '')

    return (!query || text.includes(query)) && (!tag || text.includes(tag))
  })
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

function recommendRestaurant() {
  console.log('맛집 추천 요청')
}
</script>