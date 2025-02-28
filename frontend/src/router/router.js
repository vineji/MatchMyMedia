import {createRouter, createWebHistory} from 'vue-router';

import SearchBooks from '@/components/SearchBooks.vue';
import LoginPage from '@/components/LoginPage.vue';


const routes = [
    { path: '/', name: 'Main Page', component: SearchBooks },
    { path: '/login', name: 'Login Page', component: LoginPage },
]

const router = createRouter({
    history : createWebHistory(),
    routes
})

export default router