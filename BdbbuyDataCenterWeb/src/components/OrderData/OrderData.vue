<template>
  <div id="main" style="margin-top: 20px" class="main">
    <Row>
      <Col span="4">
        <Menu  id="catogery_menu" @on-select="selectMenu" style="width: 95%;min-height: 500px">
          <MenuItem name="all">全部分类</MenuItem>
          <Submenu v-for="item in hasSubCatogeryList" :name="item.catogery_id" :key="item.catogery_id">
            <template slot="title">
              {{item.catogery_name}}
            </template>
            <MenuItem :name="item.catogery_id" :id="item.catogery_id">
              {{item.catogery_name}}
            </MenuItem>
            <MenuItem v-for="subitem in item.catogery_sublist" :name="subitem.catogery_id" :key="subitem.catogery_id">
              {{subitem.catogery_name}}
            </MenuItem>
          </Submenu>
          <MenuItem v-for="subitem in noSubCatogeryList" :name="subitem.catogery_id" :key="subitem.catogery_id">
            {{subitem.catogery_name}}
          </MenuItem>

        </Menu>
      </Col>

      <Col span="20">
        <br>
        <Row>
          <Col span="3">
            <label style="margin-top: 12px">时间段选择：</label>

          </Col>

          <Col span="9">
            <el-date-picker
              v-model="dateValue"
              type="datetimerange"
              :picker-options="pickerOptions"
              range-separator="To"
              start-placeholder="Start date"
              end-placeholder="End date"
              style="margin-left: 0;width: 100%">
            </el-date-picker>

          </Col>

          <Col span="2">
            <Button type="primary" ghost style="margin-top: 5px" v-on:click="getData">查 询</Button>
          </Col>
          <Col span="2">
            <Button type="primary" ghost style="margin-top: 5px" v-on:click="showStatisticPic">查看统计图</Button>
            <Modal v-model="showStatistic"
                   width="900">
              <p slot="header" style="color:#f60;text-align:center">
                <span>该时段内订单销量分类统计图</span>
              </p>
              <div id="catogeryOrder" style="width: 880px;height: 400px;"></div>
              <div slot="footer">
                <Button type="primary" ghost style="margin-top: 5px" v-on:click="showStatistic=false">关闭</Button>
              </div>
            </Modal>
          </Col>

          <Col span="7">
            <Button type="primary" ghost style="margin-top: 5px;float: right" v-on:click="exportTableData">导出表格</Button>
          </Col>
        </Row>
        <br>
        <Row>
          <Col span="23">
            <Table id="orderProductTable"  border :data="tableData" :columns="tableColumns" stripe :loading="tableLoading"></Table>
            <div style="margin: 20px;overflow: hidden">
              <div style="float: right;">
                <Page ref="pages" :total="totalCount" :current="pageCurrent"
                      :page-size="pageSize"
                      show-total @on-change="changePage"></Page>
              </div>
            </div>
          </Col>
        </Row>

      </Col>



    </Row>
  </div>
</template>

