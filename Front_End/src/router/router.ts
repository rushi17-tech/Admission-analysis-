import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../pages/Login.vue';
import SignupPage from '../pages/signup.vue';
import HomePage from '../components/homepage.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/signup', name: 'Signup', component: SignupPage },
  { path: '/home', name: 'Home', component: HomePage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
