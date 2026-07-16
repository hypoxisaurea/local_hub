import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/HomeView.vue'),
      meta: {
        shareImage: '/banners/banner.png',
        seo: {
          ko: {
            title: 'Local Hub - 서울 로컬 정보 공유 커뮤니티',
            description: '서울 여행자들이 로컬 정보, 숨은 명소, 맛집, 여행 후기를 함께 공유하는 커뮤니티입니다.'
          },
          en: {
            title: 'Local Hub - Seoul Local Travel Community',
            description: 'A community where Seoul travelers share local tips, hidden gems, restaurants, and travel reviews.'
          }
        }
      }
    },
    {
      path: '/community',
      name: 'Community',
      component: () => import('@/views/CommunityView.vue'),
      meta: {
        shareImage: '/banners/community_banner.png',
        seo: {
          ko: {
            title: 'Local Hub 커뮤니티 - 서울 로컬 정보 공유',
            description: '서울 여행자들과 지역 커뮤니티가 맛집, 여행지, 축제 후기를 자유롭게 나누는 공간입니다.'
          },
          en: {
            title: 'Local Hub Community - Seoul Local Tips',
            description: 'Share restaurants, places, festivals, and travel reviews with Seoul travelers and locals.'
          }
        }
      }
    },
    {
      path: '/travel',
      name: 'Travel',
      component: () => import('@/views/TravelView.vue'),
      meta: {
        seo: {
          ko: {
            title: 'Local Hub 여행지 - 서울 명소 찾기',
            description: '서울의 관광지, 문화시설, 쇼핑, 레포츠 정보를 지도와 목록으로 확인하세요.'
          },
          en: {
            title: 'Local Hub Places - Explore Seoul',
            description: 'Browse Seoul attractions, culture, shopping, and leisure spots in one place.'
          }
        }
      }
    },
    {
      path: '/restaurant',
      name: 'Restaurant',
      component: () => import('@/views/RestaurantView.vue'),
      meta: {
        seo: {
          ko: {
            title: 'Local Hub 맛집 - 서울 음식점 찾기',
            description: '지역, 음식 종류, 분위기로 서울 맛집을 검색하고 여행 계획에 더해보세요.'
          },
          en: {
            title: 'Local Hub Restaurants - Seoul Food Guide',
            description: 'Find Seoul restaurants by area, cuisine, and mood for your next trip.'
          }
        }
      }
    },
    {
      path: '/festival',
      name: 'Festival',
      component: () => import('@/views/FestivalView.vue'),
      meta: {
        seo: {
          ko: {
            title: 'Local Hub 축제 - 서울 행사 정보',
            description: '서울에서 열리는 축제, 공연, 행사 정보를 찾아보고 일정을 확인하세요.'
          },
          en: {
            title: 'Local Hub Festivals - Seoul Events',
            description: 'Discover festivals, performances, and events happening around Seoul.'
          }
        }
      }
    }
  ]
})

export default router
