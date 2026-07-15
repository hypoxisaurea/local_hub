<template>
  <section class="w-full flex-1 flex flex-col animate-fadeIn">
    
    <!-- Hero Banner with Background Image -->
    <div
      class="relative py-12 lg:py-24 px-6 lg:px-16 overflow-hidden"
      :style="{
        backgroundImage: 'url(/banners/banner.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }"
    >
      
      <!-- Content -->
      <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
        
        <!-- Left Hero Column -->
        <div class="lg:col-span-7 space-y-6">
          <!-- Main Title (텍스트색 변경) -->
          <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-slate-900 leading-loose">
            {{ t('home.titlePrefix') }} <br class="hidden sm:inline">
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-rose-300 to-pink-300 leading-normal">{{ t('home.titleHighlight') }}</span>
          </h1>
          
          <!-- Description (텍스트색 변경) -->
          <p class="text-slate-700 text-sm sm:text-base max-w-xl font-medium leading-relaxed">
            {{ t('home.subtitleLine1') }} <br>
            {{ t('home.subtitleLine2') }}
          </p>

          <!-- Hero Search Bar -->
          <div class="max-w-lg bg-white/95 backdrop-blur-sm p-2 rounded-2xl shadow-xl shadow-slate-900/20 border border-white/30 flex items-center space-x-2">
            <i class="fas fa-magnifying-glass text-slate-400 ml-3"></i>
            <input 
              v-model="searchQuery" 
              @keyup.enter="runSearch"
              type="text" 
              :placeholder="t('home.searchPlaceholder')" 
              class="flex-1 bg-transparent border-none text-sm text-slate-800 placeholder-slate-400 focus:outline-none"
            >
            <button @click="runSearch" class="bg-rose-500 hover:bg-rose-600 text-white px-5 py-2.5 rounded-xl text-xs font-bold shadow-md shadow-rose-100 transition-all">
              {{ t('common.search') }}
            </button>
          </div>

          <!-- Trending Hashtags -->
          <div class="flex flex-wrap gap-2 pt-2 text-xs">
            <span class="text-slate-900 font-semibold self-center">{{ t('home.recommendedSearches') }}</span>
            <button
              v-for="tag in homeTags"
              :key="tag"
              @click="applyTag(tag)"
              class="bg-slate-100 hover:bg-slate-200 text-slate-900 hover:text-slate-900 border border-slate-200 px-3 py-1.5 rounded-full font-medium shadow-sm transition-all backdrop-blur-sm"
            >
              {{ tag }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Map & Content Section -->
    <div class="max-w-7xl mx-auto mt-20 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative gap-8">
      
      <!-- Left: Map Area (추후 지도 연동) -->
      <div class="lg:col-span-8">
        <div class="relative min-h-[600px] overflow-hidden rounded-2xl border border-slate-200 bg-slate-100 shadow-sm">
          <div ref="mapContainer" class="absolute inset-0 z-0"></div>

          <div class="absolute left-4 right-4 top-4 z-[400] flex flex-col gap-3 sm:left-6 sm:right-6 sm:flex-row sm:items-center sm:justify-between">
            <div class="rounded-2xl border border-white/70 bg-white/90 px-5 py-4 shadow-lg shadow-slate-900/10 backdrop-blur-md">
              <p class="text-xs font-bold uppercase tracking-wide text-rose-500">Seoul Travel Map</p>
              <h3 class="mt-1 text-xl font-extrabold text-slate-800">{{ t('home.mapTitle') }}</h3>
              <p class="mt-1 text-sm text-slate-500">
                {{ mapStatusText }}
              </p>
            </div>

            <div class="flex flex-wrap gap-2 rounded-2xl border border-white/70 bg-white/90 p-2 shadow-lg shadow-slate-900/10 backdrop-blur-md">
              <button
                v-for="category in mapCategories"
                :key="category.value"
                type="button"
                @click="selectMapCategory(category.value)"
                :class="[
                  'rounded-xl px-3 py-2 text-xs font-bold transition-all',
                  selectedMapCategory === category.value
                    ? 'bg-rose-500 text-white shadow-md shadow-rose-100'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                ]"
              >
                {{ category.label }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Sidebar Widgets -->
      <div class="lg:col-span-4 space-y-6">
        <!-- Weather Widget -->
        <div class="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm">
          <h4 class="font-bold text-slate-800 mb-3 flex items-center">
            <i class="fas fa-cloud-sun text-yellow-500 mr-2"></i> {{ t('home.weatherTitle') }}
          </h4>
          <p class="text-slate-500 text-sm">{{ t('home.weatherText') }}</p>
        </div>

        <!-- Chatbot Card -->
        <div @click="ui.toggleChat()" class="bg-gradient-to-br from-rose-500 to-pink-600 rounded-2xl p-6 text-white cursor-pointer hover:shadow-lg shadow-md shadow-rose-100 transition-all">
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-bold">LocalHub AI</h4>
            <i class="fas fa-robot text-xl"></i>
          </div>
          <p class="text-sm text-rose-50">{{ t('home.chatbot') }}</p>
        </div>

        <!-- Notices Widget -->
        <div class="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm">
          <h4 class="font-bold text-slate-800 mb-3 flex items-center">
            <i class="fas fa-bullhorn text-blue-500 mr-2"></i> {{ t('home.noticesTitle') }}
          </h4>
          <ul class="space-y-2">
            <li class="text-xs text-slate-600 pb-2 border-b border-slate-100">
              <span class="font-semibold text-slate-800">{{ t('home.noticeRule') }}</span>
              <p class="text-slate-400 mt-1">{{ t('home.noticeRuleDate') }}</p>
            </li>
            <li class="text-xs text-slate-600">
              <span class="font-semibold text-slate-800">{{ t('home.noticeMaintenance') }}</span>
              <p class="text-slate-400 mt-1">{{ t('home.noticeMaintenanceDate') }}</p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { usePortalStore } from '@/stores/portalStore'
import { useUIStore } from '@/stores/uiStore'

const portal = usePortalStore()
const ui = useUIStore()
const { t } = useI18n()

const searchQuery = ref('')
const mapContainer = ref<HTMLDivElement | null>(null)
let homeMap: L.Map | null = null
let markerLayer: L.LayerGroup | null = null

interface MapSpot {
  id: number
  contentid?: string | null
  category: string
  title: string
  addr1?: string | null
  mapx: string
  mapy: string
  firstimage?: string | null
  contentType?: string | null
}

const mapCategories = computed(() => [
  { label: t('categories.all'), value: 'all' },
  { label: t('categories.travel'), value: '관광지' },
  { label: t('categories.leports'), value: '레포츠' },
  { label: t('categories.restaurant'), value: '맛집' },
  { label: t('categories.culture'), value: '문화시설' },
  { label: t('categories.shopping'), value: '쇼핑' },
  { label: t('categories.festival'), value: '축제' },
])

const selectedMapCategory = ref('all')
const mapSpots = ref<MapSpot[]>([])
const isMapLoading = ref(false)
const mapError = ref('')
const seoulBounds = L.latLngBounds(
  [37.4133, 126.7341],
  [37.7151, 127.2693],
)

const mapStatusText = computed(() => {
  if (isMapLoading.value) return t('home.mapLoading')
  if (mapError.value) return mapError.value
  const categoryLabel = mapCategories.value.find((category) => category.value === selectedMapCategory.value)?.label ?? t('categories.all')
  return t('home.mapStatus', { category: categoryLabel, count: mapSpots.value.length })
})

const homeTags = computed(() => [
  t('home.tags.0'),
  t('home.tags.1'),
  t('home.tags.2'),
  t('home.tags.3'),
])

const runSearch = () => {
  portal.searchQuery = searchQuery.value
  if (searchQuery.value.trim()) {
    ui.showToast(t('toast.searchApplied', { query: searchQuery.value }))
  }
}

const applyTag = (tag: string) => {
  const cleaned = tag.replace('#', '').trim()
  searchQuery.value = cleaned
  portal.searchQuery = cleaned
  portal.selectedCategory = '전체'
}

const selectMapCategory = (category: string) => {
  selectedMapCategory.value = category
}

const getCategoryColor = (category: string) => {
  const colors: Record<string, string> = {
    관광지: '#f43f5e',
    레포츠: '#0ea5e9',
    맛집: '#f97316',
    문화시설: '#8b5cf6',
    쇼핑: '#10b981',
    축제: '#ec4899',
  }

  return colors[category] ?? '#64748b'
}

const createMapPinIcon = (category: string) => {
  const color = getCategoryColor(category)

  return L.divIcon({
    className: 'localhub-map-pin',
    iconSize: [26, 34],
    iconAnchor: [13, 34],
    popupAnchor: [0, -30],
    html: `
      <div style="
        width: 26px;
        height: 26px;
        border-radius: 50% 50% 50% 0;
        background: ${color};
        border: 3px solid white;
        box-shadow: 0 10px 18px rgba(15, 23, 42, 0.25);
        transform: rotate(-45deg);
      ">
        <div style="
          width: 8px;
          height: 8px;
          margin: 6px;
          border-radius: 9999px;
          background: white;
          opacity: 0.9;
        "></div>
      </div>
    `,
  })
}

const getValidCoordinates = (spot: MapSpot) => {
  const lng = Number(spot.mapx)
  const lat = Number(spot.mapy)

  if (!Number.isFinite(lat) || !Number.isFinite(lng)) return null
  if (!seoulBounds.contains([lat, lng])) return null

  return { lat, lng }
}

const escapeHtml = (value: string | null | undefined) =>
  String(value ?? '').replace(/[&<>"']/g, (char) => {
    const entities: Record<string, string> = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;',
    }

    return entities[char] ?? char
  })

