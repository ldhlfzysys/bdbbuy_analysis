// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import 'iview/dist/styles/iview.css'
import $ from 'jquery'
import iView from 'iview'
import inventoryWarning from './components/InventoryWarning/inventoryWarning.vue'
import saleData from './components/SaleData/saleData.vue'
import serverBaseURL from './globalConfig.js'


Vue.config.productionTip = false

Vue.use(VueRouter);
Vue.use(VueResource);
Vue.use(iView);

var route_base_path = process.env.NODE_ENV === 'development' ? '' : '/bdbbuyanalysis'

const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [
    {
      path: '/',
      component: saleData
    },
    {
      path: '/bdbbuyanalysis',
      component: saleData
    },
    {
      path: route_base_path + '/inventoryWarning',
      component: inventoryWarning
    },
    {
      path: route_base_path + '/saleData',
      component: saleData
    }

  ]
})
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  components: { App },
  template: '<App/>'
})
