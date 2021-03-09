<template>

  <div class="tableMain">
    <el-form :model="test_add" class="demo-ruleForm" ref="form" label-position="left" :rules="rules" size="small">
      <el-row>
        <el-col :span="8">
          <el-form-item label="业务" label-width="100px">
            <el-select v-model="test_add.suit_id" placeholder="请先选择业务">
              <el-option v-for="item in suit" :key="item.s_id" :label="item.s_name" :value="item.s_id">
              </el-option>
            </el-select>
          </el-form-item>

        </el-col>
      </el-row>

      <el-row>
        <el-col :span="8">
          <el-form-item label="用例描述" label-width="100px">
            <el-input v-model="test_add.i_name" placeholder="输入用例描述"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">
          <el-form-item label="Url" label-width="100px" prop="i_url">
            <el-input v-model="test_add.i_url" placeholder="输入用例Url"></el-input>
          </el-form-item>

        </el-col>
      </el-row>

      <el-row>
        <el-col :span="8">
          <el-form-item label="请求方式" label-width="100px" prop="i_method">
            <el-select v-model="test_add.i_method" placeholder="请求方式">
              <el-option v-for="item in t_method" :key="item.value" :label="item.lable" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">
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
            <el-input type='textarea' v-model="test_add.i_json" @change.native="clearLineBreak" placeholder="填写json，如果有"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="post_data" label-width="100px">
            <el-input type='textarea' v-model="test_add.i_data" @change.native="clearLineBreak" placeholder="填写data，如果有"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="源地址" label-width="100px">
            <el-input type='textarea' v-model="test_add.i_source_address" placeholder="接口出处" @change.native="clearLineBreak"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="预期结果" label-width="100px" prop="i_expected">
            <el-input type='textarea' v-model="test_add.i_expected" placeholder="预期结果" @change.native="clearLineBreak"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="替换字符串" label-width="100px">
            <el-input type='textarea' v-model="test_add.i_replace" placeholder="替换的字符串" @change.native="clearLineBreak"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="8">
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
      <el-form-item>
        <el-input type='textarea' v-model="msg" placeholder="测试运行结果输出" rows="4"></el-input>
      </el-form-item>
    </el-form>
  </div>

</template>

<script>
  export default {
    name: 'Test',
    data() {
      return {
        input: '',
        test_lst: [],
        msg: '',
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
        this.$http.get(this.GLOBAL.BASE_URL + "get_test/").then((response) => {

          console.log(response.data);
          this.test_lst = response.data.data;
          console.log(this.test_lst)
        }).catch((error) => {
          this.$notify({
            title: '提示',
            message: "请求异常",
            type: 'error'
          });
        })
      },
      clearLineBreak(e) {
          // `e` 是原生 DOM 事件
          // @change.native 需要事件.native，e.target才有值
          var val = e.target.value;
          // alert(e.target.value)
          console.log(val)
          //获得粘贴的文字
          val = val.replace(/\r\n/g,"")
          val = val.replace(/\n/g,"");
          console.log(val)
          e.target.value = val
      },
      TestNew() {
        var is_continue = true;
        this.msg = ""
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
          this.$http.post(this.GLOBAL.BASE_URL + "test_test/", this.test_add).then((response) => {

            if (response.data.retcode == 0){
              this.$notify({
                title: '提示',
                message: '测试正常',
                type: 'success'
              });
              this.msg = response.data.msg
            }
            if (response.data.retcode == -1){
              this.$notify({
                title: '提示',
                message: "返回异常",
                type: 'error'
              });
              this.msg = response.data.msg
            }
          }).catch((error) => {
            this.$notify({
              title: '提示',
              message: "请求异常",
              type: 'error'
            });
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
        this.$http.post(this.GLOBAL.BASE_URL + "save_test/", this.test_add).then((response) => {
          this.$notify({
            title: '提示',
            message: response.data.msg,
            type: 'info'
          });

        }).catch((error) => {
          this.$notify({
            title: '提示',
            message: "请求异常",
            type: 'error'
          });
        })
      },
      InitSelect() {
        this.$http.post(this.GLOBAL.BASE_URL + "get_suit/", this.suit_add).then((response) => {
          this.suit = response.data.data;

        }).catch((error) => {
          this.$notify({
            title: '提示',
            message: "请求异常",
            type: 'error'
          });
        })
      },
      InitHeader() {
        this.$http.post(this.GLOBAL.BASE_URL + "get_header/", this.suit_add).then((response) => {
          this.t_h = response.data.data;

        }).catch((error) => {
          this.$notify({
            title: '提示',
            message: "请求异常",
            type: 'error'
          });
        })
      },
    }
  }
</script>

<!-- 设置全局样式 -->
<style lang="css">
</style>
