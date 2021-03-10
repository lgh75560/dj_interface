<template>

  <div class="home">
    <div>
      <el-row>
        <el-col :span="8">
          业务筛选
          <el-select v-model="choose_suit" placeholder="请先选择业务" @change="suit_change">
            <el-option v-for="item in suit" :key="item.s_id" :label="item.s_name" :value="item.s_id">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="8">
          是否包含留咨接口
          <el-select v-model="choose_is_send_phone" placeholder="是否包含留咨接口" @change="suit_change">
            <el-option v-for="item in t_is_send_phone" :key="item.value" :label="item.lable" :value="item.value">
            </el-option>
          </el-select>
        </el-col>
      </el-row>
    </div>
    <el-row>
      <el-table :data="test_lst" style="width: 100%" border @selection-change="handleSelectionChange" :row-key="rowKey">
        <el-table-column type="selection" v-model="multipleSelection" width="55" :reserve-selection="true">
        </el-table-column>
        <el-table-column prop="s_id" label="用例id" min-width="100">
          <template slot-scope="scope"> {{ scope.row.id }}</template>
        </el-table-column>
        <el-table-column prop="s_name" label="用例名称" min-width="100">
          <template slot-scope="scope"> {{ scope.row.case_name }}</template>
        </el-table-column>
        <el-table-column prop="s_u" label="Url" min-width="100">
          <template slot-scope="scope"> {{ scope.row.case_url }}</template>
        </el-table-column>
        <el-table-column prop="s_m" label="Method" min-width="100">
          <template slot-scope="scope"> {{ scope.row.case_method }}</template>
        </el-table-column>
        <el-table-column prop="s_m" label="PostData" min-width="100">
          <template slot-scope="scope"> {{ scope.row.case_data }}</template>
        </el-table-column>
        <el-table-column prop="s_m" label="PostJson" min-width="100">
          <template slot-scope="scope"> {{ scope.row.case_json }}</template>
        </el-table-column>
        <el-table-column prop="s_e" label="预期结果" min-width="100">
          <template slot-scope="scope"> {{ scope.row.case_expected }}</template>
        </el-table-column>
        <el-table-column prop="s_h" label="header" min-width="100">
          <template slot-scope="scope"> {{ scope.row.case_header_name }}</template>
        </el-table-column>
        <el-table-column prop="s_mu" label="替换字符串" min-width="100">
          <template slot-scope="scope"> {{ scope.row.replace_name }}</template>
        </el-table-column>
        <el-table-column prop="s_mm" label="匹配规则" min-width="100">
          <template slot-scope="scope"> {{ scope.row.result_match_type }}</template>
        </el-table-column>
      </el-table>
    </el-row>
    <div class="tabListPage">
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
        :page-sizes="pageRange" :page-size="PageSize" layout="total, sizes, prev, pager, next, jumper" :total="totalCount">
      </el-pagination>
    </div>

    <el-row :gutter="10" align="middle">
      <el-col :span="8">
        <el-input v-model="run_name" placeholder="输入运行集名称"></el-input>
      </el-col>
      <el-col :span="8">
        <el-button type="primary" @click="add_run()">添加运行集</el-button>
      </el-col>

    </el-row>
  </div>

</template>

<script>
  export default {
    name: 'TestSuitManager',
    data() {
      return {
        input: '',
        test_lst: [],
        // 默认显示第几页
        currentPage: 1,
        // 总条数，根据接口获取数据长度(注意：这里不能为空)
        totalCount: 1,
        // 个数选择器（可修改）
        pageRange: [20, 40],
        // 默认每页显示的条数（可修改）
        PageSize: 20,

        //
        run_name: '',
        choose_run_id: '',
        choose_is_send_phone: "",
        run_id: '',
        choose_lst: [],
        suit: {
          s_id: '',
          s_name: ''
        },
        choose_suit: "",
        t_method: [{
            lable: "GET",
            value: 1
          },
          {
            lable: "POST",
            value: 2
          }
        ],
        t_is_send_phone: [{
            lable: "是",
            value: 1
          },
          {
            lable: "否",
            value: 0
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
      this.InitSuitSelect()
    },

    methods: {
      InitSelect() {
        this.$http.get(this.GLOBAL.BASE_URL + "get_test/?currentPage=" + this.currentPage + "&PageSize=" + this.PageSize)
          .then((response) => {

            if (response.data.retcode == 0) {
              this.$notify({
                title: '提示',
                message: "拉取数据成功",
                type: 'success'
              });
              this.test_lst = response.data.data
              this.totalCount = response.data.total
            }
            if (response.data.retcode == -1) {
              this.$notify({
                title: '提示',
                message: response.data.msg,
                type: 'error'
              });
            }
          }).catch((error) => {
            console.log(error)
          })
      },
      // 分页勾选，不清空
      // 来源：https://blog.csdn.net/Ms_alinda/article/details/102861781
      rowKey (row) {
        console.log("?? id" + row.id);
      return row.id
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
          temp.push(this.multipleSelection[i].id)
        }
        this.selected_id_lst = temp;
        console.log(this.selected_id_lst)
      },
      // 每页显示的条数
      handleSizeChange(val) {
        // 改变每页显示的条数
        this.PageSize = val
        // 点击每页显示的条数时，显示第一页
        this.getData(val, 1)
        // 注意：在改变每页显示的条数时，要将页码显示到第一页
        this.currentPage = 1
      },
      // 显示第几页
      handleCurrentChange(val) {
        // 改变默认的页数
        this.currentPage = val
        // 切换页码时，要获取每页显示的条数
        this.getData(this.PageSize, (val) * (this.pageSize))
      },
      created: function() {
        this.getData(this.PageSize, this.currentPage)
      },
      // 将页码，及每页显示的条数以参数传递提交给后台
      getData(n1, n2) {

        this.$http.get(this.GLOBAL.BASE_URL + "get_test/?currentPage=" + this.currentPage + "&PageSize=" + this.PageSize + "&suit="+this.choose_suit + "&is_send_phone=" + this.choose_is_send_phone)
          .then((response) => {

            if (response.data.retcode == 0) {
              this.$notify({
                title: '提示',
                message: "拉取数据成功",
                type: 'success'
              });
              this.test_lst = response.data.data
              this.totalCount = response.data.total
            }
            if (response.data.retcode == -1) {
              this.$notify({
                title: '提示',
                message: response.data.msg,
                type: 'error'
              });
            }
          }).catch((error) => {
            console.log(error)
          })
      },
      reset_pagination() {
        this.PageSize = 20
        this.totalCount = 1
        this.totalCount = 1
      },
      InitSuitSelect() {
        this.$http.post(this.GLOBAL.BASE_URL + "get_suit/", this.suit_add).then((response) => {
          this.suit = response.data.data;

        }).catch((error) => {
          console.log(error)
        })
      },
      suit_change(val) {
        this.currentPage = 1

        this.$http.get(this.GLOBAL.BASE_URL + "get_test/?currentPage=" + this.currentPage + "&PageSize=" + this.PageSize + "&suit="+this.choose_suit + "&is_send_phone=" + this.choose_is_send_phone)
          .then((response) => {

            if (response.data.retcode == 0) {
              this.$notify({
                title: '提示',
                message: "拉取数据成功",
                type: 'success'
              });
              this.test_lst = response.data.data
              this.totalCount = response.data.total
            }
            if (response.data.retcode == -1) {
              this.$notify({
                title: '提示',
                message: response.data.msg,
                type: 'error'
              });
            }
          }).catch((error) => {
            console.log(error)
          })
      },
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
