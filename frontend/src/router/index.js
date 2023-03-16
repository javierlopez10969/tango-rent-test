import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Prueba Frontend',
      component: HomeView
    },
    {
      path: '/calendar',
      name: 'calendar',
      component: () => import('../components/NewCalendar.vue')
    },
    {
      path: '/calendarCSS',
      name: 'calendar css',
      component: () => import('../components/Calendar.vue')
    },
  ]
})

export default router
