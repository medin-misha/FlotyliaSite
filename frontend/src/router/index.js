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
      path: "/form",
      name: "form",
      component: () => import("../views/formView.vue"),
    },
    {
      path: "/success/:company",
      name: "success",
      component: () => import("../views/successSendFormView.vue"),
      props: true
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.name === 'form') {
    const isRegi = document.cookie
      .split('; ')
      .find(row => row.startsWith('is_regi='))
      ?.split('=')[1];

    if (isRegi === 'true') {
      const company = localStorage.getItem('mfs_platform') || 'bolt';
      next({ name: 'success', params: { company } });
      return;
    }
  }
  next();
});

export default router