<script setup>
import { usePageStore } from '../stores/page.js'
const pageStore = usePageStore()
</script>

<template>
  <header
    class="fixed top-0 right-0 w-[calc(100%-260px)] h-[70px] backdrop-blur-md bg-surface/80 dark:bg-inverse-surface/80 border-b border-outline-variant/30 dark:border-white/10 flex justify-between items-center px-margin-desktop z-40 transition-all duration-300"
  >
    <!-- Breadcrumbs / Page title -->
    <div class="flex items-center gap-8">
      <h2
        class="font-headline-sm text-headline-sm font-bold text-on-surface dark:text-white capitalize"
      >
        {{ pageStore.pageData.name === 'Users' ? 'User Directory' : pageStore.pageData.name }}
      </h2>
      <nav class="hidden lg:flex items-center gap-6">
        <span
          class="font-label-sm text-label-sm text-primary dark:text-inverse-primary border-b-2 border-primary dark:border-inverse-primary pb-1 opacity-80 cursor-pointer"
        >
          {{ pageStore.pageData.name }}
        </span>
      </nav>
    </div>

    <!-- Right-side controls (Removed notifications, apps, and avatar thumbnail) -->
    <div class="flex items-center gap-4"></div>
  </header>
</template>

<style scoped></style>
