<!-- frontend/src/views/TravelView.vue -->

<template>
  <LocalListPage
    :title="t('list.travelTitle')"
    :placeholder="t('list.travelPlaceholder')"
    :search-query="searchQuery"
    :selected-tag="selectedTag"
    :recommended-tags="recommendedTags"
    :items="filteredPlaces"
    @update:search-query="searchQuery = $event"
    @search="searchPlaces"
    @tag-click="toggleTag"
    @keyword-click="searchKeyword"
  />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import LocalListPage from '../components/LocalListPage.vue'
import type { LocalPlace } from '../types/local'

const { locale, t } = useI18n()
const searchQuery = ref('')
const selectedTag = ref('')

const recommendedTags = computed(() =>
  locale.value === 'ko'
    ? ['#힐링', '#핫플', '#역사문화', '#액티비티']
    : ['#Healing', '#Hotspots', '#History', '#Activities']
)

const places = computed<LocalPlace[]>(() => locale.value === 'ko'
  ? [
      {
        id: 1,
        title: '경복궁 야간개장',
        location: '서울특별시 종로구',
        tags: ['#서울야경', '#데이트코스', '#역사문화'],
        image: '/images/gyeongbokgung.jpg',
      },
      {
        id: 2,
        title: '성수동 팝업스토어',
        location: '서울특별시 성동구',
        tags: ['#서울', '#요즘뜨는곳', '#핫플'],
        image: '/images/seongsu.jpg',
      },
      {
        id: 3,
        title: '한강 피크닉',
        location: '서울특별시 영등포구',
        tags: ['#공원', '#힐링', '#액티비티'],
        image: '/images/hangang.jpg',
      },
      {
        id: 4,
        title: '을지로 노가리 골목',
        location: '서울특별시 중구',
        tags: ['#맛집', '#로컬감성', '#핫플'],
        image: '/images/euljiro.jpg',
      },
    ]
  : [
      {
        id: 1,
        title: 'Gyeongbokgung Night Opening',
        location: 'Jongno-gu, Seoul',
        tags: ['#SeoulNightView', '#DateCourse', '#History'],
        image: '/images/gyeongbokgung.jpg',
      },
      {
        id: 2,
        title: 'Seongsu Popup Stores',
        location: 'Seongdong-gu, Seoul',
        tags: ['#Seoul', '#Trending', '#Hotspots'],
        image: '/images/seongsu.jpg',
      },
      {
        id: 3,
        title: 'Hangang Picnic',
        location: 'Yeongdeungpo-gu, Seoul',
        tags: ['#Park', '#Healing', '#Activities'],
        image: '/images/hangang.jpg',
      },
      {
        id: 4,
        title: 'Euljiro Nogari Alley',
        location: 'Jung-gu, Seoul',
        tags: ['#Restaurants', '#LocalMood', '#Hotspots'],
        image: '/images/euljiro.jpg',
      },
    ])

const filteredPlaces = computed(() => {
  const query = searchQuery.value.toLowerCase().replace('#', '')
  const tag = selectedTag.value.replace('#', '')

  return places.value.filter((place) => {
    const searchableText = [
      place.title,
      place.location,
      ...place.tags,
    ]
      .join(' ')
      .toLowerCase()
      .replaceAll('#', '')

    const matchesQuery = !query || searchableText.includes(query)
    const matchesTag = !tag || searchableText.includes(tag)

    return matchesQuery && matchesTag
  })
})

function searchPlaces() {
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
