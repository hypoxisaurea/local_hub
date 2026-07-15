import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Comment {
  id: number
  content: string
  createdAt: string
}

export interface Post {
  id: number
  category: string
  title: string
  content: string
  password: string | number
  createdAt: string
  likes: number
  comments: Comment[]
  nickname: string
}

export interface PostInput {
  category: string
  nickname: string
  title: string
  content: string
  password: string | number
}

const API_BASE = (import.meta as any).env.VITE_API_BASE || 'http://localhost:8000/api'

const normalizePost = (raw: any): Post => {
  const rawCategory = typeof raw.category === 'string'
    ? raw.category
    : raw.category?.name || raw.category_name || '기타'

  const categoryName = rawCategory === '여행' ? '여행지' : rawCategory === '문화' ? '축제' : rawCategory

  return {
    id: raw.id ?? raw.pk_post_id,
    category: categoryName,
    title: raw.title ?? '',
    content: raw.content ?? '',
    password: raw.password ?? '',
    createdAt: raw.createdAt ?? raw.created_at ?? new Date().toISOString(),
    likes: raw.likes ?? 0,
    comments: Array.isArray(raw.comments) ? raw.comments.map((comment: any) => ({
      id: comment.id ?? comment.pk_comment_id,
      content: comment.content ?? '',
      createdAt: comment.createdAt ?? comment.created_at ?? new Date().toISOString()
    })) : [],
    nickname: raw.nickname ?? '익명 사용자'
  }
}

const mapCategoryToFkId = (category: string) => {
  switch (category) {
    case '여행지':
      return 1
    case '축제':
      return 2
    case '맛집':
      return 3
    default:
      return 1
  }
}

export const usePortalStore = defineStore('portal', () => {
  const storedPosts = localStorage.getItem('localhub_posts')
  const initialPosts = storedPosts ? JSON.parse(storedPosts).map(normalizePost) : []

  const posts = ref<Post[]>(initialPosts)
  const selectedCategory = ref('전체')
  const searchQuery = ref('')

  const filteredPosts = computed(() => {
    let result = posts.value
    if (selectedCategory.value !== '전체') {
      result = result.filter((p) => p.category === selectedCategory.value)
    }
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase()
      result = result.filter((p) =>
        p.title.toLowerCase().includes(q) ||
        p.content.toLowerCase().includes(q)
      )
    }
    return result
  })

  const saveToStorage = () => {
    localStorage.setItem('localhub_posts', JSON.stringify(posts.value))
  }

  const fetchPosts = async () => {
    try {
      const res = await fetch(`${API_BASE}/posts`)
      if (!res.ok) throw new Error('fetch failed')
      const payload = await res.json()
      posts.value = Array.isArray(payload) ? payload.map(normalizePost) : []
      saveToStorage()
    } catch (e) {
      console.warn('Failed to fetch posts, using local cache', e)
    }
  }

  const addPost = async (post: PostInput) => {
    try {
      const payload = {
        fk_category_id: mapCategoryToFkId(post.category),
        title: post.title,
        content: post.content,
        password: Number(post.password)
      }

      const res = await fetch(`${API_BASE}/posts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!res.ok) throw new Error('create failed')
      const created = normalizePost(await res.json())
      posts.value.unshift(created)
      saveToStorage()
      return created
    } catch (e) {
      console.error(e)

      const newPost: Post = {
        ...post,
        id: Date.now(),
        createdAt: new Date().toISOString(),
        likes: 0,
        comments: [],
        nickname: post.nickname || '익명 사용자'
      } as Post
      posts.value.unshift(newPost)
      saveToStorage()
      return newPost
    }
  }

  const updatePost = async (id: number, updates: Partial<PostInput>, password?: string) => {
    try {
      const body: any = {
        fk_category_id: updates.category ? mapCategoryToFkId(updates.category) : undefined,
        title: updates.title,
        content: updates.content,
        password: password ? Number(password) : undefined
      }

      Object.keys(body).forEach((key) => {
        if (body[key] === undefined) delete body[key]
      })

      const res = await fetch(`${API_BASE}/posts/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      if (!res.ok) throw new Error('update failed')
      const updated = normalizePost(await res.json())
      const idx = posts.value.findIndex((p) => p.id === id)
      if (idx !== -1) posts.value[idx] = updated
      saveToStorage()
      return updated
    } catch (e) {
      console.error(e)
      return null
    }
  }

  const updatePostWithPassword = async (id: number, password: string, updates: Partial<PostInput>) => {
    const current = posts.value.find((post) => post.id === id)
    if (!current) return false
    if (String(current.password) !== String(password)) return false

    const updated = await updatePost(id, updates, password)
    if (!updated) return false

    const idx = posts.value.findIndex((post) => post.id === id)
    if (idx !== -1) {
      const target = posts.value[idx]
      if (target) {
        posts.value[idx] = {
          ...target,
          category: updated.category,
          title: updated.title,
          content: updated.content,
          nickname: updates.nickname ?? target.nickname,
        }
      }
    }
    saveToStorage()
    return true
  }

  const deletePost = async (id: number, password?: string) => {
    try {
      const res = await fetch(`${API_BASE}/posts/${id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(password ? { password } : {})
      })
      if (!res.ok) throw new Error('delete failed')
      posts.value = posts.value.filter((p) => p.id !== id)
      saveToStorage()
      return true
    } catch (e) {
      console.error(e)
      return false
    }
  }

  const deletePostWithPassword = async (id: number, password: string) => {
    const current = posts.value.find((post) => post.id === id)
    if (!current) return false
    if (String(current.password) !== String(password)) return false

    return deletePost(id, password)
  }

  const addComment = async (postId: number, comment: Omit<Comment, 'id' | 'createdAt'>) => {
    try {
      const res = await fetch(`${API_BASE}/posts/${postId}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(comment)
      })
      if (!res.ok) throw new Error('add comment failed')
      const created = await res.json()
      const post = posts.value.find((p) => p.id === postId)
      if (post) post.comments.push(created)
      saveToStorage()
      return created
    } catch (e) {
      console.error(e)
      const post = posts.value.find((p) => p.id === postId)
      if (post) {
        const localComment: Comment = {
          id: Date.now(),
          content: (comment as any).content,
          createdAt: new Date().toISOString()
        }
        post.comments.push(localComment)
        saveToStorage()
        return localComment
      }
      return null
    }
  }

  fetchPosts()

  return {
    posts,
    selectedCategory,
    searchQuery,
    filteredPosts,
    fetchPosts,
    addPost,
    updatePost,
    updatePostWithPassword,
    deletePost,
    deletePostWithPassword,
    addComment
  }
})
