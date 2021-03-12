<template>
  <el-container>
    <el-aside class="aside">
      <el-menu :default-active="this.$route.path" :router="true">
        <el-menu-item v-for="(item,i) in navList" :key="i" :index="item.name">
          {{ item.navItem }}
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main>
      <!-- 靠了，这里和路由index.js。添加到子控件是一起的，否则点击菜单就是新开页面-->
      <router-view />
    </el-main>

  </el-container>

</template>

<script>
  export default {
    name: "Home",
    data() {
      return {
        navList: [{
            name: '/test_list',
            navItem: '用例管理'
          },{
            name: '/test',
            navItem: '用例添加'
          },
          {
            name: '/test_edit',
            navItem: '编辑用例'
          },
          {
            name: '/test_suit',
            navItem: '用例集合添加'
          },
          {
            name: '/header',
            navItem: '头部添加'
          },
          {
            name: '/suit',
            navItem: '业务添加'
          },
          {
            name: '/test_suit_run',
            navItem: '执行运行集'
          },
          {
            name: '/timer',
            navItem: '添加定时器'
          },
        ],
      }
    },

    methods: {

    },
  }
</script>
<style scoped>
  .container {
    height: 100vh;
    font-size: 15px;
  }

  .header {
    background: #212121;
    color: #fff;
  }

  .aside {
    background: #3a3a3a;
    color: #fff;
    height: 100%;
  }

  .el-submenu .el-menu-item {
    text-align: right;
  }
</style>
