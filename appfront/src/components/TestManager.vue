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
    <el-table :data="test_lst" style="width: 100%" border>
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
  </div>

</template>

<script>
  export default {
    name: 'TestList',
    data() {
      return {
        input: '',

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
        this.$http.get("http://127.0.0.1:8001/get_test/").then((response) => {

          console.log(response.data);
          this.test_lst = response.data.data;
          console.log(this.test_lst)
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
          this.$http.post("http://127.0.0.1:8001/get_test_info/", this.test_search).then((response) => {

            this.$notify({
              title: '提示',
              message: "查询成功",
              type: 'info'
            });
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
        this.$http.post("http://127.0.0.1:8001/save_test/", this.test_search).then((response) => {
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
        this.$http.post("http://127.0.0.1:8001/get_suit/", this.suit_add).then((response) => {
          this.suit = response.data.data;

        }).catch((error) => {
          console.log(error)
        })
      },
      InitHeader() {
        this.$http.post("http://127.0.0.1:8001/get_header/", this.suit_add).then((response) => {
          this.t_h = response.data.data;

        }).catch((error) => {
          console.log(error)
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .lable {
    width: 280px;
  }
</style>
