<!-- frontend/src/views/TravelView.vue -->

<template>
  <LocalListPage
    :title="t('list.travelTitle')"
    :placeholder="t('list.travelPlaceholder')"
    :search-query="searchQuery"
    :selected-tag="selectedTag"
    :recommended-tags="recommendedTags"
    :items="paginatedPlaces"
    :current-page="currentPage"
    :page-numbers="pageNumbers"
    @page-change="movePage"
    @update:search-query="searchQuery = $event"
    @search="searchPlaces"
    @tag-click="toggleTag"
    @keyword-click="searchKeyword"
  />
</template>

<script setup lang="ts">
// 1. onMounted 임포트 추가
import { computed, ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import LocalListPage from '../components/LocalListPage.vue'
import type { LocalPlace } from '../types/local'

const { locale, t } = useI18n()
const searchQuery = ref('')
const selectedTag = ref('')

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

// --- 페이지네이션 로직 ---
const DISPLAY_PAGE_COUNT = 10;
const currentPage = ref(1)
const ITEMS_PER_PAGE = 10

const pageNumbers = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;

  // 전체 페이지가 10개 이하라면 모두 표시
  if (total <= DISPLAY_PAGE_COUNT) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }

  // 페이지 범위 계산
  let startPage = current - Math.floor(DISPLAY_PAGE_COUNT / 2);
  let endPage = current + Math.floor(DISPLAY_PAGE_COUNT / 2) - 1;

  // 앞쪽 보정
  if (startPage < 1) {
    startPage = 1;
    endPage = DISPLAY_PAGE_COUNT;
  }

  // 뒤쪽 보정
  if (endPage > total) {
    endPage = total;
    startPage = total - DISPLAY_PAGE_COUNT + 1;
  }

  return Array.from({ length: DISPLAY_PAGE_COUNT }, (_, i) => startPage + i);
});

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

const totalPages = computed(() => Math.max(1, Math.ceil(filteredPlaces.value.length / ITEMS_PER_PAGE)))

const paginatedPlaces = computed(() => {
  const start = (currentPage.value - 1) * ITEMS_PER_PAGE
  return filteredPlaces.value.slice(start, start + ITEMS_PER_PAGE)
})

// --- 페이지 조작 함수 ---
const movePage = (page: number) => {
  currentPage.value = Math.min(Math.max(page, 1), totalPages.value)
}

// 검색 시 페이지 초기화
function searchPlaces() {
  console.log(searchQuery.value)
  currentPage.value = 1
}

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

function toggleTag(tag: string) {
  selectedTag.value = selectedTag.value === tag ? '' : tag
}

function searchKeyword(keyword: string) {
  searchQuery.value = keyword
  selectedTag.value = ''
}
</script>