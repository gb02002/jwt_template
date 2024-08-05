import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import Orders from '@/views/Orders.vue';
import About from '@/views/AboutView.vue';
import Settings from '@/views/Settings.vue';
import Login from '../components/auth/Login.vue';
import Profile from '@/views/ProfileView.vue';


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/registration',
    name: 'registration',
    component: () => import('../components/auth/Register.vue')
  },

  { path: '/orders', component: Orders },
  { path: '/about', component: About },
  { path: '/settings', component: Settings },
  { path: '/login', component: Login },
  { path: '/profile', component: Profile },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
