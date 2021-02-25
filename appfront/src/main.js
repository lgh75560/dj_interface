// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
// 引用包
import ElementUI from 'element-ui'
import '../node_modules/element-ui/lib/theme-chalk/index.css'
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

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

