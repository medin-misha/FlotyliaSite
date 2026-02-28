<script setup>
import { ref } from 'vue'
import APIAuth from '../api/auth.js'

const login = ref(null)
const password = ref(null)

const loginUser = () => {
  APIAuth.login(login.value, password.value)
}
</script>

<template>
  <section>
    <h1>Login user: {{ login }}</h1>
    <form>
      <input v-model="login" type="text" placeholder="Login" />
      <input v-model="password" type="text" placeholder="Password" />
      <button
        @click.prevent="loginUser"
        :disabled="!login || !password"
        :class="{ disabled: !login || !password }"
      >
        login
      </button>
    </form>
  </section>
</template>

<style scoped>
section {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

h1 {
  margin-bottom: 1rem;
}
input {
  margin-bottom: 1rem;
}

button.disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