const renderMapSpots = () => {
  if (!homeMap || !markerLayer) return

  markerLayer.clearLayers()
  const bounds = L.latLngBounds([])

  mapSpots.value.forEach((spot) => {
    const coordinates = getValidCoordinates(spot)
    if (!coordinates) return

    const marker = L.marker([coordinates.lat, coordinates.lng], {
      icon: createMapPinIcon(spot.category),
    }).bindPopup(`
      <strong>${escapeHtml(spot.title)}</strong><br>
      <span>${escapeHtml(spot.category)}</span><br>
      <span>${escapeHtml(spot.addr1)}</span>
    `)

    marker.addTo(markerLayer!)
    bounds.extend([coordinates.lat, coordinates.lng])
  })

  if (bounds.isValid()) {
    homeMap.fitBounds(bounds, {
      padding: [40, 40],
      maxZoom: selectedMapCategory.value === 'all' ? 12 : 15,
    })
  } else {
    homeMap.fitBounds(seoulBounds, {
      padding: [24, 24],
      maxZoom: 11,
    })
  }
}

const fetchMapSpots = async () => {
  isMapLoading.value = true
  mapError.value = ''

  try {
    const params = new URLSearchParams({
      category: selectedMapCategory.value,
      limit: selectedMapCategory.value === 'all' ? '600' : '300',
    })

    if (searchQuery.value.trim()) {
      params.set('q', searchQuery.value.trim())
    }

    const response = await fetch(`/api/map-spots?${params.toString()}`)
    if (!response.ok) throw new Error(t('home.mapError'))

    mapSpots.value = await response.json()
    renderMapSpots()
  } catch (error) {
    mapSpots.value = []
    renderMapSpots()
    mapError.value = error instanceof Error ? error.message : t('home.mapError')
  } finally {
    isMapLoading.value = false
  }
}

onMounted(async () => {
  await nextTick()

  if (!mapContainer.value || homeMap) return

  homeMap = L.map(mapContainer.value, {
    center: [37.5665, 126.978],
    zoom: 11,
    minZoom: 11,
    maxBounds: seoulBounds,
    maxBoundsViscosity: 1,
    zoomControl: false,
    scrollWheelZoom: true,
    worldCopyJump: false,
  })

  L.control.zoom({ position: 'bottomright' }).addTo(homeMap)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    minZoom: 11,
    maxZoom: 19,
    bounds: seoulBounds.pad(0.15),
  }).addTo(homeMap)

  L.rectangle(seoulBounds, {
    color: '#f43f5e',
    weight: 2,
    opacity: 0.7,
    fillOpacity: 0,
    interactive: false,
  }).addTo(homeMap)

  markerLayer = L.layerGroup().addTo(homeMap)
  homeMap.fitBounds(seoulBounds, {
    padding: [24, 24],
    maxZoom: 11,
  })
  fetchMapSpots()
})

watch(selectedMapCategory, () => {
  fetchMapSpots()
})

onBeforeUnmount(() => {
  markerLayer?.clearLayers()
  markerLayer = null
  homeMap?.remove()
  homeMap = null
})
</script>