<script>
  import {serverBaseURL} from '../../globalConfig'
  import {formatDate, customDateParse, range, getTimeByTimeZone}from '../CommonTool/commonMethod'
  import MenuItem from 'iview/src/components/menu/menu-item.vue'
  import FileSaver from 'file-saver'
  import echarts from 'echarts'
  import XLSX from 'xlsx'
  import XLSX_SAVE from  'file-saver'
  import {isString}from '../CommonTool/commonMethod'
  import {chartTimeStatistic, chartAreaStatistic} from '../SaleData/chartInfo'

  export default {
    name: 'OrderData',

    data () {
      return {
        dateValue: '',
        catogeryModel: 'all',
        tableData: [],
        tableColumns: [],
        tableLoading: false,
        pickerOptions: [],

        totalCount: 0,
        pageCurrent: 1,
        pageSize: 30,

        hasSubCatogeryList: [],
        noSubCatogeryList: [],

        tableLoading: false,
        allProductList: [],

        storeProductList: [],
        lastFromDateValue: '',
        lastToDateValue: '',

        showStatistic: false,
        statisticChart: ''

      }
    },
    mounted: function () {
      const end = getTimeByTimeZone(-5);
      const start = getTimeByTimeZone(-5);
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 1);
      this.dateValue = [start, end]
      this.getShotcuts()
      this.getCatogery()
      this.setTableColumn()
      this.getData()
      this.initChart()
    },

    methods: {

      initChart:function () {
        var elementId = document.getElementById('catogeryOrder')
        echarts.dispose(elementId)
        var chart = echarts.init(elementId);
        this.statisticChart = chart;

      },

      getData:function () {
        let url = serverBaseURL + 'product/getProductSale?fromDate='
          + this.customFormatDate(this.dateValue[0]) + '&toDate='+ this.customFormatDate(this.dateValue[1])
          + '&catogeryId=' + this.catogeryModel

        this.allProductList = []
        this.tableData = []
        this.tableLoading = true
        this.$http.get(url).then(function (response) {
          var status = response.status;
          this.tableLoading = false
          if (status == 200) {
            var result = response.body;
            this.allProductList = result['data']['product_list']
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

      getAllData:function () {
        console.log('获取统计数据')
        let url = serverBaseURL + 'product/getCatogeryGroupSale?fromDate='
          + this.customFormatDate(this.dateValue[0]) + '&toDate='+ this.customFormatDate(this.dateValue[1])

        this.storeProductList = []
        this.lastFromDateValue = this.dateValue[0]
        this.lastToDateValue = this.dateValue[1]
        this.statisticChart.showLoading({
          text: '数据获取中',
          effect: 'whirling'
        })
        this.$http.get(url).then(function (response) {
          var status = response.status;
          if (status == 200) {
            var result = response.body;
            this.storeProductList = result['data']['statistic_list']
            console.log(this.storeProductList)
            this.drawStatisticInfo()
            this.statisticChart.hideLoading()
          }
        }, function (response) {
          console.log("发生错误")
          var str = response.body.message
          this.$Message.success(str)
        });

      },

      showStatisticPic:function () {
        if (this.storeProductList.length > 0
          && this.lastFromDateValue == this.dateValue[0]
          && this.lastToDateValue == this.dateValue[1]) {
          // 如果数据存在并且选择的日期未发生改变，则使用缓存数据
          this.drawStatisticInfo();
        } else {
          this.getAllData();
        }
        this.showStatistic = true

      },

      drawStatisticInfo:function () {
        var self = this
        var dataList = []
        var xAxisData = []

        for (var index in this.storeProductList) {
          var catogery = this.storeProductList[index]
          dataList.push(catogery['catogery_sale'])
          xAxisData.push(catogery['catogery_name'])
        }

        var serie_dic = {
          'name':'各时段订单数统计',
          'type':'bar',
          'itemStyle':{
            'normal':{
              'color': '#63a2c3'
            }
          },
          'label': {
            'normal': {
              'color': '#ffffff',
              'show': true,
              'formatter': function (params) {
                if (params.value > 0) {
                  return params.value;
                } else {
                  return '';
                }
              }
            }
          },
          'data': dataList,
        }

        var dataDic = {}

        dataDic['title'] = '各分类销量统计'
        dataDic['subtitle'] = ''
        dataDic['series'] = [serie_dic]
        dataDic['xAxisType'] = 'category'
        dataDic['xAxisData'] = xAxisData
        dataDic['rotate'] = 40
        this.statisticChart.setOption(chartTimeStatistic(dataDic));

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

      selectMenu:function (menu) {
        this.catogeryModel = menu
        this.getData()
      },

      getCatogery:function () {
        this.hasSubCatogeryList = []
        this.noSubCatogeryList = []

        let url = serverBaseURL + 'product/getProductCatogery'
        this.$http.get(url).then(function (response) {
          var status = response.status;
          if (status == 200) {
            var result = response.body;
            var catogeryList = result['data']['catogery_list']
            for (var i = 0;i < catogeryList.length;i++) {
              var catogery = catogeryList[i]
              if (catogery.catogery_sublist.length > 0) {
                this.hasSubCatogeryList.push(catogery)
              } else {
                this.noSubCatogeryList.push(catogery)
              }
            }

          }
        }, function (response) {
          console.log("发生错误")
          var str = response.body.message
          this.$Message.success(str)
        });
      },

      customFormatDate:function (date) {
        let format = 'yyyy-MM-dd hh:mm:ss'
        return formatDate(date, format)
      },

      setTableColumn:function () {
        this.tableColumns = [
          {
            title: '英文名',
            key: 'en_name',
            align: 'left',
          },
          {
            title: '中文名',
            key: 'name',
            align: 'left',
          },
          {
            title: 'SKU',
            key: 'sku',
            align: 'center',
          },
          {
            title: '规格',
            key: 'description',
            align: 'center',
          },
          {
            title: '销量',
            key: 'sale_count',
            align: 'center',
          },
          {
            title: '库存数量',
            key: 'product_qty',
            align: 'center',
          },
        ]
      },

      exportTableData:function () {
          /* generate workbook object from table */
          // var wb = XLSX.utils.table_to_book(document.querySelector('#inventoryWarningTable'))
          var wb = XLSX.utils.book_new();
          var json_data = []
          var header_keys = []
          var header_titles = []

          for (var i = 0; i < this.tableColumns.length; i++) {
            var column = this.tableColumns[i];
            header_keys.push(column['key'])
            header_titles.push(column['title'])
          }


          for (var i = 0;i < this.allProductList.length;i++) {
            var record = this.allProductList[i];

            var dic = {};
            for (var j = 0;j < header_keys.length;j++) {
              if (j == 0) {
                dic['序号'] = i + 1
              }
              var header_key = header_keys[j]
              var header_title = header_titles[j]
              var data = record[header_key]
              dic[header_title] = data;
            }
            json_data.push(dic)
          }


          var ws = XLSX.utils.json_to_sheet(json_data);
          /* get binary string as output */

          for (var key in ws) {
            var cell = ws[key]
            if (!isString(cell)) {
              try {
                cell['s'] = {border: borderAll}
              } catch (e) {
                console.log(e)
              }

            }
          }

          XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
          var wbout = XLSX.write(wb, {type: "binary", bookType: "xlsx"});

          try {
            XLSX_SAVE.saveAs(new Blob([this.s2ab(wbout)], {type: "application/octet-stream"}), "分类销量统计.xlsx");
          } catch (e) { if (typeof console !== 'undefined') console.log(e, wbout) }
          return wbout
      },

      s2ab:function(s) {
        const buf = new ArrayBuffer(s.length);
        const view = new Uint8Array(buf);
        for (let i = 0; i !== s.length; ++i) {
          view[i] = s.charCodeAt(i) & 0xFF;
        }
        return buf;
      },

      getShotcuts:function () {
        var self = this;
        this.pickerOptions = {
          shortcuts: [{
            text: '过去一天',
            onClick (picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 1);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去一周',
            onClick (picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去一个月',
            onClick (picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * self.getMonthDays(1));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去三个月',
            onClick (picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * self.getMonthDays(3));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去六个月',
            onClick (picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * self.getMonthDays(6));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去一年',
            onClick (picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * self.getMonthDays(12));
              picker.$emit('pick', [start, end]);
            }
          }]
        }
      },

      getMonthDays:function (month) {
        var date = new Date()
        var daysInMonth = new Array([0],[31],[28],[31],[30],[31],[30],[31],[31],[30],[31],[30],[31]);
        var strYear = date.getFullYear();
        if(strYear%4 == 0 && strYear%100 != 0){
          daysInMonth[2] = 29;
        }

        var past_days = 0
        for (var i = month; i > 0; i--) {
          var searchMonth = date.getMonth()  - i;
          searchMonth = searchMonth <= 0 ? searchMonth + 12:searchMonth;
          past_days += parseInt(daysInMonth[searchMonth])
        }

        return past_days;

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

</style>
