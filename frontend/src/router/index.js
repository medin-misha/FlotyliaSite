import { createRouter, createWebHistory } from 'vue-router'
import homeView from '../views/homeView.vue'

const router = createRouter({
  history: createWebHistory(), // createWebHistory (отображает путь в адресной строке, без #) 
  // createWebHashHistory (отображает путь в адресной строке, с #)
  // createMemoryHistory (отображает путь в памяти)
  routes: [
    {
      path: "/",
      name: "home",
      component: homeView
    },
    {
      path: "/select-platform",
      name: "select-platform",
      component: () => import("../views/selectPlatformView.vue")
    },
    {
      path: "/form/:company",
      name: "form",
      component: () => import("../views/formView.vue"),
      props: true
    },
    {
      path: "/success/:company",
      name: "success",
      component: () => import("../views/successSendFormView.vue"),
      props: true
    }
  ]
})

export default router