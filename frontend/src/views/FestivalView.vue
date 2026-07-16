<template>
  <LocalListPage
    :title="t('list.festivalTitle')"
    :placeholder="t('list.festivalPlaceholder')"
    :search-query="searchQuery"
    :selected-tag="selectedTag"
    :items="paginatedPlaces"
    :current-page="currentPage"
    :page-numbers="pageNumbers"
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

interface TravelSpotResponse {
  contentid: string
  firstimage?: string | null
  title: string
  addr1?: string | null
}

const toFestivalPlace = (item: TravelSpotResponse, index: number): LocalPlace => ({
  id: Number(item.contentid) || index,
  title: item.title,
  location: item.addr1 || '',
  tags: [locale.value === 'ko' ? '#축제' : '#Festivals'],
  image: item.firstimage || '/banners/banner.png',
})

const fetchFestivals = async () => {
  const params = new URLSearchParams({ lang: locale.value })
  if (searchQuery.value.trim()) {
    params.set('q', searchQuery.value.trim())
  }

  const response = await fetch(`/api/travel-spots-simple/festivals?${params.toString()}`)
  if (!response.ok) {
    festivalItems.value = []
    return
  }

  const data = await response.json() as TravelSpotResponse[]
  festivalItems.value = data.map(toFestivalPlace)
}

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

function searchFestivals() {
  fetchFestivals()
}

function toggleTag(tag: string) {
  selectedTag.value = selectedTag.value === tag ? '' : tag
}

function searchKeyword(keyword: string) {
  searchQuery.value = keyword
  selectedTag.value = ''
  fetchFestivals()
}

watch(locale, () => {
  selectedTag.value = ''
  fetchFestivals()
})

onMounted(fetchFestivals)
</script>
