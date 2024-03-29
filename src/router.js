import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Api from './views/Api.vue'
import Ping from '@/components/Ping';
import Books from '@/components/Books';
import Order from '@/components/Order';
import OrderComplete from '@/components/OrderComplete';

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/api',
      name: 'api',
      component: Api
    },
    {
      path: '/books',
      name: 'Books',
      component: Books,
    },
    {
      path: '/order/:id',
      name: 'Order',
      component: Order,
    },
    {
      path: '/complete/:id',
      name: 'OrderComplete',
      component: OrderComplete,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ]
})
