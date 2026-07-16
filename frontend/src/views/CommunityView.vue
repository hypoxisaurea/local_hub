<template>
  <section class="w-full flex-1 flex flex-col animate-fadeIn pt-28 pb-12">
    <div class="max-w-7xl mx-auto w-full px-4 lg:px-8">
      <!--- Community Banner -->
      <div class="relative mb-8 min-h-[112px] overflow-hidden rounded-2xl bg-rose-50 px-5 py-5 shadow-sm sm:min-h-[132px] sm:px-8">
        <div class="relative z-10 max-w-[72%] sm:max-w-xl">
          <div class="min-w-0 mr-6">
            <p class="text-lg font-black text-slate-900 sm:text-2xl">
              {{ pageTitle }}
            </p>

            <p class="mt-1 text-xs font-semibold text-slate-500 sm:text-sm">
              {{ pageSubtitle }}
            </p>
          </div>
        </div>

        <button
          type="button"
          class="absolute right-5 bottom-5 z-20 shrink-0 rounded-xl bg-rose-500 px-3 py-2 text-sm font-bold text-white shadow-md shadow-rose-100 transition-all hover:bg-rose-600 sm:right-8"
          @click="openWriteForm"
        >
          <i class="fas fa-pen mr-2"></i>
          {{ t('community.writeShort') }}
        </button>

        <img
          src="/banners/community_banner.png"
          alt=""
          class="pointer-events-none absolute bottom-0 right-0 h-[92px] w-auto object-contain sm:h-[126px]"
          aria-hidden="true"
        >
      </div>

      <!-- Category & Search Section -->
      <div class="space-y-6 mb-8">
        <!-- Category Buttons -->
        <div class="flex flex-wrap justify-center gap-3">
          <!-- 전체보기 버튼 -->
          <button 
            @click="selectCategory(ALL_CATEGORY)"
            :class="[
              'w-40 p-4 rounded-2xl flex flex-col items-center justify-center border transition-all hover:shadow-md',
              portal.selectedCategory === ALL_CATEGORY 
                ? 'bg-rose-500 text-white border-rose-500 shadow-md shadow-rose-100' 
                : 'bg-white text-slate-600 border-slate-100'
            ]"
          >
            <div :class="['w-10 h-10 rounded-xl flex items-center justify-center mb-2', portal.selectedCategory === ALL_CATEGORY ? 'bg-rose-400 text-white' : 'bg-slate-50']">
              <i class="fas fa-grid-2 text-lg"></i>
            </div>
            <span class="text-xs font-bold">{{ t('categories.allView') }}</span>
          </button>

          <!-- 카테고리 버튼들 -->
          <button 
            v-for="cat in categories" 
            :key="cat"
            @click="selectCategory(cat)"
            :class="[
              'w-40 p-4 rounded-2xl flex flex-col items-center justify-center border transition-all hover:shadow-md',
              portal.selectedCategory === cat 
                ? 'bg-rose-500 text-white border-rose-500 shadow-md shadow-rose-100' 
                : 'bg-white text-slate-600 border-slate-100'
            ]"
          >
            <div
              :class="[
                'w-10 h-10 rounded-xl flex items-center justify-center mb-2',
                portal.selectedCategory === cat
                  ? 'bg-rose-400 text-white'
                  : 'bg-slate-50 text-rose-500'
              ]"
            >
              <i :class="getCategoryIcon(cat)"></i>
            </div>
            <span class="text-xs font-bold">{{ categoryLabel(cat) }}</span>
          </button>
        </div>

        <!-- Search Bar -->
        <div class="bg-white p-3 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-2">
          <i class="fas fa-magnifying-glass text-slate-400 ml-3"></i>
          <input 
            v-model="searchQuery" 
            @keyup.enter="runSearch"
            type="text" 
            :placeholder="searchPlaceholder"
            class="flex-1 bg-transparent border-none text-sm text-slate-800 placeholder-slate-400 focus:outline-none"
          >
          <button @click="runSearch" class="bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded-xl text-xs font-bold transition-all">
            {{ searchLabel }}
          </button>
        </div>
      </div>

      <!-- Posts Section -->
      <div>
        <h3 class="text-lg font-black text-slate-800 flex items-center mb-4">
          <span class="w-2 h-5 bg-rose-500 rounded-full mr-2"></span>
          {{ allPostsLabel }}
        </h3>

        <!-- Posts Grid -->
        <div v-if="portal.filteredPosts.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 items-stretch">
          <PostCard 
            v-for="post in paginatedPosts" 
            :key="post.id"
            :post="post"
            @click="viewPost(post)"
          />
        </div>

        <!-- 페이지네이션 -->
          <div
            v-if="portal.filteredPosts.length > 0"
            class="mt-10 flex items-center justify-center gap-2"
          >
            <button
              type="button"
              class="rounded-lg border px-3 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-40"
              :disabled="currentPage === 1"
              @click="movePage(currentPage - 1)"
            >
              {{ t('common.previous') }}
            </button>

            <button
              v-for="page in pageNumbers"
              :key="page"
              type="button"
              class="h-10 w-10 rounded-lg border text-sm font-bold transition-colors"
              :class="
                currentPage === page
                  ? 'border-rose-500 bg-rose-500 text-white'
                  : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-50'
              "
              @click="movePage(page)"
            >
              {{ page }}
            </button>

            <button
              type="button"
              class="rounded-lg border px-3 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-40"
              :disabled="currentPage === totalPages"
              @click="movePage(currentPage + 1)"
            >
              {{ t('common.next') }}
            </button>
          </div>

        <!-- No Posts Message -->
        <div v-else class="bg-slate-50 border border-slate-200 rounded-2xl p-16 text-center">
          <i class="fas fa-inbox text-4xl text-slate-300 mb-3"></i>
          <p class="text-slate-500 font-semibold">{{ emptyLabel }}</p>
          <p class="text-slate-400 text-sm mt-1">{{ emptyHint }}</p>
          <button @click="openWriteForm" class="bg-rose-500 hover:bg-rose-600 text-white px-6 py-2.5 rounded-xl font-bold mt-4 transition-all shadow-md shadow-rose-100">
            <i class="fas fa-pen-fancy mr-2"></i>
              {{ writeLabel }}
          </button>
        </div>
      </div>
    </div>
    <Teleport to="body">
      <div
        v-if="selectedPost"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-sm"
        role="dialog"
        aria-modal="true"
        :aria-label="t('community.detailLabel')"
        @click.self="closePostModal"
      >
        <article
          class="w-full max-w-2xl max-h-[85vh] overflow-y-auto rounded-3xl bg-white shadow-2xl"
        >
          <!-- 모달 헤더 -->
          <header class="sticky top-0 z-10 flex items-center justify-between border-b border-slate-100 bg-white px-6 py-4">
            <div class="flex items-center gap-3">
              <span class="rounded-full border border-rose-200 bg-rose-50 px-3 py-1 text-xs font-bold text-rose-600">
                {{ categoryLabel(selectedPost.category) }}
              </span>

              <span class="text-xs text-slate-400">
                {{ formatPostDate(selectedPost.createdAt) }}
              </span>
            </div>

            <button
              type="button"
              class="rounded-xl px-3 py-2 text-sm font-bold text-rose-500 transition-colors hover:bg-rose-50"
              @click="requestEdit(selectedPost)"
            >
              <i class="fas fa-pen mr-1"></i>
              {{ t('common.edit') }}
            </button>

            <button
              type="button"
              class="rounded-xl px-3 py-2 text-sm font-bold text-red-500 transition-colors hover:bg-red-50"
              @click="requestDelete(selectedPost)"
            >
              <i class="fas fa-trash-can mr-1"></i>
              {{ t('common.delete') }}
            </button>

            <button
              type="button"
              class="flex h-9 w-9 items-center justify-center rounded-full text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-700"
              :aria-label="t('community.closeDetailLabel')"
              @click="closePostModal"
            >
              <i class="fas fa-xmark text-lg"></i>
            </button>
          </header>

          <!-- 모달 본문 -->
          <div class="px-6 py-7 sm:px-8">
            <h2 class="mb-3 text-2xl font-black leading-snug text-slate-900">
              {{ selectedPost.title }}
            </h2>

            <div class="mb-6 flex items-center gap-2 text-sm text-slate-500">
              <i class="fas fa-user-circle text-slate-400"></i>
              <span class="font-semibold">{{ selectedPost.nickname }}</span>
            </div>

            <div class="whitespace-pre-wrap break-words text-sm leading-7 text-slate-700">
              {{ selectedPost.content }}
            </div>
          </div>

          <!-- 모달 Footer -->
          <footer class="border-t border-slate-100 bg-slate-50 px-6 py-4 text-right sm:px-8">
            <button
              type="button"
              class="rounded-xl bg-slate-800 px-4 py-2 text-sm font-bold text-white transition-colors hover:bg-slate-700"
              @click="closePostModal"
            >
              {{ t('common.close') }}
            </button>
          </footer>
        </article>
      </div>
    </Teleport>
    <Teleport to="body">
      <div
        v-if="showPostForm"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-sm"
        @click.self="closePostForm"
      >
        <form
          class="w-full max-w-2xl rounded-3xl bg-white shadow-2xl"
          @submit.prevent="submitPostForm"
        >
          <header class="flex items-center justify-between border-b border-slate-100 px-6 py-5">
            <div>
              <h2 class="text-xl font-black text-slate-900">{{ editingPost ? t('community.formEditTitle') : t('community.formTitle') }}</h2>
              <p class="mt-1 text-sm text-slate-500">
                {{ t('community.formHint') }}
              </p>
            </div>

            <button
              type="button"
              class="flex h-9 w-9 items-center justify-center rounded-full text-slate-400 hover:bg-slate-100"
              :aria-label="t('community.closeDetailLabel')"
              @click="closePostForm"
            >
              <i class="fas fa-xmark text-lg"></i>
            </button>
          </header>

          <div class="space-y-4 px-6 py-6">
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <label class="space-y-1.5">
                <span class="text-sm font-bold text-slate-700">{{ t('community.category') }}</span>
                <select
                  v-model="postForm.category"
                  class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-rose-400"
                >
                  <option v-for="category in categories" :key="category" :value="category">
                    {{ categoryLabel(category) }}
                  </option>
                </select>
              </label>

              <label class="space-y-1.5">
                <span class="text-sm font-bold text-slate-700">{{ t('community.nickname') }}</span>
                <input
                  v-model="postForm.nickname"
                  type="text"
                  maxlength="20"
                  :placeholder="t('community.nicknamePlaceholder')"
                  class="w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-rose-400"
                >
              </label>
            </div>

            <label class="block space-y-1.5">
              <span class="text-sm font-bold text-slate-700">{{ t('community.postTitle') }}</span>
              <input
                v-model="postForm.title"
                type="text"
                maxlength="100"
                :placeholder="t('community.titlePlaceholder')"
                class="w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-rose-400"
              >
            </label>

            <label class="block space-y-1.5">
              <span class="text-sm font-bold text-slate-700">{{ t('community.content') }}</span>
              <textarea
                v-model="postForm.content"
                rows="8"
                :placeholder="t('community.contentPlaceholder')"
                class="w-full resize-none rounded-xl border border-slate-200 px-3 py-2.5 text-sm leading-6 outline-none focus:border-rose-400"
              ></textarea>
            </label>

            <label class="block space-y-1.5">
              <span class="text-sm font-bold text-slate-700">{{ t('community.password') }}</span>
              <input
                v-model="postForm.password"
                type="password"
                maxlength="30"
                :placeholder="t('community.passwordPlaceholder')"
                class="w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-rose-400"
              >
            </label>
          </div>

          <footer class="flex justify-end gap-2 border-t border-slate-100 bg-slate-50 px-6 py-4">
            <button
              type="button"
              class="rounded-xl px-4 py-2.5 text-sm font-bold text-slate-500 hover:bg-slate-200"
              @click="closePostForm"
            >
              {{ t('common.cancel') }}
            </button>

            <button
              type="submit"
              class="rounded-xl bg-rose-500 px-5 py-2.5 text-sm font-bold text-white shadow-md shadow-rose-100 hover:bg-rose-600"
            >
              {{ t('common.submit') }}
            </button>
          </footer>
        </form>
      </div>
    </Teleport>
    <Teleport to="body">
      <div
        v-if="showPasswordModal"
        class="fixed inset-0 z-[60] flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-sm"
        @click.self="showPasswordModal = false"
      >
        <form
          class="w-full max-w-sm rounded-3xl bg-white p-6 shadow-2xl"
          @submit.prevent="verifyPostPassword"
        >
          <h2 class="text-lg font-black text-slate-900">
            {{ passwordAction === 'delete' ? t('community.deleteTitle') : t('community.passwordCheckTitle') }}
          </h2>

          <p class="mt-2 text-sm leading-6 text-slate-500">
            <template v-if="passwordAction === 'delete'">
              {{ t('community.deleteDescription') }}
            </template>

            <template v-else>
              {{ t('community.editDescription') }}
            </template>
          </p>

          <input
            v-model="editPassword"
            type="password"
            autofocus
            :placeholder="t('community.passwordInputPlaceholder')"
            class="mt-5 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-rose-400"
          >

          <div class="mt-5 flex justify-end gap-2">
            <button
              type="button"
              class="rounded-xl px-4 py-2.5 text-sm font-bold text-slate-500 hover:bg-slate-100"
              @click="showPasswordModal = false"
            >
              {{ t('common.cancel') }}
            </button>

            <button
              type="submit"
              :class="[
                'rounded-xl px-4 py-2.5 text-sm font-bold text-white',
                passwordAction === 'delete'
                  ? 'bg-red-500 hover:bg-red-600'
                  : 'bg-rose-500 hover:bg-rose-600'
              ]"
            >
              {{ passwordAction === 'delete' ? t('community.deleteSubmit') : t('common.confirm') }}
            </button>
          </div>
        </form>
      </div>
    </Teleport>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { usePortalStore } from '@/stores/portalStore'
