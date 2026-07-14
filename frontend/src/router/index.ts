import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/community',
      name: 'Community',
      component: () => import('@/views/CommunityView.vue')
    },
    {
      path: '/travel',
      name: 'Travel',
      component: () => import('@/views/TravelView.vue')
    },
    {
      path: '/restaurant',
      name: 'Restaurant',
      component: () => import('@/views/RestaurantView.vue')
    },
    {
      path: '/festival',
      name: 'Festival',
      component: () => import('@/views/FestivalView.vue')
    }
  ]
})

export default router