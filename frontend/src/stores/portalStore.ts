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
  password: string
  createdAt: string
  likes: number
  comments: Comment[]
}

// 여기 앞쪽에 .env 파일에서 API_BASE를 가져오는게 실패함
const API_BASE = (import.meta as any).env.VITE_API_BASE || 'http://localhost:8000/api'

export const usePortalStore = defineStore('portal', () => {
  const defaultPosts: Post[] = [
    {
      id: 1,
      category: '여행지',
      title: '경복궁 한복 대여 꿀팁 공유 드립니다!',
      content: '주말에는 방문자가 엄청 많으니 가급적 오전 9시 개장 시간에 맞춰 가시는 걸 추천해요. 그리고 근처 대여점마다 가격은 비슷한데, 소품이나 머리 땋아주는 서비스가 포함인지 미리 물어보시면 돈을 훨씬 절약할 수 있습니다.',

      password: '1111',
      createdAt: new Date(Date.now() - 3600000 * 2).toISOString(),
      likes: 32,
      comments: [
        {
          id: 1,
          
          content: '좋은 팁이네요! 내일 모레 가는데 참고하겠습니다.',
          createdAt: new Date(Date.now() - 3600000).toISOString()
        }
      ]
    },
    {
      id: 2,
      category: '맛집',
      title: '광장시장 먹거리 추천 및 바가지 피하기 방법',
      content: '육회나 빈대떡은 가격이 정해져 있어서 안전해요! 모듬순대나 떡볶이 시키실 때는 먼저 양이랑 가격 꼭 물어보시는 것 추천합니다.',
      
      password: '2222',
      createdAt: new Date(Date.now() - 3600000 * 5).toISOString(),
      likes: 45,
      comments: []
    },
    {
      id: 3,
      category: '카페',
      title: '성수동 힙하고 야외 테라스 예쁜 카페 3곳',
      content: '주택을 개조한 이색적인 분위기의 인더스트리얼 감성 카페들 위주로 다녀왔습니다. 대기가 다소 길 수 있으나 인생사진 건지기 좋은 스팟들이에요.',
      
      password: '3333',
      createdAt: new Date(Date.now() - 3600000 * 8).toISOString(),
      likes: 28,
      comments: []
    }
  ]

  const posts = ref<Post[]>(JSON.parse(localStorage.getItem('localhub_posts') || 'null') || defaultPosts)
  const selectedCategory = ref('전체')
  const searchQuery = ref('')

  const filteredPosts = computed(() => {
    let result = posts.value
    if (selectedCategory.value !== '전체') {
      result = result.filter(p => p.category === selectedCategory.value)
    }
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase()
      result = result.filter(p =>
        p.title.toLowerCase().includes(q) ||
        p.content.toLowerCase().includes(q)
      )
    }
    return result
  })

  const saveToStorage = () => {
    localStorage.setItem('localhub_posts', JSON.stringify(posts.value))
  }

  // fetch from backend
  const fetchPosts = async () => {
    try {
      const res = await fetch(`${API_BASE}/posts`)
      if (!res.ok) throw new Error('fetch failed')
      posts.value = await res.json()
      saveToStorage()
    } catch (e) {
      // 네트워크 실패 시 로컬스토리지 유지 (이미 로드됨)
      console.warn('Failed to fetch posts, using local cache', e)
    }
  }

  const addPost = async (post: Omit<Post, 'id' | 'createdAt' | 'likes' | 'comments'>) => {
    try {
      const res = await fetch(`${API_BASE}/posts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(post)
      })
      if (!res.ok) throw new Error('create failed')
      const created = await res.json()
      posts.value.unshift(created)
      saveToStorage()
      return created
    } catch (e) {
      console.error(e)
      // fallback: 로컬에 추가
      const newPost: Post = {
        ...post,
        id: Date.now(),
        createdAt: new Date().toISOString(),
        likes: 0,
        comments: []
      } as Post
      posts.value.unshift(newPost)
      saveToStorage()
      return newPost
    }
  }

  const updatePost = async (id: number, updates: Partial<Post>, password?: string) => {
    try {
      const body = { ...updates } as any
      if (password) body.password = password
      const res = await fetch(`${API_BASE}/posts/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      if (!res.ok) throw new Error('update failed')
      const updated = await res.json()
      const idx = posts.value.findIndex(p => p.id === id)
      if (idx !== -1) posts.value[idx] = updated
      saveToStorage()
      return updated
    } catch (e) {
      console.error(e)
      return null
    }
  }

  const deletePost = async (id: number, password?: string) => {
    try {
      const res = await fetch(`${API_BASE}/posts/${id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(password ? { password } : {})
      })
      if (!res.ok) throw new Error('delete failed')
      posts.value = posts.value.filter(p => p.id !== id)
      saveToStorage()
      return true
    } catch (e) {
      console.error(e)
      return false
    }
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
      const post = posts.value.find(p => p.id === postId)
      if (post) post.comments.push(created)
      saveToStorage()
      return created
    } catch (e) {
      console.error(e)
      // fallback 로컬
      const post = posts.value.find(p => p.id === postId)
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

  // 초기 로드
  fetchPosts()

  return {
    posts,
    selectedCategory,
    searchQuery,
    filteredPosts,
    fetchPosts,
    addPost,
    updatePost,
    deletePost,
    addComment
  }
})