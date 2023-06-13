import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  // Определите ваши маршруты здесь
  // Пример:
  {
    path: '/',
    name: 'Home',
    component: require('../components/ShortenLinkForm.vue').default
  },
  {
    path: '/404',
    name: '404',
    component: require('../components/Error404Page.vue').default
  },
  {
    path: '/collision',
    name: 'Collision',
    component: require('../components/CollisionPage.vue').default
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router