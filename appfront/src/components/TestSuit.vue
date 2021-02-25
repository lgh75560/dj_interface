<template>

  <div class="home">
    <el-form :inline="true" :model="suit_add" class="demo-form-inline">
      <el-form-item label="输入业务名称">
        <el-input v-model="suit_add.suit_name" placeholder="输入业务名称"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">添加业务</el-button>
      </el-form-item>
    </el-form>

    <el-row>
      <el-table :data="suit_lst" style="width: 100%" border>
        <el-table-column prop="s_id" label="业务id" min-width="100">
          <template slot-scope="scope"> {{ scope.row.s_id }} </template>
        </el-table-column>
        <el-table-column prop="s_name" label="业务名称" min-width="100">
          <template slot-scope="scope"> {{ scope.row.s_name }} </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>

</template>

<script>
  export default {
    name: 'Suit',
    data() {
      return {
        input: '',
        suit_lst: [],
        suit_add: {
          suit_name: ''
        }
      }
    },
    mounted: function() {
      this.ShowSuit()
    },
    methods: {
      ShowSuit() {
        this.$http.get("http://127.0.0.1:8001/get_suit").then((response) => {

          console.log(response.data);
          this.suit_lst = response.data.data;
          console.log(this.suit_lst)
        }).catch((error) => {
          console.log(error)
        })
      },
      onSubmit() {
        console.log(this.suit_add);
        this.$http.post("http://127.0.0.1:8001/save_suit/", this.suit_add).then((response) => {
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
