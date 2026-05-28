<script setup>
import { ref } from 'vue'
import APIAuth from '../api/auth.js'

const login = ref('')
const password = ref('')
const isSubmitting = ref(false)

const loginUser = async () => {
  if (!login.value || !password.value) return
  isSubmitting.value = true
  try {
    await APIAuth.login(login.value, password.value)
  } catch (error) {
    console.error('Login failed:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <section class="relative flex min-h-screen w-full items-center justify-center overflow-hidden bg-[#111315] p-margin-mobile">
    <div class="absolute inset-x-0 top-0 h-1 bg-primary"></div>

    <div class="z-10 flex w-full max-w-[420px] flex-col items-center rounded-xl border border-white/10 bg-[#181b1f] p-stack-lg shadow-2xl transition-all">

      <!-- Brand Icon & Titles -->
      <div class="w-14 h-14 rounded-2xl bg-primary flex items-center justify-center text-white mb-6 shadow-lg shadow-primary/30">
        <span class="material-symbols-outlined text-[32px]" style="font-variation-settings: 'FILL' 1;">admin_panel_settings</span>
      </div>

      <h2 class="font-headline-sm text-headline-sm font-bold text-white mb-1">Панель управления</h2>
      <p class="text-xs text-secondary/60 mb-8 uppercase tracking-widest font-semibold">Flotylia Suite</p>

      <!-- Auth Form -->
      <form @submit.prevent="loginUser" class="w-full space-y-5">
        <!-- Login Input Group -->
        <div class="space-y-1">
          <label class="font-label-sm text-label-sm text-secondary/70 ml-1">Логин</label>
          <div class="relative">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-secondary/50 text-[18px]">person</span>
            <input
              v-model="login"
              type="text"
              name="username"
              autocomplete="username"
              placeholder="Введите логин"
              class="w-full h-12 pl-10 pr-4 rounded-xl bg-white/5 border border-white/10 text-white font-body-md text-body-md focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition-all placeholder-white/20"
            />
          </div>
        </div>

        <!-- Password Input Group -->
        <div class="space-y-1">
          <label class="font-label-sm text-label-sm text-secondary/70 ml-1">Пароль</label>
          <div class="relative">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-secondary/50 text-[18px]">lock</span>
            <input
              v-model="password"
              type="password"
              name="password"
              autocomplete="current-password"
              placeholder="Введите пароль"
              class="w-full h-12 pl-10 pr-4 rounded-xl bg-white/5 border border-white/10 text-white font-body-md text-body-md focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition-all placeholder-white/20"
            />
          </div>
        </div>

        <!-- Form Submission Button -->
        <button
          type="submit"
          :disabled="!login || !password || isSubmitting"
          :class="[
            'w-full h-12 rounded-xl bg-primary text-white font-bold flex items-center justify-center gap-2 transition-all shadow-md shadow-primary/20 mt-4',
            (!login || !password || isSubmitting) ? 'opacity-40 cursor-not-allowed' : 'hover:brightness-110 active:scale-[0.98]'
          ]"
        >
          <span class="font-label-md text-label-md">
            {{ isSubmitting ? 'Вход в систему...' : 'Войти в панель' }}
          </span>
          <span v-if="!isSubmitting" class="material-symbols-outlined text-[16px]">arrow_forward</span>
        </button>
      </form>

      <!-- Small Footer Disclaimer -->
      <p class="text-[11px] text-secondary/40 mt-8 text-center">
        Для внутреннего использования Flotylia Group
      </p>
    </div>
  </section>
</template>

<style scoped>
</style>
