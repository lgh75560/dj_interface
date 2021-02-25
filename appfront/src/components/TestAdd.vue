<template>

  <div class="tableMain">
    <el-form :model="test_add" class="demo-ruleForm" ref="form" label-position="left" :rules="rules">
      <el-row>
        <el-col :span="12">
          <el-form-item label="业务" label-width="100px">
            <el-select v-model="test_add.suit_id" placeholder="请先选择业务">
              <el-option v-for="item in suit" :key="item.s_id" :label="item.s_name" :value="item.s_id">
              </el-option>
            </el-select>
          </el-form-item>

        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="用例描述" label-width="100px">
            <el-input v-model="test_add.i_name" placeholder="输入用例描述"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="Url" label-width="100px" prop="i_url">
            <el-input type="textarea" v-model="test_add.i_url" placeholder="输入用例Url"></el-input>
          </el-form-item>

        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="请求方式" label-width="100px" prop="i_method">
            <el-select v-model="test_add.i_method" placeholder="请求方式">
              <el-option v-for="item in t_method" :key="item.value" :label="item.lable" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="header选择" label-width="100px" prop="i_header">
            <el-select v-model="test_add.i_header" placeholder="头部选择">
              <el-option v-for="item in t_h" :key="item.h_id" :label="item.h_name" :value="item.h_id">
              </el-option>
            </el-select>
          </el-form-item>

        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="post_json" label-width="100px">
            <el-input type='textarea' v-model="test_add.i_json" placeholder="填写json，如果有"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="post_data" label-width="100px">
            <el-input type='textarea' v-model="test_add.i_data" placeholder="填写data，如果有"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="源地址" label-width="100px">
            <el-input type='textarea' v-model="test_add.i_source_address" placeholder="接口出处"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="预期结果" label-width="100px" prop="i_expected">
            <el-input type='textarea' v-model="test_add.i_expected" placeholder="预期结果"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="替换字符串" label-width="100px">
            <el-input type='textarea' v-model="test_add.i_replace" placeholder="替换的字符串"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="匹配方式" label-width="100px" prop="i_match_type">

            <el-select v-model="test_add.i_match_type" placeholder="结果匹配方式">
              <el-option v-for="item in t_match_type" :key="item.value" :label="item.lable" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="3">
          <el-form-item>
            <el-button type="primary" @click="onSubmit">添加测试用例</el-button>
          </el-form-item>
        </el-col>
        <el-col :span="3">
          <el-form-item>
            <el-button type="success" @click="TestNew">测试运行</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-row>
      <el-table :data="test_lst" style="width: 100%" border>
        <el-table-column prop="s_id" label="用例id" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_id }}</template>
        </el-table-column>
        <el-table-column prop="s_name" label="用例名称" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_name }}</template>
        </el-table-column>
        <el-table-column prop="s_u" label="Url" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_url }}</template>
        </el-table-column>
        <el-table-column prop="s_m" label="Method" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_method }}</template>
        </el-table-column>
        <el-table-column prop="s_m" label="PostData" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_data }}</template>
        </el-table-column>
        <el-table-column prop="s_m" label="PostJson" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_json }}</template>
        </el-table-column>
        <el-table-column prop="s_m" label="Method" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_method }}</template>
        </el-table-column>
        <el-table-column prop="s_e" label="预期结果" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_expected }}</template>
        </el-table-column>
        <el-table-column prop="s_h" label="header" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_header_name }}</template>
        </el-table-column>
        <el-table-column prop="s_mu" label="替换字符串" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_replace_name }}</template>
        </el-table-column>
        <el-table-column prop="s_mm" label="匹配规则" min-width="100">
          <template slot-scope="scope"> {{ scope.row.t_match_type }}</template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>

</template>

<script>
  export default {
    name: 'Test',
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
        },
        rules: {
          suit_id: [{
            required: true,
            message: '请选择业务类型',
            trigger: 'change'
          }],
          // 这里的name 和v-model中的要一致，就是和data中绑定的字典name一致
          i_url: [{
            required: true,
            message: '请输入用例Url',
            trigger: 'blur'
          }],
          i_method: [{
            required: true,
            message: '请选择请求方式',
            trigger: 'change'
          }],
          i_header: [{
            required: true,
            message: '请选择header信息',
            trigger: 'change'
          }],
          i_expected: [{
            required: true,
            message: '请输入预期结果',
            trigger: 'blur'
          }],
          i_match_type: [{
            required: true,
            message: '请选择匹配方式',
            trigger: 'change'
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
      TestNew() {
        var is_continue = true;
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
          this.$http.post("http://127.0.0.1:8001/test_test/", this.test_add).then((response) => {

            this.$notify({
              title: '提示',
              message: response.data.msg,
              type: 'info'
            });
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
  .lable {
    width: 280px;
  }
</style>
