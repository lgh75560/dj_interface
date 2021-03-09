<template>

  <div>
    <div><h3>用例集--{{run_name}}, 第{{counter_id}}次数运行结果</h3> </div>
    <div id="chartColumn" style="width: 100%; height: 400px;"></div>

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
  import * as echarts from 'echarts';

  export default {
    name: 'TestSuitResultReport',
    data() {
      return {
        run_id2: "4",
        test_result_lst: [],
        run_id: 0,
        counter_id: 0,
        run_name: "",
      }
    },
    mounted: function() {
      this.run_id = this.$route.query.run_id
      this.counter_id = this.$route.query.counter_id
      console.log("接受的参数" + this.run_id)
      console.log("接受的参数" + this.counter_id)
      this.drawLine();
    },
    methods: {
      getting() {
        this.$http.post(this.GLOBAL.BASE_URL + "get_test_result/", {
          "run_id": this.run_id,
          "run_counter": this.counter_id
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
        // 通过的用例，绿色
        if (row.result_pass === true && columnIndex === 6) {
          return {
            background: 'green',
            color: 'white'
          }
        }
         // 失败用例，标红
        if (row.result_pass === false && columnIndex === 6) {
          return {
            background: 'red'
          }
        }
        // 大于3s的，标红
        if (row.request_time > 3 && columnIndex === 9) {
          return {
            background: 'red',
            color: 'white'
          }
        }
        if (row.request_time < 3 && columnIndex === 9) {
          return {
            background: 'green',
            color: 'white'
          }
        }
      },
      drawLine() {
        this.$http.post(this.GLOBAL.BASE_URL + "get_run_report/", {
          "run_id": this.run_id,
          "run_counter": this.counter_id
        }).then((response) => {

          this.chartColumn = echarts.init(document.getElementById('chartColumn'));
          this.run_name = response.data.run_name
          this.chartColumn.setOption({
            title: {
              text: '测试报告'
            },
            tooltip: {
              trigger: 'item',
              formatter: "{a} <br/>{b} : {d}%"
            },
            type: 'pie', // 设置图表类型为饼图
            radius: '55%', // 饼图的半径，外半径为可视区尺寸（容器高宽中较小一项）的 55% 长度。
            series: [{
              name: '测试报告结果',
              type: 'pie',
              clockwise: 'true',
              startAngle: '0',
              radius: '60%',
              center: ['50%', '50%'],
              // 设置颜色
              color: ['green', 'red', 'grey'],
              data: [{
                  value: response.data.pass_count,
                  name: '通过个数' + response.data.pass_count
                },
                {
                  value: response.data.fail_count,
                  name: '失败个数' + response.data.fail_count
                },
                {
                  value: response.data.unkown_count,
                  name: '未执行个数' + response.data.unkown_count
                }
              ],
            }]
          });

          this.test_result_lst = response.data.data;
        }).catch((error) => {
          console.log(error)
        })

      },
    }
  }
</script>
