<template>

  <div class="tableMain">
    <el-form :model="test_search" ref="form" label-position="left" :rules="rules">
      <el-form-item prop="test_info">
        <el-input v-model="test_search.test_info" placeholder="输入用例名称或者test_id"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click='TestSearch'>查询</el-button>
      </el-form-item>
    </el-form>

    <el-row>
      <el-table :data="test_lst" style="width: 100%;" :cell-style="grey_case" @row-dbclick.native="editCase">
        <el-table-column prop="s_id" label="用例id" min-width="100">
          <template slot-scope="scope"> {{ scope.row.id }}</template>
        </el-table-column>
        <el-table-column prop="s_name" label="是否可用" min-width="100">
          <template slot-scope="scope">
            <el-switch @change="changeStatus(scope.row)" v-model="scope.row.is_able"></el-switch>
          </template>

        </el-table-column>
        <el-table-column prop="s_name" label="用例名称" min-width="100">
          <template slot-scope="scope">
            <span v-if="!scope.row.isSet">{{ scope.row.case_name }}</span>
            <span v-else>
              <el-input v-model="scope.row.case_name"></el-input>
            </span>
          </template>
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
  </div>

</template>

<script>
  export default {
    name: 'TestList',
    data() {
      return {
        input: '',
        // 默认显示第几页
        currentPage: 1,
        // 总条数，根据接口获取数据长度(注意：这里不能为空)
        totalCount: 1,
        // 个数选择器（可修改）
        pageRange: [20, 40],
        // 默认每页显示的条数（可修改）
        PageSize: 20,

        test_lst: [],
        suit: {
          s_id: '',
          s_name: ''
        },
        t_method: [{
            lable: "GET",
            value: 0
          },
          {
            lable: "POST",
            value: 1
          }
        ],
        t_match_type: [{
            lable: "包含",
            value: 0
          },
          {
            lable: "相等",
            value: 1
          }
        ],
        t_h: {
          h_id: '',
          h_name: '',
          h_v: ''
        },
        test_search: {
          test_info: '',
        },
        rules: {
          test_info: [{
            required: true,
            message: '请输入内容',
            trigger: 'blur'
          }],
        }
      }
    },
    mounted: function() {
      this.ShowSuit();
      this.InitSelect();
      this.InitHeader();

    },
    methods: {
      ShowSuit() {
        this.$http.get(this.GLOBAL.BASE_URL + "get_test/?currentPage=" + this.currentPage + "&PageSize=" + this.PageSize).then((response) => {

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
      TestSearch() {
        var is_continue = true;
        this.test_lst = [];
        this.$refs.form.validate((valid) => {
          if (valid) {

          } else {
            is_continue = false
            this.$notify({
              title: '提示',
              message: '有信息为空',
              type: 'error'
            });
            return false;
          }
        });
        if (is_continue) {
          this.$http.post(this.GLOBAL.BASE_URL + "get_test_info/", this.test_search).then((response) => {

            this.$notify({
              title: '提示',
              message: "查询成功",
              type: 'info'
            });
            this.reset_pagination();
            this.test_lst = response.data.data;
            console.log(this.test_lst)

          }).catch((error) => {
            console.log(error)
          })
        }

      },
      onSubmit() {
        this.$refs.form.validate((valid) => {
          if (valid) {

          } else {
            console.log('error submit!!');
            return false;
          }
        });
        this.$http.post(this.GLOBAL.BASE_URL + "save_test/", this.test_search).then((response) => {
          this.$notify({
            title: '提示',
            message: response.data.msg,
            type: 'info'
          });

        }).catch((error) => {
          console.log(error)
        })
      },
      InitSelect() {
        this.$http.post(this.GLOBAL.BASE_URL + "get_suit/", this.suit_add).then((response) => {
          this.suit = response.data.data;

        }).catch((error) => {
          console.log(error)
        })
      },
      InitHeader() {
        this.$http.post(this.GLOBAL.BASE_URL + "get_header/", this.suit_add).then((response) => {
          this.t_h = response.data.data;

        }).catch((error) => {
          console.log(error)
        })
      },
      editCase(row, col, event) { // 可以修改
        console.log(1)
        row.isSet = false
      },
      changeStatus(row) {
        console.log(row)
        this.$http.post(this.GLOBAL.BASE_URL + "update_test/", row).then((response) => {
          if (response.data.retcode == 0) {
            this.$notify({
              title: '提示',
              message: response.data.msg,
              type: 'success'
            });
            this.msg = response.data.msg
          }
          if (response.data.retcode == -1) {
            this.$notify({
              title: '提示',
              message: response.data.msg,
              type: 'error'
            });
            this.msg = response.data.msg
          }

        }).catch((error) => {
          console.log(error)
        })
      },
      grey_case({
        row,
        column,
        rowIndex,
        columnIndex
      }) {
        if (row.is_able === false) {
          return {
            background: 'grey',
            color: 'white'
          }
        }
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
        this.$http.get(this.GLOBAL.BASE_URL + "get_test/?currentPage=" + this.currentPage + "&PageSize=" + this.PageSize).then((response) => {

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
      reset_pagination(){
        this.PageSize = 20
        this.totalCount = 1
        this.totalCount = 1
      },
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="css">

</style>
