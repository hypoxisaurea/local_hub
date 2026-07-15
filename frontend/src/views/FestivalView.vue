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
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import LocalListPage from '@/components/LocalListPage.vue'
import type { LocalPlace } from '@/types/local'

const { locale, t } = useI18n()
const searchQuery = ref('')
const selectedTag = ref('')

const recommendedTags = computed(() =>
  locale.value === 'ko'
    ? ['#야외행사', '#전시', '#공연', '#무료']
    : ['#Outdoor', '#Exhibition', '#Performance', '#Free']
)

const festivals = computed<LocalPlace[]>(() => locale.value === 'ko'
  ? [
      {
        id: 1,
        title: '서울 재즈 페스티벌',
        location: '서울특별시 송파구',
        tags: ['#공연', '#야외행사', '#음악'],
        image: '/images/seoul-jazz.jpg',
      },
      {
        id: 2,
        title: '한강 불빛 축제',
        location: '서울특별시 영등포구',
        tags: ['#야경', '#무료', '#야외행사'],
        image: '/images/hangang-light.jpg',
      },
    ]
  : [
      {
        id: 1,
        title: 'Seoul Jazz Festival',
        location: 'Songpa-gu, Seoul',
        tags: ['#Performance', '#Outdoor', '#Music'],
        image: '/images/seoul-jazz.jpg',
      },
      {
        id: 2,
        title: 'Hangang Light Festival',
        location: 'Yeongdeungpo-gu, Seoul',
        tags: ['#NightView', '#Free', '#Outdoor'],
        image: '/images/hangang-light.jpg',
      },
    ])

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
