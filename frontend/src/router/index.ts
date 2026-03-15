import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/choice',
      name: 'choice',
      component: () => import('../views/ChoiceView.vue'),
    },
    {
      path: '/found-caregiver',
      name: 'found-caregiver',
      component: () => import('../views/FoundCaregiver.vue'),
    },
    {
      path: '/forms-page',
      name: 'forms-page',
      component: () => import('../views/FormsPage.vue'),
    },
  ],
})

export default router
