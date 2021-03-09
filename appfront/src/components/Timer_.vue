<template>

  <div class="home">

    <el-row>
      <el-row>
        <el-col :span="6">
          选择运行集
          <el-select v-model="choose_run_id" placeholder="选择运行集" @change="selectChanged">
            <el-option v-for="item in choose_lst" :key="item.r_id" :label="item.r_name" :value="item.r_id">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="6">
          选择定时间隔
          <el-input-number type="" v-model="interval_hour" placeholder="选择定时间隔(h)"></el-input-number>
          /小时
        </el-col>

        <el-button type="primary" @click="add_timer()">添加定时器</el-button>
      </el-row>
    </el-row>
    <el-table :data="timer_job_lst" style="width: 100%">

      <el-table-column prop="s_id" label="调用的运行集" min-width="100">
        <template slot-scope="scope"> {{ scope.row.id }}</template>
      </el-table-column>
      <el-table-column prop="s_name" label="绑定函数" min-width="100">
        <template slot-scope="scope"> {{ scope.row.name }}</template>
      </el-table-column>
      <el-table-column prop="s_name" label="定时函数传参" min-width="100">
        <template slot-scope="scope"> {{ scope.row.kwargs }}</template>
      </el-table-column>
      <el-table-column prop="s_name" label="运行间隔interval" min-width="100">
        <template slot-scope="scope"> {{ scope.row.interval }}</template>
      </el-table-column>
      <el-table-column prop="s_u" label="下次运行时间" min-width="100">
        <template slot-scope="scope"> {{ scope.row.next_run_time }}</template>
      </el-table-column>
      <el-table-column prop="s_u" label="是否只运行一次" min-width="100">
        <template slot-scope="scope"> {{ scope.row.run_once }}</template>
      </el-table-column>
      <el-table-column prop="s_u" label="是否移除" min-width="100">
        <template slot-scope="scope">
          <el-button @click='del_job(scope.row.id)' type="text">删除定时器</el-button>
        </template>

      </el-table-column>
    </el-table>
  </div>

</template>

<script>
  export default {
    name: 'TestTimer',
    data() {
      return {
        choose_run_id: '',
        choose_run_name: "",
        interval_hour: 3,
        select_data: [],
        choose_lst: [],
        timer_job_lst: [],
        bind_job_id: 0,
      }
    },
    mounted: function() {
      this.InitRun()
      this.InitTimerLst()
    },
    methods: {
      InitRun() {
        this.$http.get(this.GLOBAL.BASE_URL + "get_run/").then((response) => {

          console.log(response.data);
          this.choose_lst = response.data.data;
          console.log(this.choose_lst)
        }).catch((error) => {
          console.log(error)
        })
      },
      InitTimerLst() {
        this.$http.get(this.GLOBAL.BASE_URL + "get_timer_jobs/").then((response) => {

          console.log(response.data);
          this.timer_job_lst = response.data.data;
          console.log(this.timer_job_lst)
        }).catch((error) => {
          console.log(error)
        })
      },
      add_timer() {
        // 添加定时器
        if ('' === this.choose_run_id) {
          this.$notify({
            title: '提示',
            message: '请选项运行集',
            type: 'error'
          });
          return
        };

        this.$http.post(this.GLOBAL.BASE_URL + "add_timer_job/", {
          "run_id": this.choose_run_id,
          "interval_hour": this.interval_hour,
          "run_name": this.choose_run_name
        }).then((response) => {

          console.log(response.data);
          this.$notify({
            title: '成功',
            message: response.data.msg,
            type: 'success'
          });
          this.InitTimerLst()
        }).catch((error) => {
          console.log(error)
        })
      },
      del_job(val) {
        console.log("删除" + val)
        this.$confirm('此操作将任务状态改为删除状态, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          //点击确定的操作(调用接口)
          this.$http.post(this.GLOBAL.BASE_URL + "del_timer_jobs/", {
            "job_id": val
          }).then((response) => {
            console.log(response.data);
            this.$notify({
              title: '成功',
              message: response.data.msg,
              type: 'success'
            });
            this.InitTimerLst()
          }).catch((error) => {
            console.log(error)
          })
        }).catch(() => {
          //几点取消的提示
        });

      },
      selectChanged(value) {

        var obj = {}
        obj = this.choose_lst.find(function(item) {
          return item.r_id === value
        })
        console.log("lable " + obj.r_name)
        this.choose_run_name = obj.r_name
      },
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
