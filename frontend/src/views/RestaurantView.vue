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
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import FoodListPage from '@/components/FoodListPage.vue'
import type { LocalPlace } from '@/types/local'

const { locale, t } = useI18n()
const searchQuery = ref('')
const selectedTag = ref('')

const recommendedTags = computed(() =>
  locale.value === 'ko'
    ? ['#한식', '#카페', '#혼밥', '#데이트']
    : ['#KoreanFood', '#Cafe', '#SoloDining', '#Date']
)

const restaurants = computed<LocalPlace[]>(() => locale.value === 'ko'
  ? [
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
  : [
      {
        id: 1,
        title: 'Eulji Myeonok',
        location: 'Jung-gu, Seoul',
        tags: ['#PyongyangColdNoodles', '#OldFavorite', '#KoreanFood'],
        image: '/images/euljimyeonok.jpg',
      },
      {
        id: 2,
        title: 'Seongsu Bakery',
        location: 'Seongdong-gu, Seoul',
        tags: ['#Bakery', '#Cafe', '#Date'],
        image: '/images/seongsu-bakery.jpg',
      },
    ])

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
