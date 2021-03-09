<template>
  <div>
    <el-row>
      <el-table :data="test_result_lst" style="width: 100%" border :cell-style="green_padd_row">
        <el-table-column prop="suit_name" label="业务名称" min-width="100">
          <template slot-scope="scope"> {{ scope.row.suit_name }} </template>
        </el-table-column>
        <el-table-column prop="case_name" label="用例描述" min-width="100">
          <template slot-scope="scope"> {{ scope.row.case_name }} </template>
        </el-table-column>
        <el-table-column prop="case_method" label="请求方式" min-width="100">
          <template slot-scope="scope"> {{ scope.row.case_method }} </template>
        </el-table-column>
        <el-table-column prop="case_url" label="Url" min-width="100">
          <template slot-scope="scope"> {{ scope.row.case_url }} </template>
        </el-table-column>
        <el-table-column prop="result_match_type" label="结果匹配方式" min-width="100">
          <template slot-scope="scope"> {{ scope.row.result_match_type }} </template>
        </el-table-column>
        <el-table-column prop="result_response" label="response返回值" min-width="100">
          <template slot-scope="scope"> {{ scope.row.result_response }} </template>
        </el-table-column>
        <el-table-column prop="result_pass" label="结果" min-width="100">
          <template slot-scope="scope"> {{ scope.row.result_pass }} </template>
        </el-table-column>
        <el-table-column prop="start_time" label="开始时间" min-width="100">
          <template slot-scope="scope"> {{ scope.row.start_time }} </template>
        </el-table-column>
        <el-table-column prop="end_time" label="结束时间" min-width="100">
          <template slot-scope="scope"> {{ scope.row.end_time }} </template>
        </el-table-column>
        <el-table-column prop="request_time" label="响应时长" min-width="100">
          <template slot-scope="scope"> {{ scope.row.request_time }} </template>
        </el-table-column>
        <el-table-column prop="result_des" label="错误描述" min-width="100">
          <template slot-scope="scope"> {{ scope.row.result_des }} </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>


</template>

<script>
  import TestSuit from '@/components/TestSuitManager.vue';

  export default {
    name: 'TestSuitResult',
    components: {
      TestSuit
    },

    props: {
      "select_current_value": 0,
      required: true
    },
    watch: {
      // 草了，花费2个小时，组件传值，监听变化
      select_current_value: {
        immediate: true,
        handler: function() {
          this.getting()
        }
      }
    },
    data() {
      return {
        run_id2: "4",
        test_result_lst: []
      }
    },
    mounted: function() {

    },
    methods: {
      getting() {
        this.$http.post(this.GLOBAL.BASE_URL + "get_test_result/", {
          "run_id": this.select_current_value[0], "run_counter": this.select_current_value[1]
        }).then((response) => {

          console.log(response.data);
          this.test_result_lst = response.data.data;
          console.log(this.test_result_lst)
        }).catch((error) => {
          console.log(error)
        })
      },
      green_padd_row({
        row,
        column,
        rowIndex,
        columnIndex
      }) {

        if (row.result_pass === true && columnIndex === 6) {
          return {
            background: 'green',
            color: 'white'
          }
        }
        if (row.result_pass === false && columnIndex === 6) {
          return {
            background: 'red'
          }
        }
      },
    }
  }
</script>