import { useUIStore } from '@/stores/uiStore'
import type { Post } from '@/stores/portalStore'
import PostCard from '@/components/PostCard.vue'

const portal = usePortalStore()
const ui = useUIStore()
const { locale, t } = useI18n()

const searchQuery = ref('')
const ALL_CATEGORY = '전체'


const pageTitle = computed(() => t('community.title'))
const pageSubtitle = computed(() => t('community.subtitle'))
const searchPlaceholder = computed(() => t('community.searchPlaceholder'))
const searchLabel = computed(() => t('common.search'))
const allPostsLabel = computed(() => t('community.allPosts'))
const writeLabel = computed(() => t('community.write'))
const emptyLabel = computed(() => t('community.empty'))
const emptyHint = computed(() => t('community.emptyHint'))
const passwordAction = ref<'edit' | 'delete'>('edit')
const DISPLAY_PAGE_COUNT = 10

// 검색 실행
const runSearch = () => {
  portal.searchQuery = searchQuery.value
  currentPage.value = 1 // 검색하면 첫 페이지부터 표시

  if (searchQuery.value.trim()) {
    ui.showToast(t('toast.searchApplied', { query: searchQuery.value }))
  }
}
const showPostForm = ref(false)
const showPasswordModal = ref(false)
const editingPost = ref<Post | null>(null)
const editPassword = ref('')

