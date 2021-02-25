<template>

  <div class="home">
    <el-row>
      <el-button type="primary">没有用的按钮</el-button>
    </el-row>

    <el-row>
      <el-table :data="test_lst" style="width: 100%" border>
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
  </div>

</template>

<script>
  export default {
    name: 'Run',
    data() {
      return {
        input: '',
        test_lst: [

        ],

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
      onSubmit() {
        console.log(this.test_add);
        this.$http.post("http://127.0.0.1:8001/save_test/", this.test_add).then((response) => {
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

</style>
