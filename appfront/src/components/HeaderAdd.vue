<template>

  <div class="home">
    <el-form :inline="true" :model="head_add" class="demo-form-inline">
      <el-form-item label="添加header">
        <el-input v-model="head_add.header_name" placeholder="输入header名称"></el-input>
        <el-input type="textarea" v-model="head_add.header_value" placeholder="输入header值"></el-input>
        <el-button type="primary" @click="onSubmit">添加业务</el-button>
      </el-form-item>

    </el-form>

    <el-row>
      <el-table :data="header_lst" style="width: 100%" border>
        <el-table-column prop="s_id" label="header_id" min-width="100">
          <template slot-scope="scope"> {{ scope.row.h_id }} </template>
        </el-table-column>
        <el-table-column prop="s_name" label="header_name" min-width="100">
          <template slot-scope="scope"> {{ scope.row.h_name }} </template>
        </el-table-column>
        <el-table-column prop="s_name" label="header_value" min-width="100">
          <template slot-scope="scope"> {{ scope.row.h_v }} </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>

</template>

<script>
  export default {
    name: 'Header',
    data() {
      return {
        input: '',
        header_lst: [],
        head_add: {
          header_name: '',
          header_value: ''
        }
      }
    },
    mounted: function() {
      this.ShowSuit()
    },
    methods: {
      ShowSuit() {
        this.$http.get("http://127.0.0.1:8001/get_header/").then((response) => {

          console.log(response.data);
          this.header_lst = response.data.data;
          console.log(this.header_lst)
        }).catch((error) => {
          console.log(error)
        })
      },
      onSubmit() {
        console.log(this.head_add);
        this.$http.post("http://127.0.0.1:8001/save_header/", this.head_add).then((response) => {
          this.$notify({
            title: '提示',
            message: response.data.msg,
            type: 'info'
          });

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
