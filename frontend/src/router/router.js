import {createRouter, createWebHistory} from 'vue-router';

import SearchBooks from '@/components/SearchBooks.vue';
import DashboardPage from '@/components/DashboardPage.vue';


const routes = [
    { path: '/', name: 'Main Page', component: SearchBooks },
    { path: '/dashboard', name: 'Dashboard Page', component: DashboardPage },
]

const router = createRouter({
    history : createWebHistory(),
    routes
})

export default router