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
      <br/>
      <p :hidden="pageType!='ordercount'" style="margin-left: 0px;width: 360px">
        <label style="text-align: left">(查找的数据包含：库存低于{{orderDay}}天销量的数据和总库存低于5的数据)</label>
      </p>
      <!--<Button v-on:click="exportToExcel" style="float:right;margin-right: 10px" type="primary">-->
        <!--导出到Excel-->
      <!--</Button>-->
      <Button v-on:click="printTable" style="float:right" type="primary">
        打印所有数据
      </Button>
      <br>


    </div>
    <br>

    <Table id="inventoryWarningTable"  border :data="tableData" :columns="tableColumns" stripe :loading="tableLoading"></Table>
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
            // width: 100,
            align: 'center',
          },
          {
            title: '中文名',
            key: 'name',
            // width: 200,
            align: 'left',
          },
          {
            title: 'SKU',
            key: 'sku',
            // width: 150,
            align: 'center',
          },
          {
            title: '规格',
            key: 'description',
            // width: 150,
            align: 'center',
          },
          {
            title: '保质期',
            key: 'quality_date',
            // width: 200,
            align: 'center',
            sortable: true
          },
          {
            title: '库存数量',
            key: 'product_qty',
            // width: 100,
            align: 'center',
            sortable: true
          },
        ]
        if (this.pageType == 'ordercount') {
          var order_count_dic = {
            title: '过去' + this.orderDay + '天销量',
            key: 'order_count',
            // width: 150,
            align: 'center',
            sortable: true
          }
          this.tableColumns.push(order_count_dic)
          var delta_stock_dic =  {
            title: '库存差值',
            key: 'delta_count',
            // width: 100,
            align: 'center',
            sortable: true
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

      printTable:function () {
        this.tableData = this.allProductList
        var tableToPrint = this.preparePrintTable();//将要被打印的表格
        var newWin= window.open("",'打印');//新打开一个空窗口
        newWin.document.write('<html><head><title>库存预警商品清单</title>');
        newWin.document.write('</head><body >');
        newWin.document.write(tableToPrint);
        newWin.document.write('</body></html>');
        newWin.document.close();//在IE浏览器中使用必须添加这一句
        newWin.focus();//在IE浏览器中使用必须添加这一句
        setTimeout(()=> {     //延时
          newWin.print();
          newWin.close()
        },1000);



      },

      preparePrintTable() {
        //隐藏原表格
        var record_num = 40;
        var pages = Math.ceil(this.allProductList.length / record_num);
        //满页数
        var newTableDiv;
        var html_tbl;
        html_tbl = "";
        var head_table_comp;
        var tail_table_comp;
        var newTable;
        //获取原table的class和style属性
        head_table_comp = document.getElementsByClassName("ivu-table-header").outerHTML;
        tail_table_comp = document.getElementsByClassName("ivu-table-body").outerHTML;

        var printTitle = document.createElement("h1");
        printTitle.appendChild(document.createTextNode("库存预警清单"))
        printTitle.setAttribute("style", "text-align: center")
        html_tbl += printTitle.outerHTML;

        var headerTable = document.createElement("table");
        // headerTable.setAttribute("class", "print_table");
        headerTable.setAttribute("cellspacing", "0");
        headerTable.setAttribute("border", "1px solid");
        headerTable.setAttribute("style", "margin-left: 5mm;width: 200mm;border-color: #515a6e;page-break-after:always");
        var head_thead = document.createElement("thead");
        var head_tr = document.createElement("tr");
        var head_content = "";
        // 设置打印表头
        for(var i = 0; i < this.tableColumns.length; i++) {
          var header_data = this.tableColumns[i];
          var header_th = document.createElement("th");
          var title_span = document.createElement("span");
          var title = document.createTextNode(header_data["title"]);
          title_span.appendChild(title);
          header_th.appendChild(title_span);
          head_content += header_th.outerHTML;
        }
        head_tr.innerHTML = head_content;
        head_thead.appendChild(head_tr);
        headerTable.appendChild(head_thead);
        // html_tbl += headerTable.outerHTML;

        // 设置table body部分

        var tbody = document.createElement("tbody");
        headerTable.appendChild(tbody);
        for (var i = 0; i < pages; i++) {
          var last_data = ((i + 1) * record_num) <  this.allProductList.length ? ((i + 1) * record_num) : this.allProductList.length;
          for (var j = i * record_num;j < last_data ;j++) {
            var record = this.allProductList[j];
            var record_tr = document.createElement("tr")
            record_tr.setAttribute("style", "text-align: center;word-break: break-all")
            for(var k = 0; k < this.tableColumns.length; k++) {
              var record_td = document.createElement("td")
              var column_key = this.tableColumns[k]["key"];
              var content_span = document.createElement("span")
              content_span.setAttribute("style", "align: center")
              content_span.appendChild(document.createTextNode(record[column_key]))
              record_td.appendChild(content_span)
              record_tr.appendChild(record_td)
            }
            tbody.appendChild(record_tr)

          }
        }

        html_tbl += headerTable.outerHTML;


        return html_tbl
      },

      createEmptyTr(idx) {
        var emptyTr;
        var emptyTd;
        emptyTr = document.createElement("tr");
        emptyTr.setAttribute("style","word-wrap:break-word;width: 10%;border-left-width:5px;text-align:center");
        emptyTd = document.createElement("td");
        emptyTd.setAttribute("style","word-wrap:break-word;width: 10%;border-left-width:5px;text-align:center");
        emptyTd.innerHTML="  ";
        var tra= emptyTd.outerHTML;

        emptyTd = document.createElement("td");
        emptyTd.setAttribute("style","text-align:center");
        var trb= emptyTd.outerHTML;

        emptyTd = document.createElement("td");
        emptyTd.setAttribute("style","text-align:center");
        var trc= emptyTd.outerHTML;

        emptyTd = document.createElement("td");
        emptyTd.setAttribute("style","text-align:center");
        var trd= emptyTd.outerHTML;

        emptyTd = document.createElement("td");
        emptyTd.setAttribute("style","text-align:center");
        var tre= emptyTd.outerHTML;
        emptyTr.innerHTML=tra+trb+trc+trd+tre;
        return emptyTr.outerHTML;
      },

      exportToExcel () {

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
