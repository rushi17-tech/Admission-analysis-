import { createRouter, createWebHistrory } from 'vue-router';
import Login from '/pages/Login.vue';

const routes = [{ path: '/login', component: Login}];

const router = createRouter({
    history: createWebHistrory(),
    routes,
});

export default router;