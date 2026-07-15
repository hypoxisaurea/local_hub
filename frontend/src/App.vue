<script setup lang="ts">
import { RouterView } from 'vue-router'
import HeaderNav from '@/components/HeaderNav.vue'
import FooterSection from '@/components/FooterSection.vue'
</script>

<template>
  <div id="app" class="min-h-screen flex flex-col bg-white">
    <!-- Header Navigation (투명) -->
    <HeaderNav />

    <!-- Main Content -->
    <main class="flex-1">
      <RouterView />
    </main>

    <!-- Footer -->
    <FooterSection />
  </div>
</template>

<style scoped>
/* Global styles */
</style>