const postForm = ref({
  category: '여행지',
  nickname: '',
  title: '',
  content: '',
  password: '',
})

const resetPostForm = () => {
  postForm.value = {
    category: '여행지',
    nickname: '',
    title: '',
    content: '',
    password: '',
  }
}

const openWriteForm = () => {
  editingPost.value = null
  resetPostForm()
  showPostForm.value = true
}

const closePostForm = () => {
  showPostForm.value = false
  resetPostForm()
}

const submitPostForm = async () => {
  const { category, nickname, title, content, password } = postForm.value

  if (!title.trim() || !content.trim()) {
    ui.showToast(t('toast.requiredPostFields'))
    return
  }

  // 🟢 닉네임이 비어있다면 익명 처리를 해줍니다 (선택 사항이지만 권장)
  const finalNickname = nickname.trim() || '익명 사용자'

  // 게시글 수정
  if (editingPost.value) {
    const updated = await portal.updatePostWithPassword(
      editingPost.value.id,
      editPassword.value,
      {
        category,
        nickname: finalNickname,
        title: title.trim(),
        content: content.trim(),
      }
    )

    if (!updated) {
      ui.showToast(t('toast.passwordMismatch'))
      return
    }

    if (selectedPost.value) {
      selectedPost.value = {
        ...selectedPost.value,
        category,
        nickname: finalNickname,
        title: title.trim(),
        content: content.trim(),
      }
    }

    editingPost.value = null
    closePostForm()
    ui.showToast(t('toast.postUpdated'))
    return
  }

  // 새 게시글 작성
  if (!password.trim()) {
    ui.showToast(t('toast.passwordRequired'))
    return
  }

  await portal.addPost({
    category,
    nickname: finalNickname, // 저장 반영
    title: title.trim(),
    content: content.trim(),
    password,
  })

  closePostForm()
  ui.showToast(t('toast.postCreated'))
}

