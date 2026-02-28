<script setup>
import { ref, markRaw } from 'vue'
import { useAuthStore } from '../stores/auth.js'
import { usePageStore } from '../stores/page.js'
import { useStatesStore } from '../stores/states.js'

import { userSchema, userCreateSchema } from '../forms/userFrom.js'
import { adminSchema, adminCreateSchema } from '../forms/adminForm.js'
import { contractSchema, contractCreateSchema } from '../forms/contractForm.js'
import { transportSchema, transportCreateSchema } from '../forms/transportForm.js'
import { productSchema, productCreateSchema } from '../forms/productForm.js'

const authStore = useAuthStore()
const pageStore = usePageStore()
const statesStore = useStatesStore()
const menu = [
  {
    url: userSchema.endpoint,
    name: 'Users',
    isActive: false,
    schema: markRaw(userSchema),
    createSchema: markRaw(userCreateSchema),
  },
  {
    url: adminSchema.endpoint,
    name: 'Admins',
    isActive: false,
    schema: markRaw(adminSchema),
    createSchema: markRaw(adminCreateSchema),
  },
  {
    url: contractSchema.endpoint,
    name: 'Contracts',
    isActive: false,
    createSchema: markRaw(contractCreateSchema),
    schema: markRaw(contractSchema),
  },
  {
    url: transportSchema.endpoint,
    name: 'Transports',
    isActive: false,
    createSchema: markRaw(transportCreateSchema),
    schema: markRaw(transportSchema),
  },
  {
    url: productSchema.endpoint,
    name: 'Products',
    isActive: false,
    createSchema: markRaw(productCreateSchema),
    schema: markRaw(productSchema),
  },
]

const activeIndex = ref(null)
const setPage = (index) => {
  activeIndex.value = index
  pageStore.setPage(menu[index].url, menu[index].name, menu[index].createSchema, menu[index].schema)
  statesStore.setTableState()
  pageStore.resetSearchParams()
}
</script>

<template>
  <aside>
    <h1>Admin Panel</h1>
    <div class="side-bar-line"></div>
    <ul>
      <li
        tabindex="0"
        v-for="(item, index) in menu"
        :key="index + item.name"
        :class="{ active: activeIndex === index }"
        @click="setPage(index)"
      >
        {{ item.name }}
      </li>
    </ul>
    <button @click="authStore.logout()">Logout</button>
  </aside>
</template>

<style scoped>
aside {
  width: clamp(200px, 15%, 250px);
  background: var(--slidebar-bg);
  min-height: 100dvh;
  padding: 1rem 1rem 0;
  border-right: 1px solid var(--slidebar-item-hover-bg);
  display: flex;
  flex-direction: column;
}
.side-bar-line {
  width: 100%;
  height: 3px;
  background: var(--slidebar-item-hover-bg);
  margin-bottom: 1rem;
  margin-top: 0.3rem;
}
ul {
  list-style: none;
}
li {
  display: flex;
  cursor: pointer;
  text-align: left;
  align-items: center;
  justify-content: flex-start;
  padding: 0.5rem;
  font-size: 20px;
  font-weight: 500;
  transition: background-color 0.3s ease;
  border-radius: 1rem;
}
li:hover {
  background: var(--slidebar-item-hover-bg);
}

li.active {
  background: var(--slidebar-item-active-bg);
}

h1 {
  font-size: 1.5rem;
  font-weight: 800;
}
button {
  width: 100%;
  margin-top: auto;
  margin-bottom: 1rem;
}
</style>
