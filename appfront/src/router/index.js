import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import TestSuitAdd from '@/components/TestSuitAdd'
import HeaderAdd from  '@/components/HeaderAdd'
import TestAdd from  '@/components/TestAdd'
import TestSuitManager from  '@/components/TestSuitManager'
import Home from  '@/components/Home'
import TestSuitRun from  '@/components/TestSuitRun'
import TestList from  '@/components/TestManager'
import TestSuitResultReport from  '@/components/TestSuitResultReport'
import Timer_ from  '@/components/Timer_'

const originalPush = Router.prototype.push

Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
};
Vue.use(Router);

export default new Router({
  // 这个鬼东西为了页面好看，但是刷新页面404，通用vue问题，解决起来要nginx什么的，麻烦，所以不要这个模式
  // mode: 'history',  //去掉url中的#

  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      children: [
        {
          path: '/test_list',
          name: 'TestManager',
          component: TestList
        },
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
          path: '/test_suit',
          name: 'TestSuit',
          component: TestSuitManager
        },
        {
          path: '/suit',
          name: 'TestSuitAdd',
          component: TestSuitAdd
        },
        {
          path: '/test_suit_run',
          name: 'TestSuitRun',
          component: TestSuitRun
        },

        {
          path: '/timer',
          name: 'Timer',
          component: Timer_
        },
      ]
    },
    {
      path: '/test_report',
      name: 'TestRport',
      component: TestSuitResultReport
    },
  ],
})