const selectedPost = ref<Post | null>(null)

// 카테고리 아이콘 반환
const categories = ['여행지', '맛집', '축제']

const categoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    전체: t('categories.all'),
    여행지: t('categories.travel'),
    맛집: t('categories.restaurant'),
    축제: t('categories.festival'),
    카페: t('categories.cafe'),
  }

  return labels[category] ?? category
}

const getCategoryIcon = (cat: string): string => {
  const icons: Record<string, string> = {
    여행지: 'fa-solid fa-map-location-dot',
    맛집: 'fa-solid fa-utensils',
    축제: 'fa-solid fa-wand-magic-sparkles'
  }
  return icons[cat] ?? 'fa-solid fa-circle-info'
}

// 게시글 상세보기
const viewPost = (post: Post) => {
  selectedPost.value = post
}

const closePostModal = () => {
  selectedPost.value = null
}

const requestEdit = (post: Post) => {
  editingPost.value = post
  editPassword.value = ''
  passwordAction.value = 'edit'
  showPasswordModal.value = true
}

const requestDelete = (post: Post) => {
  editingPost.value = post
  editPassword.value = ''
  passwordAction.value = 'delete'
  showPasswordModal.value = true
}

const formatPostDate = (dateString: string) => {
  return new Date(dateString).toLocaleString(locale.value === 'ko' ? 'ko-KR' : 'en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const selectCategory = (category: string) => {
  portal.selectedCategory = category
  currentPage.value = 1
}

const POSTS_PER_PAGE = 6 // 한 페이지에 보일 게시글 수
const currentPage = ref(1)

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(portal.filteredPosts.length / POSTS_PER_PAGE))
})

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * POSTS_PER_PAGE
  const end = start + POSTS_PER_PAGE

  return portal.filteredPosts.slice(start, end)
})

