import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import TestSuit from '@/components/TestSuit'
import HeaderAdd from  '@/components/HeaderAdd'
import TestAdd from  '@/components/TestAdd'
import TestTable from  '@/components/TestTable'
import Home from  '@/components/Home'
import RunAdd from  '@/components/RunAdd'


const originalPush = Router.prototype.push

Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
};
Vue.use(Router);

export default new Router({
  mode: 'history',  //去掉url中的#
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      children: [
        {
          path: '/header',
          name: 'Header',
          component: HeaderAdd
        },
        {
          path: '/test',
          name: 'Test',
          component: TestAdd
        },
        {
          path: '/TestTable',
          name: 'TestTable',
          component: TestTable
        },
        {
          path: '/suit',
          name: 'Suit',
          component: TestSuit
        },
        {
          path: '/run',
          name: 'Run',
          component: RunAdd
        },
      ]
    }
  ],
})


