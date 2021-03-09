// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
// 引用包
import ElementUI from 'element-ui'

import '../node_modules/element-ui/lib/theme-chalk/index.css'
import Vue from 'vue'
import App from './App'

// 引用echarts
import echarts from 'echarts'

import router from './router'
// 自定义设置的全局变量
import global_ from '../config/global.js'
Vue.prototype.GLOBAL = global_;

// get 使用到的
import axios from 'axios'
import VueAxios from 'vue-axios'
import qs from 'qs'
Vue.prototype.$qs = qs

Vue.prototype.axios = axios;
Vue.use(VueAxios, axios);

Vue.config.productionTip = false
// 添加组件
Vue.use(ElementUI)

Vue.config.productionTip = false
Vue.prototype.$echarts = echarts

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

