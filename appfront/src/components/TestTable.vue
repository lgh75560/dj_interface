<template>

  <div class="home">
    <el-row>
      <el-table :data="test_lst" style="width: 100%" border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55">
        </el-table-column>
        <el-table-column prop="s_id" label="用例id" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_id }} </template>
        </el-table-column>
        <el-table-column prop="s_name" label="用例名称" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_name }} </template>
        </el-table-column>
        <el-table-column prop="s_u" label="Url" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_url }} </template>
        </el-table-column>
        <el-table-column prop="s_m" label="Method" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_method }} </template>
        </el-table-column>
        <el-table-column prop="s_e" label="预期结果" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_expected }} </template>
        </el-table-column>
        <el-table-column prop="s_h" label="header" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_header_name }} </template>
        </el-table-column>
        <el-table-column prop="s_mm" label="匹配规则" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_match_type }} </template>
        </el-table-column>
      </el-table>
    </el-row>
    <el-row :gutter="10" align="middle">
      <div>
        <el-col :span="6" align="middle">
          <el-input v-model="run_name" placeholder="输入运行集名称"></el-input>
        </el-col>
      </div>

    </el-row>
    <el-row>
      <el-button type="primary" @click="add_run()">添加运行集</el-button>
      <el-row>
        选择将要运行的集合
        <el-select v-model="choose_run_id" placeholder="也可以手动筛选运行集" change="selectChanged">
          <el-option v-for="item in choose_lst" :key="item.r_id" :label="item.r_name" :value="item.r_id">
          </el-option>
        </el-select>
        <el-button type="primary" @click="run_run()">执行所选运行集</el-button>
      </el-row>


    </el-row>
    <el-row>
      <TestResultTemp :run_id="choose_run_id"></TestResultTemp>
    </el-row>

  </div>

</template>

<script>
  import TestResultTemp from '@/components/TestResultView.vue';

  export default {
    name: 'TestTable',
    components: {
      TestResultTemp
    },
    data() {
      return {
        input: '',
        test_lst: [],
        run_name: '',
        choose_run_id: '',
        run_id: '',
        choose_lst: [],
        suit: {
          s_id: '',
          s_name: ''
        },
        t_method: [{
            lable: "GET",
            value: 1
          },
          {
            lable: "POST",
            value: 2
          }
        ],
        t_match_type: [{
            lable: "包含",
            value: 1
          },
          {
            lable: "相等",
            value: 2
          }
        ],
        t_h: {
          h_id: '',
          h_name: '',
          h_v: ''
        },
        test_add: {
          t_id: '',
          suit_id: '',
          i_name: '',
          i_url: '',
          i_header: '',
          i_method: '',
          i_json: '',
          i_data: '',
          i_source_address: '',
          i_expected: '',
          i_match_type: '',
          i_replace: ''
        },
        multipleSelection: [],
        selected_id_lst: []
      }
    },
    mounted: function() {
      this.InitSelect();
      this.InitRun();
    },

    methods: {
      InitSelect() {
        this.$http.get("http://127.0.0.1:8001/get_test/").then((response) => {

          console.log(response.data);
          this.test_lst = response.data.data;
          console.log(this.test_lst)
        }).catch((error) => {
          console.log(error)
        })
      },
      InitRun() {
        this.$http.get("http://127.0.0.1:8001/get_run/").then((response) => {

          console.log(response.data);
          this.choose_lst = response.data.data;
          console.log(this.choose_lst)
        }).catch((error) => {
          console.log(error)
        })
      },
      binde_event(data) {
        this.$emit("getting", this.run_id)
      },
      selectChanged(value) {
        console.log("选择的value" + value);
        // 向其他组件发射信息，调用他函数
        this.updata_run_result();

      },
      updata_run_result() {
        this.$http.post("http://127.0.0.1:8001/get_run/", {
          "run_id": this.choose_run_id
        }).then((response) => {
          console.log(response.data);
          this.test_lst = response.data.data;
          console.log(this.test_lst)
        }).catch((error) => {
          console.log(error)
        })
      },
      add_run() {
        if ('' === this.run_name) {
          this.$notify({
            title: '提示',
            message: '请选输入运行集名称',
            type: 'error'
          });
          return
        };
        if (this.selected_id_lst == undefined || this.selected_id_lst.length <= 0) {
          this.$notify({
            title: '提示',
            message: '勾选为空，无法提交',
            type: 'error'
          });
          return
        };
        this.$http.post("http://127.0.0.1:8001/add_run/", {
          "test_ids": this.selected_id_lst,
          "run_name": this.run_name
        }).then((response) => {

          console.log(response.data);
          this.$notify({
            title: '成功',
            message: response.data.msg,
            type: 'success'
          });
        }).catch((error) => {
          console.log(error)
        })
      },
      run_run() {
        if (this.choose_run_id == undefined || this.choose_run_id == '') {
          this.$notify({
            title: '提示',
            message: "请先下拉选择运行集",
            type: 'error'
          });
          return;
        };
        this.$http.post("http://127.0.0.1:8001/run_result/", {
          "run_id": this.choose_run_id
        }).then((response) => {

          console.log(response.data);
          this.$notify({
            title: '提示',
            message: response.data.msg,
            type: 'info'
          });
          this.updata_run_result();
        }).catch((error) => {
          console.log(error)
        })
      },
      filterMethod(query, item) {
        console.log(item)
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;

        // 获取选中数据
        console.log(this.multipleSelection);
        var temp = [];
        for (var i = 0; i < this.multipleSelection.length; i++) {
          // vue 中，用append会报错，用push
          temp.push(this.multipleSelection[i].t_id)
        }
        this.selected_id_lst = temp;
        console.log(this.selected_id_lst)
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
