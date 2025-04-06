import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import Dashboard from '../components/Dashboard.vue';
import CoinRank from '../components/CoinRank.vue';

const routes = [
    { 
        path: '/',
        name: 'Home',
        component: HomePage
    },
    { 
        path: '/dashboard',
        name: 'DashboardPage',
        component: Dashboard 
    },
    { 
        path: '/coinrank',
        name: 'CoinRank',
        component: CoinRank 
    },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;