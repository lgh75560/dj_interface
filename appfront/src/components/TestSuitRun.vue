<template>

  <div class="home">

    <el-row>
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
      选择查看结果
      <el-cascader v-model="select_current_value" :options="select_data" placeholder="请选择" :show-all-levels="false"
        :key="isRescourceShow" @change="handlechange">
      </el-cascader>
      <el-button type="infor" @click="jump_page()">查看此报告</el-button>
    </el-row>
    <el-row>
      <TestSuitResultTable :select_current_value="select_current_value"></TestSuitResultTable>
    </el-row>

  </div>

</template>

<script>
  import TestSuitResultTable from '@/components/TestSuitResultTable.vue';

  export default {
    name: 'TestSuitRun',
    components: {
      TestSuitResultTable
    },
    data() {
      return {
        input: '',
        test_lst: [],
        isRescourceShow: 0,
        run_name: '',
        choose_run_id: '',
        run_id: '',
        choose_lst: [],
        select_data: [],
        // 级联插件，绑定值，要[]
        select_current_value: [],
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
      this.InitRun()
      this.InitSelect()
    },

    watch: {
      select_data() {
        ++this.isRescourceShow
      }
    },

    methods: {
      InitSelect() {
        this.$http.get(this.GLOBAL.BASE_URL + "get_run_select/").then((response) => {

          console.log(response.data);
          this.select_data = response.data.data;
          console.log(this.test_lst)
        }).catch((error) => {
          console.log(error)
        })
      },

      InitRun() {
        this.$http.get(this.GLOBAL.BASE_URL + "get_run/").then((response) => {

          console.log(response.data);
          this.choose_lst = response.data.data;
          console.log(this.choose_lst)
        }).catch((error) => {
          console.log(error)
        })
      },
      handlechange(value) {
        console.log("级联菜单" + value) // 这里的值会输出 value 的一个数组
        this.select_current_value = value
        this.updata_run_result()
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
        this.$http.post(this.GLOBAL.BASE_URL + "get_run/", {
          "run_id": this.select_current_value[0],
          "run_counter": this.select_current_value[1]
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
        this.$http.post(this.GLOBAL.BASE_URL + "add_run/", {
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
        this.$http.post(this.GLOBAL.BASE_URL + "run_result/", {
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
      },
      jump_page() {
        if(this.select_current_value!= []){
          console.log(this.select_current_value)
          let {href} = this.$router.resolve({
            path: '/test_report',
            name: 'TestRport',
            query: {
              run_id: this.select_current_value[0],
              counter_id: this.select_current_value[1]
            }
          });
          window.open(href, '_blank');
        }
      },
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
