// src/router/router.ts
import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../pages/login.vue'
import SignupPage from '../pages/signup.vue'
import HomePage from '../components/homepage.vue' // optional
import wrapbackground from '@/components/wrapbackground.vue'



const routes = [
  { path: '/', component: LoginPage }, // default route is Login
  { path: '/login', component: LoginPage },
  { path: '/signup', component: SignupPage },
  { path: '/home', component: HomePage }, // optional
  
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
