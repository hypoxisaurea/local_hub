<template>
  <LocalListPage
    :title="t('list.festivalTitle')"
    :placeholder="t('list.festivalPlaceholder')"
    :search-query="searchQuery"
    :selected-tag="selectedTag"
    :recommended-tags="recommendedTags"
    :items="filteredFestivals"
    @update:search-query="searchQuery = $event"
    @search="searchFestivals"
    @tag-click="toggleTag"
    @keyword-click="searchKeyword"
  />
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import LocalListPage from '@/components/LocalListPage.vue'
import type { LocalPlace } from '@/types/local'

interface FestivalRow {
  contentid: string
  firstimage?: string | null
  title: string
  addr1?: string | null
}

const { locale, t } = useI18n()
const searchQuery = ref('')
const selectedTag = ref('')
const festivals = ref<LocalPlace[]>([])

const recommendedTags = computed(() =>
  locale.value === 'ko'
    ? ['#야외행사', '#전시', '#공연', '#무료']
    : ['#Outdoor', '#Exhibition', '#Performance', '#Free']
)

const filteredFestivals = computed(() => {
  const query = searchQuery.value.toLowerCase().replace('#', '')
  const tag = selectedTag.value.replace('#', '')

  return festivals.value.filter((festival) => {
    const text = [festival.title, festival.location, ...festival.tags]
      .join(' ')
      .toLowerCase()
      .replaceAll('#', '')

    return (!query || text.includes(query)) && (!tag || text.includes(tag))
  })
})

async function fetchFestivals() {
  try {
    const res = await fetch('/api/travel-spots-simple/festivals')
    if (!res.ok) throw new Error('failed to load festivals')

    const rows: FestivalRow[] = await res.json()
    festivals.value = rows.map((row, index) => ({
      id: Number(row.contentid) || index + 1,
      title: row.title || '제목 없음',
      location: row.addr1 || '서울',
      tags: ['#축제', '#공연', '#행사'],
      image: row.firstimage || '/images/default-festival.jpg',
    }))
  } catch (error) {
    console.error('Failed to load festivals from DB', error)
    festivals.value = []
  }
}

onMounted(() => {
  fetchFestivals()
})

function searchFestivals() {
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
