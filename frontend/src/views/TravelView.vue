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
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import LocalListPage from '../components/LocalListPage.vue'
import type { LocalPlace } from '../types/local'

const { locale, t } = useI18n()
const searchQuery = ref('')
const selectedTag = ref('')
const placeItems = ref<LocalPlace[]>([])

interface PlaceRow {
  contentid: string
  firstimage?: string | null
  title: string
  addr1?: string | null
}

const recommendedTags = computed(() =>
  locale.value === 'ko'
    ? ['#힐링', '#핫플', '#역사문화', '#액티비티']
    : ['#Healing', '#Hotspots', '#History', '#Activities']
)

// 2. computed 대신 데이터를 직접 쓸 수 있는 ref 변수로 변경
const places = ref<LocalPlace[]>([])

const filteredPlaces = computed(() => {
  const query = searchQuery.value.toLowerCase().replace('#', '')
  const tag = selectedTag.value.replace('#', '')

  return placeItems.value.filter((place) => {
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

async function fetchPlace() {
  try {
    const res = await fetch('/api/travel-spots')
    if (!res.ok) throw new Error('failed to load places')

    const rows: PlaceRow[] = await res.json()
    places.value = rows.map((row, index) => ({
      id: Number(row.contentid) || index + 1,
      title: row.title || '제목 없음',
      location: row.addr1 || '서울',
      tags: ['#관광지', '#문화', '#장소'],
      image: row.firstimage || '/images/default-festival.jpg',
    }))
  } catch (error) {
    console.error('Failed to load places from DB', error)
    places.value = []
  }
}

// 3. 컴포넌트 로드 시 자동으로 API를 호출하도록 onMounted 추가
onMounted(() => {
  fetchPlace()
})

function searchPlaces() {
  fetchPlaces()
}

function toggleTag(tag: string) {
  selectedTag.value = selectedTag.value === tag ? '' : tag
}

function searchKeyword(keyword: string) {
  searchQuery.value = keyword
  selectedTag.value = ''
  fetchPlaces()
}
</script>