const pageNumbers = computed(() => {
  const total = totalPages.value

  // 전체 페이지가 10개 이하라면 모두 표시
  if (total <= DISPLAY_PAGE_COUNT) {
    return Array.from(
      { length: total },
      (_, index) => index + 1
    )
  }


  let startPage =
    currentPage.value - Math.floor(DISPLAY_PAGE_COUNT / 2)

  let endPage =
    currentPage.value + Math.floor(DISPLAY_PAGE_COUNT / 2) - 1


  // 앞쪽 보정
  if (startPage < 1) {
    startPage = 1
    endPage = DISPLAY_PAGE_COUNT
  }


  // 뒤쪽 보정
  if (endPage > total) {
    endPage = total
    startPage = total - DISPLAY_PAGE_COUNT + 1
  }


  return Array.from(
    { length: DISPLAY_PAGE_COUNT },
    (_, index) => startPage + index
  )
})

const movePage = (page: number) => {
  currentPage.value = Math.min(Math.max(page, 1), totalPages.value)
}

const verifyPostPassword = async () => {
  if (!editingPost.value) return

  if (String(editingPost.value.password) !== editPassword.value.trim()) {
    ui.showToast(t('toast.passwordMismatch'))
    return
  }

  // 삭제 모드
  if (passwordAction.value === 'delete') {
    const deleted = await portal.deletePostWithPassword(
      editingPost.value.id,
      editPassword.value
    )

    if (!deleted) {
      ui.showToast(t('toast.postDeleteFailed'))
      return
    }

    selectedPost.value = null
    editingPost.value = null
    showPasswordModal.value = false
    ui.showToast(t('toast.postDeleted'))
    return
  }

  // 수정 모드: 기존 내용을 폼에 채운 뒤 작성 모달 열기
  postForm.value = {
    category: editingPost.value.category,
    nickname: editingPost.value.nickname,
    title: editingPost.value.title,
    content: editingPost.value.content,
    password: '',
  }

  showPasswordModal.value = false
  showPostForm.value = true
}
</script>
