<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
  export default {
    name: 'App'
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

  /*这些是全局样式，直接改*/
  .el-input__inner {
    height: 30px;
    line-height: 30px;
  }

  .el-table {
    table-layout: fixed;
  }

  /* 设置table header的背景颜色 */
  .el-table__header th,
  .el-table__header tr {

    background-color: #17B3A3;
    color: black;
  }

  .el-select {
    //充满父元素（el-col）
    width: 100%;
  }

  /* 设置表单元个 */
  .el-table .cell {
    padding: 0.03125rem !important;
    word-break: keep-all;
    /* 不换行 */
    white-space: nowrap;
    /* 不换行 */
    overflow: hidden;
    /* 内容超出宽度时隐藏超出部分的内容 */
    text-overflow: ellipsis;
    /* 溢出时显示省略标记...；需与overflow:hidden;一起使用*/
  }

  /* 鼠标移入，展开内容*/
  .el-table .cell:hover {
    white-space: normal;
    overflow: auto;
    text-overflow: clip
  }

  .el-table__body td {}

  ,
  .el-table__body th {


  }

  /* 设置表头的高度 */

  .el-table__header td {
    height: 1.875rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  ,
  .el-table__header th {
    height: 1.875rem;
    padding: 6px 0px;

  }

  /* 设置分页器的高度 */

  .site-wrapper .el-pagination {

    margin-top: 5px;

    text-align: right;

  }

  .el-pager li.active {

    color: #080909;

    cursor: default;

    background-color: #17B3A3;

    border-radius: 2px;

  }

</style>
