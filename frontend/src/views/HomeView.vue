<template>
  <section class="flex flex-col flex-1 w-full animate-fadeIn">
    <!-- Hero Banner with Background Image -->
    <div
      class="relative min-h-[clamp(420px,53vw,720px)] py-12 lg:py-24 px-6 lg:px-16 overflow-hidden bg-white"
      :style="{
        backgroundImage: 'url(/banners/banner.png)',
        backgroundSize: 'contain',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
      }"
    >
      <!-- Content -->
      <div
        class="relative z-10 grid items-center grid-cols-1 pt-8 mx-auto gap-15 max-w-7xl lg:grid-cols-12 lg:pt-12"
      >
        <!-- Left Hero Column -->
        <div class="lg:col-span-7">
          <!-- Main Title (텍스트색 변경) -->
          <h1
            class="text-3xl font-extrabold leading-loose tracking-tight sm:text-4xl lg:text-5xl text-slate-900"
          >
            {{ t("home.titlePrefix") }} <br class="hidden sm:inline" />
            <span
              class="leading-normal text-transparent bg-clip-text bg-gradient-to-r from-rose-300 to-pink-300"
              >{{ t("home.titleHighlight") }}</span
            >
          </h1>

          <!-- Description (텍스트색 변경) -->
          <p
            class="max-w-xl mt-6 text-sm font-medium leading-relaxed text-slate-700 sm:text-base"
          >
            {{ t("home.subtitleLine1") }} <br />
            {{ t("home.subtitleLine2") }}
          </p>

          <!-- Hero Search Bar -->
          <div
            class="flex items-center max-w-lg p-2 space-x-2 border shadow-xl mt-[70px] bg-white/95 backdrop-blur-sm rounded-2xl shadow-slate-900/20 border-white/30"
          >
            <i class="ml-3 fas fa-magnifying-glass text-slate-400"></i>
            <input
              v-model="searchQuery"
              @keyup.enter="runSearch"
              type="text"
              :placeholder="t('home.searchPlaceholder')"
              class="flex-1 text-sm bg-transparent border-none text-slate-800 placeholder-slate-400 focus:outline-none"
            />
            <button
              @click="runSearch"
              class="bg-rose-500 hover:bg-rose-600 text-white px-5 py-2.5 rounded-xl text-xs font-bold shadow-md shadow-rose-100 transition-all"
            >
              {{ t("common.search") }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Map & Content Section -->
    <div
      class="relative grid items-start grid-cols-1 gap-8 mx-auto mt-20 max-w-7xl lg:grid-cols-12"
    >
      <!-- Left: Map Area -->
      <div class="lg:col-span-8">
        <div
          class="relative min-h-[600px] overflow-hidden rounded-2xl border border-slate-200 bg-slate-100 shadow-sm"
        >
          <div ref="mapContainer" class="absolute inset-0 z-0"></div>

          <div
            class="absolute left-4 right-4 top-4 z-[400] flex flex-col gap-3 sm:left-6 sm:right-6 sm:flex-row sm:items-start sm:justify-between"
          >
            <div
              class="px-5 py-4 border shadow-lg rounded-2xl border-white/70 bg-white/90 shadow-slate-900/10 backdrop-blur-md"
            >
              <p
                class="text-xs font-bold tracking-wide uppercase text-rose-500"
              >
                Seoul Travel Map
              </p>
              <h3 class="mt-1 text-xl font-extrabold text-slate-800">
                {{ t("home.mapTitle") }}
              </h3>
              <p class="mt-1 text-sm text-slate-500">
                {{ mapStatusText }}
              </p>
            </div>

            <div
              class="ml-auto flex w-fit max-w-full flex-wrap justify-end gap-2 p-2 border shadow-lg rounded-2xl shadow-slate-900/10 backdrop-blur-md sm:w-[25rem]"
            >
              <button
                v-for="category in mapCategories"
                :key="category.value"
                type="button"
                @click="selectMapCategory(category.value)"
                :class="[
                  'min-w-0 basis-[calc((100%_-_1.5rem)/3)] whitespace-nowrap rounded-xl px-3 py-2 text-center text-xs font-bold transition-all',
                  selectedMapCategory === category.value
                    ? 'bg-rose-500 text-white shadow-md shadow-rose-100'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200',
                ]"
              >
                {{ category.label }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Sidebar Widgets -->
      <div class="space-y-6 lg:col-span-4">
        <!-- Weather Widget -->
        <div class="p-6 bg-white border shadow-sm rounded-2xl border-slate-100">
          <h4 class="flex items-center mb-1 font-bold text-slate-800">
            <i :class="[getWeatherIcon(weather?.condition), 'mr-2']"></i>
            {{ t("home.weatherTitle") }}
          </h4>
          
          <div v-if="weather" class="mt-3 space-y-2 transition-all duration-300">
            <div class="flex justify-between items-baseline gap-2">
              <span class="text-3xl font-extrabold tracking-tight text-slate-900">
                {{ weather.temp }}°C
              </span>
              <span class="text-sm font-medium text-slate-500 right-5">
                {{ weather.condition }}
              </span>
            </div>
          </div>

          <div v-else class="py-4 mt-2 text-sm animate-pulse text-slate-400">
            {{ t("home.weatherText") }}...
          </div>
        </div>

        <!-- Chatbot Card -->
        <div
          @click="ui.toggleChat()"
          class="p-6 text-white transition-all shadow-md cursor-pointer bg-gradient-to-br from-rose-500 to-pink-600 rounded-2xl hover:shadow-lg shadow-rose-100"
        >
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-bold">LocalHub AI</h4>
            <i class="text-xl fas fa-robot"></i>
          </div>
          <p class="text-sm text-rose-50">{{ t("home.chatbot") }}</p>
        </div>

        <!-- Notices Widget -->
        <div class="p-6 bg-white border shadow-sm rounded-2xl border-slate-100">
          <h4 class="flex items-center mb-3 font-bold text-slate-800">
            <i class="mr-2 text-blue-500 fas fa-bullhorn"></i>
            {{ t("home.noticesTitle") }}
          </h4>
          <ul class="space-y-2">
            <li class="pb-2 text-xs border-b text-slate-600 border-slate-100">
              <span class="font-semibold text-slate-800">{{
                t("home.noticeRule")
              }}</span>
              <p class="mt-1 text-slate-400">{{ t("home.noticeRuleDate") }}</p>
            </li>
            <li class="text-xs text-slate-600">
              <span class="font-semibold text-slate-800">{{
                t("home.noticeMaintenance")
              }}</span>
              <p class="mt-1 text-slate-400">
                {{ t("home.noticeMaintenanceDate") }}
              </p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import {
  computed,
  nextTick,
  onBeforeUnmount,
  onMounted,
  onUnmounted,
  ref,
  watch,
} from "vue";

// ---------------------------------------------------
// 날씨 부분 스크립트 추가
interface WeatherUpdate {
  temp: number | string
  condition: string
}

const weather = ref<WeatherUpdate | null>(null)
const isConnected = ref(false)
let eventSource: EventSource | null = null

const getWeatherIcon = (condition?: string | null) => {
  if (!condition) return 'fas fa-spinner fa-spin text-slate-400' // 로딩 중 일때
  
  const cond = condition.toLowerCase()
  if (cond.includes('sun') || cond.includes('clear') || condition.includes('맑')) return 'fas fa-sun text-yellow-500'
  if (cond.includes('cloud') || condition.includes('구름') || condition.includes('흐림')) return 'fas fa-cloud text-slate-400'
  if (cond.includes('rain') || condition.includes('비')) return 'fas fa-cloud-showers-heavy text-blue-400'
  if (cond.includes('snow') || condition.includes('눈')) return 'fas fa-snowflake text-sky-300'
  
  return 'fas fa-cloud-sun text-yellow-500' // 기본값
}

onMounted(() => {
  eventSource = new EventSource("/api/stream-weather")

  eventSource.onopen = () => {
    isConnected.value = true
    console.log("SSE connected.")
  }

  eventSource.addEventListener("weather_update", (event) => {
    try {
      const data = JSON.parse(event.data)
      weather.value = data
    } catch (error) {
      console.error("데이터 파싱 에러:", error)
    }
  })

  eventSource.onerror = (err) => {
    console.error("SSE connection error:", err)
    isConnected.value = false
  }
})

onUnmounted(() => {
  eventSource?.close()
})
// ----------------------------------------------------
import { useI18n } from "vue-i18n";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useRouter } from "vue-router";
import { usePortalStore } from "@/stores/portalStore";
import { useUIStore } from "@/stores/uiStore";

