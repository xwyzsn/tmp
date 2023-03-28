import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: ()=>import('../views/login/LoginView.vue')
    },

    {
      path:'/home',
      name:'home',
      component:()=>import('../views/home/homeView.vue'),
      redirect:'/home/order',
      children:[
        {path:'order',name:'order',component:()=>import('../views/order/orderView.vue')},
        {path:'index',name:'index',component:()=>import('../views/index/index.vue')},
        {path:'food',name:'food',component:()=>import('../views/food/FoodView.vue')},
        {path:'history',name:'history',component:()=>import('../views/history/history.vue')},
      ]
    }
  ]
})

export default router
