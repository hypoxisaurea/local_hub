import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Comment {
  id: number
  nickname: string
  content: string
  createdAt: string
}

export interface Post {
  id: number
  category: string
  title: string
  content: string
  nickname: string
  password: string
  createdAt: string
  likes: number
  comments: Comment[]
}

export const usePortalStore = defineStore('portal', () => {
  // 기본 게시글 데이터
  const defaultPosts: Post[] = [
    {
      id: 1,
      category: '여행지',
      title: '경복궁 한복 대여 꿀팁 공유 드립니다!',
      content: '주말에는 방문자가 엄청 많으니 가급적 오전 9시 개장 시간에 맞춰 가시는 걸 추천해요. 그리고 근처 대여점마다 가격은 비슷한데, 소품이나 머리 땋아주는 서비스가 포함인지 미리 물어보시면 돈을 훨씬 절약할 수 있습니다.',
      nickname: '성동구여우',
      password: '1111',
      createdAt: new Date(Date.now() - 3600000 * 2).toISOString(),
      likes: 32,
      comments: [
        {
          id: 1,
          nickname: '마포갈매기',
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
      nickname: '남대문아재',
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
      nickname: '커피마니아',
      password: '3333',
      createdAt: new Date(Date.now() - 3600000 * 8).toISOString(),
      likes: 28,
      comments: []
    }
  ]

  // 로컬스토리지에서 불러오기 또는 기본값 사용
  const posts = ref<Post[]>(
    JSON.parse(localStorage.getItem('localhub_posts') || JSON.stringify(defaultPosts))
  )

  const selectedCategory = ref('전체')
  const searchQuery = ref('')

  // 필터링된 게시글
  const filteredPosts = computed(() => {
    let result = posts.value

    // 카테고리 필터
    if (selectedCategory.value !== '전체') {
      result = result.filter(p => p.category === selectedCategory.value)
    }

    // 검색어 필터
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase()
      result = result.filter(p =>
        p.title.toLowerCase().includes(q) ||
        p.content.toLowerCase().includes(q)
      )
    }

    return result
  })

  // 게시글 추가
  const addPost = (
    post: Omit<Post, 'id' | 'createdAt' | 'likes' | 'comments'>
  ) => {
    const newPost: Post = {
      ...post,
      id: Date.now(),
      createdAt: new Date().toISOString(),
      likes: 0,
      comments: [],
    }

    posts.value.unshift(newPost)
    saveToStorage()
}

  // 게시글 수정
  const updatePost = (id: number, updates: Partial<Post>) => {
    const idx = posts.value.findIndex(p => p.id === id)
    const currentPost = posts.value[idx]
    if (currentPost) {
      posts.value[idx] = { ...currentPost, ...updates }
      saveToStorage()
    }
  }

  // 비밀번호 확인하는 함수
  const updatePostWithPassword = (
    id: number,
    password: string,
    updates: Pick<Post, 'category' | 'nickname' | 'title' | 'content'>
  ) => {
    const post = posts.value.find((item) => item.id === id)

    if (!post || post.password !== password) {
      return false
    }

    Object.assign(post, updates)
    saveToStorage()

    return true
  }

  // 게시글 삭제
  const deletePost = (id: number) => {
    posts.value = posts.value.filter(p => p.id !== id)
    saveToStorage()
  }

  const deletePostWithPassword = (id: number, password: string) => {
  const post = posts.value.find((item) => item.id === id)

  if (!post || post.password !== password) {
    return false
  }

  posts.value = posts.value.filter((item) => item.id !== id)
  saveToStorage()

  return true
  }

  // 댓글 추가
  const addComment = (postId: number, comment: Omit<Comment, 'id'>) => {
    const post = posts.value.find(p => p.id === postId)
    if (post) {
      post.comments.push({
        ...comment,
        id: Date.now()
      })
      saveToStorage()
    }
  }

  // 로컬스토리지 저장
  const saveToStorage = () => {
    localStorage.setItem('localhub_posts', JSON.stringify(posts.value))
  }

  return {
    posts,
    selectedCategory,
    searchQuery,
    filteredPosts,
    addPost,
    updatePost,
    deletePost,
    addComment,
    updatePostWithPassword,
    deletePostWithPassword,
  }
})