const portal = usePortalStore();
const ui = useUIStore();
const router = useRouter();
const { t } = useI18n();

const searchQuery = ref("");
const mapContainer = ref<HTMLDivElement | null>(null);
let homeMap: L.Map | null = null;
let markerLayer: L.LayerGroup | null = null;

interface MapSpot {
  id: number;
  contentid?: string | null;
  category: string;
  title: string;
  addr1?: string | null;
  mapx: string;
  mapy: string;
  firstimage?: string | null;
  contentType?: string | null;
}

const mapCategories = computed(() => [
  { label: t("categories.all"), value: "all" },
  { label: t("categories.travel"), value: "관광지" },
  { label: t("categories.leports"), value: "레포츠" },
  { label: t("categories.culture"), value: "문화시설" },
  { label: t("categories.shopping"), value: "쇼핑" },
  { label: t("categories.festival"), value: "축제" },
]);

const selectedMapCategory = ref("all");
const mapSpots = ref<MapSpot[]>([]);
const isMapLoading = ref(false);
const mapError = ref("");
const seoulBounds = L.latLngBounds([37.4133, 126.7341], [37.7151, 127.2693]);

const mapStatusText = computed(() => {
  if (isMapLoading.value) return t("home.mapLoading");
  if (mapError.value) return mapError.value;
  const categoryLabel =
    mapCategories.value.find(
      (category) => category.value === selectedMapCategory.value,
    )?.label ?? t("categories.all");
  return t("home.mapStatus", {
    category: categoryLabel,
    count: mapSpots.value.length,
  });
});

