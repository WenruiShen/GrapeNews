import Vue from 'vue'
import App from './App'
import router from './router'
import jQuery from 'jquery'
global.jQuery = jQuery
import 'bootstrap/dist/css/bootstrap.min.css'
// eslint-disable-next-line
var Bootstrap = require('bootstrap')
import axios from './http'
import store from './store/store'
Vue.config.productionTip = false

Vue.prototype.$axios = axios

/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>',
  router: router,
  store: store
})
