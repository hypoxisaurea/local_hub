import { createI18n } from 'vue-i18n'

const messages = {
  ko: {
    common: {
      switchLang: 'EN'
    },
    nav: {
      community: '커뮤니티',
      travel: '여행지',
      restaurant: '맛집',
      festival: '축제'
    },
    home: {
      title: '서울, 우리끼리 로컬 정보 공유해요!',
      subtitle: '여행자들의 생생한 리뷰와 꿀팁을 한 곳에서 만나보세요.',
      searchPlaceholder: '어디를 찾고 있나요? (예: 을지로, 맛집, 성수동)',
      search: '검색',
      chatbot: '여행 계획 도와드려요! 클릭해서 시작하세요.'
    },
    community: {
      title: '커뮤니티',
      subtitle: '지역 커뮤니티와 소통하세요',
      searchPlaceholder: '게시글 검색...',
      search: '검색',
      allPosts: '전체 게시글',
      write: '글 작성하기',
      empty: '게시글이 없습니다.'
    }
  },
  en: {
    common: {
      switchLang: 'KO'
    },
    nav: {
      community: 'Community',
      travel: 'Places',
      restaurant: 'Restaurants',
      festival: 'Festivals'
    },
    home: {
      title: 'Share local Seoul tips together!',
      subtitle: 'Discover real traveler reviews and hidden gems in one place.',
      searchPlaceholder: 'Where are you looking for? (e.g. Euljiro, food, Seongsu)',
      search: 'Search',
      chatbot: 'Need help planning your trip? Click to start.'
    },
    community: {
      title: 'Community',
      subtitle: 'Connect with your local community',
      searchPlaceholder: 'Search posts...',
      search: 'Search',
      allPosts: 'All posts',
      write: 'Write a post',
      empty: 'No posts yet.'
    }
  }
}

export const i18n = createI18n({
  legacy: false,
  locale: typeof window !== 'undefined' ? (localStorage.getItem('localhub-locale') || 'ko') : 'ko',
  fallbackLocale: 'ko',
  messages
})

export const setLocale = (lang: 'ko' | 'en') => {
  i18n.global.locale.value = lang
  if (typeof window !== 'undefined') {
    localStorage.setItem('localhub-locale', lang)
  }
}