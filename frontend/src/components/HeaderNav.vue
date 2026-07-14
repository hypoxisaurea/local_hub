<template>
  <header class="header">
    <nav class="navbar">
      <!-- 로고 -->
      <div class="logo">
        <RouterLink to="/">
          <img src="@/assets/logo.svg" alt="Logo" class="logo-img">
          <span class="logo-text">Local Hub</span>
        </RouterLink>
      </div>

      <!-- 네비게이션 메뉴 -->
      <ul class="nav-menu">
        <li><RouterLink to="/" :class="{ active: activeRoute === '/' }">홈</RouterLink></li>
        <li><RouterLink to="/community" :class="{ active: activeRoute === '/community' }">커뮤니티</RouterLink></li>
        <li><RouterLink to="/travel" :class="{ active: activeRoute === '/travel' }">여행지</RouterLink></li>
        <li><RouterLink to="/restaurant" :class="{ active: activeRoute === '/restaurant' }">맛집</RouterLink></li>
        <li><RouterLink to="/festival" :class="{ active: activeRoute === '/festival' }">축제</RouterLink></li>
      </ul>

      <!-- 사용자 메뉴 (로그인/회원가입) -->
      <div class="user-menu">
        <button class="login-btn">로그인</button>
        <button class="signup-btn">회원가입</button>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeRoute = computed(() => route.path)
</script>

<style scoped>
.header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 70px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo a {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.logo-img {
  height: 40px;
  width: auto;
}

.logo-text {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 30px;
  margin: 0;
  padding: 0;
}

.nav-menu a {
  text-decoration: none;
  color: #666;
  font-size: 16px;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-menu a:hover,
.nav-menu a.active {
  color: #ff6b6b;
}

.user-menu {
  display: flex;
  gap: 10px;
}

.login-btn,
.signup-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.login-btn {
  background-color: transparent;
  color: #666;
  border: 1px solid #ddd;
}

.login-btn:hover {
  background-color: #f5f5f5;
}

.signup-btn {
  background-color: #ff6b6b;
  color: white;
}

.signup-btn:hover {
  background-color: #ff5252;
}

@media (max-width: 768px) {
  .navbar {
    flex-wrap: wrap;
  }

  .nav-menu {
    gap: 15px;
    font-size: 14px;
  }

  .user-menu {
    width: 100%;
    margin-top: 10px;
  }
}
</style>