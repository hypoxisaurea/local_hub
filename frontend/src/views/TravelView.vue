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

const recommendedTags = computed(() =>
  locale.value === 'ko'
    ? ['#힐링', '#핫플', '#역사문화', '#액티비티']
    : ['#Healing', '#Hotspots', '#History', '#Activities']
)

interface TravelSpotResponse {
  contentid: string
  firstimage?: string | null
  title: string
  addr1?: string | null
}

const toLocalPlace = (item: TravelSpotResponse, index: number): LocalPlace => ({
  id: Number(item.contentid) || index,
  title: item.title,
  location: item.addr1 || '',
  tags: [locale.value === 'ko' ? '#관광지' : '#Attractions'],
  image: item.firstimage || '/banners/banner.png',
})

const fetchPlaces = async () => {
  const params = new URLSearchParams({ lang: locale.value })
  if (searchQuery.value.trim()) {
    params.set('q', searchQuery.value.trim())
  }

  const response = await fetch(`/api/travel-spots-simple/attractions?${params.toString()}`)
  if (!response.ok) {
    placeItems.value = []
    return
  }

  const data = await response.json() as TravelSpotResponse[]
  placeItems.value = data.map(toLocalPlace)
}

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

watch(locale, () => {
  selectedTag.value = ''
  fetchPlaces()
})

onMounted(fetchPlaces)
</script>
