<template>
  <div class="main-layout">
    <HeaderNav />
    <main class="content">
      <RouterView />
    </main>
    <FooterSection />
  </div>
</template>

<script setup lang="ts">
import HeaderNav from '@/components/HeaderNav.vue'
import FooterSection from '@/components/FooterSection.vue'
</script>

<style scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
}
</style>