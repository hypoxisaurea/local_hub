<template>
  <section class="local-page">
    <div class="local-container">
      <section class="search-panel">
        <h1>{{ title }}</h1>

        <form class="search-form" @submit.prevent="emit('search')">
          <i class="fa-solid fa-magnifying-glass"></i>

          <input
            :value="searchQuery"
            type="search"
            :placeholder="placeholder"
            @input="updateSearchQuery"
          />

          <button type="submit">{{ t('common.search') }}</button>
        </form>
      </section>

      <div class="local-content">
        <section class="place-section">
          <div v-if="items.length" class="place-grid">
            <article v-for="item in items" :key="item.id" class="place-card">
              <img :src="item.image" :alt="item.title" class="place-image" />

              <div class="place-info">
                <h2>{{ item.title }}</h2>
                <p>{{ item.location }}</p>

                <div class="place-tags">
                  <span v-for="tag in item.tags" :key="tag">
                    {{ tag }}
                  </span>
                </div>
              </div>
            </article>
          </div>
          <div v-else class="empty-state">
            <p>{{ t('common.noResults') }}</p>
          </div>
        </section>
          <div v-if="items.length > 0" class="pagination-container">
            <button
              class="page-nav-btn"
              :disabled="currentPage === 1"
              @click="emit('page-change', currentPage - 1)"
            >
              {{ t('common.previous') }}
            </button>

            <button
              v-for="page in pageNumbers"
              :key="page"
              class="page-number-btn"
              :class="{ 'active': currentPage === page }"
              @click="emit('page-change', page)"
            >
              {{ page }}
            </button>

            <button
              class="page-nav-btn"
              :disabled="currentPage === totalPages"
              @click="emit('page-change', currentPage + 1)"
            >
              {{ t('common.next') }}
            </button>
          </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import type { LocalPlace } from '@/types/local'

const { t } = useI18n()

defineProps<{
  title: string
  placeholder: string
  searchQuery: string
  selectedTag: string
  items: LocalPlace[]
  aiDescription?: string
  currentPage: number
  pageNumbers: number[]
  totalPages: number
}>()

const emit = defineEmits<{
  search: []
  'update:search-query': [value: string]
  'tag-click': [tag: string]
  recommend: []
  'page-change': [page: number]
}>()

function updateSearchQuery(event: Event) {
  const input = event.target as HTMLInputElement
  emit('update:search-query', input.value)
}
</script>

<style scoped>
.local-page {
  min-height: 100vh;
  padding: 110px 24px 72px;
  background: #f8fafc;
  color: #17253d;
}

.local-container {
  max-width: 1120px;
  margin: 0 auto;
}

.search-panel,
.place-card,
.popular-card {
  border: 1px solid #edf0f4;
  border-radius: 26px;
  background: white;
}

.search-panel {
  padding: 32px;
}

.search-panel h1 {
  margin: 0 0 18px;
  font-size: 2rem;
  font-weight: 800;
}

.search-form {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 58px;
  padding: 6px 7px 6px 20px;
  border: 1px solid #dfe4eb;
  border-radius: 999px;
}

.search-form input {
  flex: 1;
  min-width: 0;
  border: 0;
  outline: 0;
  font: inherit;
}

.search-form button {
  min-width: 78px;
  min-height: 40px;
  border: 0;
  border-radius: 999px;
  background: #ed3e94;
  color: white;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 24px;
}

.tag-list button {
  padding: 9px 16px;
  border: 0;
  border-radius: 999px;
  background: #f3f5f8;
  cursor: pointer;
}

.tag-list button.active {
  background: #ed3e94;
  color: white;
}

.local-content {
  margin-top: 30px;
}

.place-section {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
}

.place-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 16px;
}

.place-card {
  width: auto;
  max-width: none;
  overflow: hidden;
}

.place-image {
  width: 100%;
  height: auto;
  aspect-ratio: 1 / 1;
  background: #f1f3f6;
}

.place-info {
  padding: 17px 15px 16px;
}

.place-info h2 {
  margin: 0 0 6px;
  font-size: 1.12rem;
}

.place-info p {
  margin: 0;
  color: #69758a;
  font-size: 0.86rem;
}

.place-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 12px;
}

.place-tags span {
  color: #ed3e94;
  font-size: 0.78rem;
}

.sidebar {
  display: grid;
  gap: 16px;

  align-self: start;
  align-content: start;
}

.empty-state {
  display: grid;
  min-height: 300px;
  place-content: center;
  border: 1px dashed #cdd5df;
  border-radius: 24px;
  color: #78869a;
}

.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 40px;
  padding: 20px 0;
}

/* 이전/다음 버튼 */
.page-nav-btn {
  padding: 8px 16px;
  border: 1px solid #dfe4eb;
  border-radius: 12px;
  background: white;
  color: #69758a;
  font-weight: bold;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

/* 숫자 버튼 */
.page-number-btn {
  width: 40px;
  height: 40px;
  border: 1px solid #dfe4eb;
  border-radius: 12px;
  background: white;
  color: #69758a;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

/* 활성화된 버튼 */
.page-number-btn.active {
  background: #ed3e94;
  border-color: #ed3e94;
  color: white;
}

/* 호버 효과 */
.page-nav-btn:hover:not(:disabled),
.page-number-btn:hover:not(.active) {
  background: #f8fafc;
  border-color: #cdd5df;
}

/* 비활성화 상태 */
.page-nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

@media (max-width: 820px) {
  .local-content {
    grid-template-columns: 1fr;
  }

  .sidebar {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 1000px) {
  .place-grid {
    grid-template-columns: repeat(3, 180px);
  }
}

@media (max-width: 650px) {
  .place-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }
}

@media (max-width: 560px) {
  .local-page {
    padding: 84px 16px 48px;
  }

  .search-panel {
    padding: 24px 18px;
  }
  .place-card {
    width: 100%;
    max-width: 100%;
  }
}
</style>