const homeTags = computed(() => [
  t("home.tags.0"),
  t("home.tags.1"),
  t("home.tags.2"),
  t("home.tags.3"),
]);

const runSearch = () => {
  const query = searchQuery.value.trim();
  portal.searchQuery = query;
  portal.selectedCategory = "전체";

  if (query) {
    ui.showToast(t("toast.searchApplied", { query }));
  }

  router.push({
    path: "/community",
    query: query ? { q: query } : undefined,
  });
};

const applyTag = (tag: string) => {
  const cleaned = tag.replace("#", "").trim();
  searchQuery.value = cleaned;
  portal.searchQuery = cleaned;
  portal.selectedCategory = "전체";
};

const selectMapCategory = (category: string) => {
  selectedMapCategory.value = category;
};

const getCategoryColor = (category: string) => {
  const colors: Record<string, string> = {
    관광지: "#f43f5e",
    레포츠: "#0ea5e9",
    맛집: "#f97316",
    문화시설: "#8b5cf6",
    쇼핑: "#10b981",
    축제: "#ec4899",
  };

  return colors[category] ?? "#64748b";
};

const createMapPinIcon = (category: string) => {
  const color = getCategoryColor(category);

  return L.divIcon({
    className: "localhub-map-pin",
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
  });
};

const getValidCoordinates = (spot: MapSpot) => {
  const lng = Number(spot.mapx);
  const lat = Number(spot.mapy);

  if (!Number.isFinite(lat) || !Number.isFinite(lng)) return null;
  if (!seoulBounds.contains([lat, lng])) return null;

  return { lat, lng };
};

const escapeHtml = (value: string | null | undefined) =>
  String(value ?? "").replace(/[&<>"']/g, (char) => {
    const entities: Record<string, string> = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    };

    return entities[char] ?? char;
  });

const renderMapSpots = () => {
  if (!homeMap || !markerLayer) return;

  markerLayer.clearLayers();
  const bounds = L.latLngBounds([]);

  mapSpots.value.forEach((spot) => {
    const coordinates = getValidCoordinates(spot);
    if (!coordinates) return;

    const popupCategory = spot.contentType || spot.category;
    const marker = L.marker([coordinates.lat, coordinates.lng], {
      icon: createMapPinIcon(spot.category),
    }).bindPopup(`
      <strong>${escapeHtml(spot.title)}</strong><br>
      <span>${escapeHtml(popupCategory)}</span><br>
      <span>${escapeHtml(spot.addr1)}</span>
    `);

    marker.addTo(markerLayer!);
    bounds.extend([coordinates.lat, coordinates.lng]);
  });

  if (bounds.isValid()) {
    homeMap.fitBounds(bounds, {
      padding: [40, 40],
      maxZoom: selectedMapCategory.value === "all" ? 12 : 15,
    });
  } else {
    homeMap.fitBounds(seoulBounds, {
      padding: [24, 24],
      maxZoom: 11,
    });
  }
};

const fetchMapSpots = async () => {
  isMapLoading.value = true;
  mapError.value = "";

  try {
    const params = new URLSearchParams({
      category: selectedMapCategory.value,
      lang: ui.currentLang,
      limit: selectedMapCategory.value === "all" ? "600" : "300",
    });

    if (searchQuery.value.trim()) {
      params.set("q", searchQuery.value.trim());
    }

    const response = await fetch(`/api/map-spots?${params.toString()}`);
    if (!response.ok) throw new Error(t("home.mapError"));

    mapSpots.value = await response.json();
    renderMapSpots();
  } catch (error) {
    mapSpots.value = [];
    renderMapSpots();
    mapError.value =
      error instanceof Error ? error.message : t("home.mapError");
  } finally {
    isMapLoading.value = false;
  }
};

onMounted(async () => {
  await nextTick();

  if (!mapContainer.value || homeMap) return;

  homeMap = L.map(mapContainer.value, {
    center: [37.5665, 126.978],
    zoom: 11,
    minZoom: 11,
    maxBounds: seoulBounds,
    maxBoundsViscosity: 1,
    zoomControl: false,
    scrollWheelZoom: true,
    worldCopyJump: false,
  });

  L.control.zoom({ position: "bottomright" }).addTo(homeMap);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    minZoom: 11,
    maxZoom: 19,
    bounds: seoulBounds.pad(0.15),
  }).addTo(homeMap);

  L.rectangle(seoulBounds, {
    color: "#f43f5e",
    weight: 2,
    opacity: 0.7,
    fillOpacity: 0,
    interactive: false,
  }).addTo(homeMap);

  markerLayer = L.layerGroup().addTo(homeMap);
  homeMap.fitBounds(seoulBounds, {
    padding: [24, 24],
    maxZoom: 11,
  });
  fetchMapSpots();
});

watch(selectedMapCategory, () => {
  fetchMapSpots();
});

watch(
  () => ui.currentLang,
  () => {
    fetchMapSpots();
  }
);

onBeforeUnmount(() => {
  markerLayer?.clearLayers();
  markerLayer = null;
  homeMap?.remove();
  homeMap = null;
});
</script>
