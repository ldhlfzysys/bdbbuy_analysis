<template>
  <div id="main" style="margin-left: 3%;margin-right: 3%;margin-top: 20px">
    <div class="row" >
      <p :hidden="pageType!='count'" style="margin-left: 0px;width: 400px">
        <label >输入库存最低数量：</label>
        <input type="text" class="normal" v-model="countInfo"/>
        <label >件</label>
        <Button v-on:click="getData">
          刷新
        </Button>
        <small></small>
      </p>
      <p :hidden="pageType!='ordercount'" style="margin-left: 0px;width: 300px">
        <label >按过去</label>
        <input type="text" class="normal" v-model="orderDay"/>
        <label >天销量</label>
        <Button v-on:click="getData">
          查找
        </Button>
        <small></small>
      </p>
      <br>
      <p style="margin-left: 0px;width: 360px">
        <label style="text-align: left">(查找的数据包含：库存低于{{orderDay}}天销量的数据和总库存低于5的数据)</label>
      </p>


    </div>
    <br>

    <Table  border :data="tableData" :columns="tableColumns" stripe :loading="tableLoading"></Table>
    <div style="margin: 20px;overflow: hidden">
      <div style="float: right;">
        <Page ref="pages" :total="totalCount" :current="pageCurrent" @on-change="changePage"
              :page-size="pageSize" show-sizer :page-size-opts="page_size_opts" show-total></Page>
      </div>
    </div>

  </div>
</template>

<script>
  import {serverBaseURL} from '../../globalConfig'

  export default {
    name: 'inventoryWarning',
    watch: {
      '$route' (to, from) {
        this.pageType = this.$route.query.type
        this.setTableColumn()
        this.getData()
      },
    },
    data() {
      return {
        page_size_opts: [20, 40, 50, 100],
        pageSize: 20,
        tableData: [],
        tableColumns: [],
        totalCount: 0,
        allProductList: [],
        pageType: 'count',
        countInfo: 5,
        orderDay: 7,
        pageCurrent: 1,
        tableLoading: false,
        cancelTokenFn: null

      }

    },
    mounted: function () {
      // 页面加载
      console.log('这里是库存预警页面')
      this.pageType = this.$route.query.type
      this.setTableColumn()
      this.getData()
    },

    methods: {

      getData:function () {
        this.tableData = []
        this.pageCurrent = 1
        this.totalCount = 0
        this.tableLoading = true
        let url = serverBaseURL + 'product/getWarnigProduct'
        if (this.pageType == 'count') {
          // 按照最低库存数查找
          url = url + '?lowCount=' + this.countInfo
        } else if (this.pageType == 'date') {
          // 查找过期商品
          url = url + '?outOfDate=' + true
        } else if (this.pageType == 'ordercount') {
          // 按照销量查找库存数据
          url = url + '?orderDay=' + this.orderDay
        }
        this.$http.get(url).then(function (response) {
          var status = response.status;
          this.tableLoading = false
          if (status == 200) {
            var result = response.body;
            this.allProductList = result['data']['order_list']
            this.totalCount = result['data']['totalCount']
            this.changePage(1)
          }
        }, function (response) {
          console.log("发生错误")
          var str = response.body.message
          this.tableLoading = false
          this.$Message.success(str)
        });
      },

      setTableColumn:function () {
        this.tableColumns = [
          {
            title: 'id',
            key: 'product_id',
            width: 100,
            align: 'center',
          },
          {
            title: '中文名',
            key: 'name',
            width: 200,
            align: 'left',
          },
          {
            title: 'SKU',
            key: 'sku',
            // width: 150,
            align: 'center',
          },
          {
            title: '售价',
            key: 'price',
            // width: 150,
            align: 'center',
          },
          {
            title: '保质期',
            key: 'quality_date',
            // width: 200,
            align: 'center',
          },
          {
            title: '库存数量',
            key: 'product_qty',
            // width: 100,
            align: 'center',
          },
        ]
        if (this.pageType == 'ordercount') {
          var order_count_dic = {
            title: '过去' + this.orderDay + '天销量',
            key: 'order_count',
            // width: 150,
            align: 'center',
          }
          this.tableColumns.push(order_count_dic)
          var delta_stock_dic =  {
            title: '库存差值',
            key: 'delta_count',
            // width: 100,
            align: 'center',
          }
          this.tableColumns.push(delta_stock_dic)
        }

      },

      changePage:function (index) {
        var startPosition = 0
        var endPosition = this.allProductList.length
        if (this.allProductList.length > this.pageSize) {
          startPosition = this.pageSize * (index - 1)
          endPosition = this.pageSize * index
        }
        this.tableData = this.allProductList.slice(startPosition, endPosition)
      },


    }

  }
</script>

<style scoped>
  label {
    /*width: 25%;*/
    display: inline-block;
    padding: 0 5px;
    vertical-align: middle;
    font-style: normal;
    color: black;
    margin-left: 0px;
  }


  input[type="text"] {
    height: 30px;
    line-height: 20px;
    border-radius: 5px;
    padding: 5px 5px;
    vertical-align: middle;
    color: #666;
  }

</style>
