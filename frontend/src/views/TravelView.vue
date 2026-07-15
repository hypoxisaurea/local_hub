<!-- frontend/src/views/TravelView.vue -->

<template>
  <LocalListPage
    title="어디로 떠나볼까요?"
    placeholder="서울에서 가고 싶은 곳을 검색하세요"
    :search-query="searchQuery"
    :selected-tag="selectedTag"
    :recommended-tags="recommendedTags"
    :items="filteredPlaces"
    ai-description="지금 당신의 취향에 딱 맞는 여행지를 추천해드려요!"
    @update:search-query="searchQuery = $event"
    @search="searchPlaces"
    @tag-click="toggleTag"
    @keyword-click="searchKeyword"
    @recommend="recommendTravel"
  />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import LocalListPage from '../components/LocalListPage.vue'
import type { LocalPlace } from '../types/local'

const searchQuery = ref('')
const selectedTag = ref('')

const recommendedTags = ['#힐링', '#핫플', '#역사문화', '#액티비티']

const places: LocalPlace[] = [
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

const filteredPlaces = computed(() => {
  const query = searchQuery.value.toLowerCase().replace('#', '')
  const tag = selectedTag.value.replace('#', '')

  return places.filter((place) => {
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
  console.log('여행지 검색:', searchQuery.value)
}

function toggleTag(tag: string) {
  selectedTag.value = selectedTag.value === tag ? '' : tag
}

function searchKeyword(keyword: string) {
  searchQuery.value = keyword
  selectedTag.value = ''
}

function recommendTravel() {
  const firstPlace = filteredPlaces.value[0]

  if (!firstPlace) {
    console.log('추천할 여행지가 없습니다.')
    return
  }

  console.log('추천 여행지:', firstPlace.title)
}
</script>