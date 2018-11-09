<template>
  <div id="main" style="margin-left: 3%;margin-right: 3%;margin-top: 20px">
    <Row>
      <Col :xs="8" :sm="8" :md="8" :lg="8">
        <h2 style="color: #363e4f;text-align: left;">销售数据一览</h2>
      </Col>
      <Select v-model="areaModel" multiple style="width:200px;float: right;margin-right: 20px" size="large" @on-change="getData">
        <Option v-for="item in areaList" :value="item.value" :key="item.value">{{ item.label }}</Option>
      </Select>

      <el-date-picker
        v-model="dateValue"
        type="datetimerange"
        :picker-options="pickerOptions"
        range-separator="To"
        start-placeholder="Start date"
        end-placeholder="End date"
        v-on:change="getData"
        style="float: right;margin-right: 50px">
      </el-date-picker>
    </Row>

    <br>
    <br>
    <Row>
      <Tabs type="card">
        <TabPane :label="saleCard" style="height: 800px">
          <div id="saleInfo" style="width: 1200px;height: 500px;margin:0 auto;margin-top: 20px;margin-left: 0px"></div>
        </TabPane>
        <TabPane :label="orderCard">暂无</TabPane>
        <TabPane :label="areaOrderCard">
          <div id="areaInfo" style="width: 1200px;height: 500px;margin:0 auto;margin-top: 20px;margin-left: 0px"></div>
        </TabPane>
      </Tabs>

    </Row>

  </div>
</template>

<script>
  import {serverBaseURL} from '../../globalConfig'
  import {formatDate }from '../CommonTool/commonMethod'
  import echarts from 'echarts'
  import {chartTimeStatistic, chartAreaStatistic} from './chartInfo'

  export default {
    name: 'saleData',
    data () {
      return {
        split1: 0.5,
        pickerOptions: '',
        dateValue: '',
        areaList: [{
          'label': '全部地区',
          'value': 'all'
        }],
        orderData:{},
        chartDic: {},

        areaModel:"",

        saleCard: (h) => {
        return h('div',
          {style:{
              width:'300px',
              height:'180px',
              backgroundColor:'transparent'}},
        )
        },

        orderCard: (h) => {
          return h('div',
            {style:{
                width:'300px',
                height:'180px',
                backgroundColor:'transparent'}},
            )
        },

        areaOrderCard: (h) => {
          return h('div',
            {style:{
                width:'300px',
                height:'180px',
                backgroundColor:'transparent'}},
          )
        },

      }
    },
    mounted: function () {
      // 页面加载
      console.log('这里是销售统计页面')
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 1);
      this.dateValue = [start, end]
      this.areaModel = ['all']
      this.getAreaList()
      this.getShotcuts()
      // this.getData()
    },
    methods: {

      getData:function () {
        var self = this
        this.initChart()
        let url = serverBaseURL + 'order/getOrderList?fromDate='
          + this.customFormatDate(this.dateValue[0]) + '&toDate='+ this.customFormatDate(this.dateValue[1]) + '&areaId=' + this.areaModel.join('-')
        this.$http.get(url).then(function (response) {
          var status = response.status;
          if (status == 200) {
            var result = response.body;
            self.orderData = result['data']
            console.log('gggggg')
            console.log(self.orderData)
            self.updateSaleData()
            self.updateOrderData()
            self.chartSaleData()
            self.updateAreaOrderData()
            self.chartAreaOrderData()

          }
        }, function (response) {
          console.log("发生错误")
          var str = response.body.message
          self.$Message.success(str)
        });
      },

      updateSaleData:function () {
        var self = this
        this.saleCard = function (h) {
          var sale_total = self.orderData['sale_total']
          var validate_order_list = self.orderData['validate_order_list']
          var tax_total = self.orderData['tax_total']
          var refund_total = self.orderData['refund_total']
          var order_total = self.orderData['order_total']
          return h('div',
            {style:{
                width:'300px',
                height:'180px',
                textAlign: 'left',
                backgroundColor:'transparent'}},
            [
              h('br'),
              h('h2', {}, '销售总额：$' + sale_total.toFixed(2)  + ' CAD'),
              h('h4', {}, '订单总额：$' + order_total.toFixed(2)  + ' CAD'),
              h('h4', {}, '税费：$' + tax_total.toFixed(2)  + ' CAD'),
              h('h4', {}, '退款：$' + refund_total.toFixed(2)  + ' CAD'),
              h('h4', {}, '有效订单数：' + validate_order_list.length),
              h('h4', {}, '平均订单金额：$' + (sale_total / validate_order_list.length).toFixed(2) + ' CAD'),
            ])
        }

      },

      initChart:function () {
        var self = this
        var elementIdList = ['saleInfo', 'areaInfo']
        elementIdList.forEach(function (elID) {
          var elementId = document.getElementById(elID)
          echarts.dispose(elementId)
          var chart = echarts.init(elementId);
          self.chartDic[elID] = chart
          chart.showLoading({
            text: '数据获取中',
            effect: 'whirling'
          })
        })
      },

      chartSaleData:function () {
        var self = this
        let chart = this.chartDic['saleInfo']
        chart.hideLoading()

        var dataDic = {}
        var dataList = []
        this.orderData['validate_order_list'].forEach(function (order) {
          var dic = {'value': [order['create_at'], order['total']]}
          dataList.push(dic)
        })
        var serie_dic = {
          'name':'销售额',
          'type':'line',
          'itemStyle':{
            'normal':{
              'color': '#63a2c3'
            }
          },
          'data': dataList,
          'markPoint' : {
            'data' : [
              {'type' : 'max', 'name': '最大值'},
              {'type' : 'min', 'name': '最小值'}
            ]
          },
          'markLine': {
            'data' : [
              {'type' : 'average', 'name': '平均销售额'}
            ],
            'itemStyle': {
              'normal': {
                'label': {show: true,
                  'formatter': function(params) {
                    return '平均:$' + params.value + '(CAD)'
                  }},

              }
            },
          }
        }

        dataDic['title'] = '总销售额'
        dataDic['subtitle'] = ''
        dataDic['yUnit'] = 'CAD'
        dataDic['series'] = [serie_dic]
        dataDic['minValue'] = this.customFormatDate(this.dateValue[0])
        dataDic['maxValue'] = this.customFormatDate(this.dateValue[1])

        chart.setOption(chartTimeStatistic(dataDic));
      },

      updateOrderData:function () {
        var self = this
        this.orderCard = function (h) {
          var order_total = self.orderData['all_order_list'].length
          var validate_order_list = self.orderData['validate_order_list']
          return h('div',
            {style:{
                width:'300px',
                height:'180px',
                textAlign: 'left',
                backgroundColor:'transparent'}},
            [
              h('br'),
              h('h2', {}, '全部订单数：' + order_total),
              h('h4', {}, '有效订单数：' + validate_order_list.length),
              h('h4', {}, '退款订单数：' + self.orderData['refund_order']),
              h('h4', {}, '订单增长率：' + self.orderData['order_rate'].toFixed(2) + '%'),
              h('br'),
              h('br'),
            ])
        }

      },

      getAreaList:function () {
        this.initAreaList()
        let url = serverBaseURL + 'otherinfo/getAreaList'
        this.$http.get(url).then(function (response) {
          var status = response.status;
          this.tableLoading = false
          if (status == 200) {
            var result = response.body;
            var area_list = result['data']['area_list']
            for (var i = 0;i < area_list.length;i++) {
              var area = area_list[i]
              var area_dic = {'label': area['name'],'value':area['id']}
              this.areaList.push(area_dic)
            }
          }
        }, function (response) {
          console.log("发生错误")
          var str = response.body.message
          this.$Message.success(str)
        });

      },

      updateAreaOrderData:function () {
        var self = this
        this.areaOrderCard = function (h) {

          return h('div',
            {style:{
                width:'300px',
                height:'150px',
                textAlign: 'left',
                backgroundColor:'transparent'}},
            [
              h('br'),
              h('h2', {}, '区域销售额统计'),
              h('br'),
              h('br'),
              h('br'),
              h('br'),
              h('br'),
            ])
        }
      },
      chartAreaOrderData:function () {
        let chart = this.chartDic['areaInfo']
        chart.hideLoading()

        var dataDic = {}
        var dataList = []

        var area_order_info = this.orderData['area_info']['area_order_info']
        var min = -100
        var max = -100

        for (var key in area_order_info) {
          var value = area_order_info[key]
          if (min == -100) {
            min = value[0]
          }

          if (max == -100) {
            max = value[0]
          }

          if (value[0] > max) {
            max = value[0]
          }

          if (value[0] < max) {
            min = value[0]
          }
          var dic = {'name':value[1], 'value': value[0].toFixed(2)}
          dataList.push(dic)
        }

        dataDic['title'] = '区域销售额统计'
        dataDic['data'] = dataList
        dataDic['min'] = min
        dataDic['max'] = max
        chart.setOption(chartAreaStatistic(dataDic))


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

      initAreaList:function () {
        this.areaList = [{
          'label': '全部地区',
          'value': 'all'
        }]
      },

      customFormatDate:function (date) {
        let format = 'yyyy-MM-dd hh:mm:ss'
        return formatDate(date, format)
      },


      getShotcuts:function () {
        var self = this;
        this.pickerOptions = {
          shortcuts: [{
            text: '过去一天',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 1);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去一周',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去一个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * self.getMonthDays(1));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去三个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * self.getMonthDays(3));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去六个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * self.getMonthDays(6));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去一年',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * self.getMonthDays(12));
              picker.$emit('pick', [start, end]);
            }
          }]
        }
      }
    }
  }
</script>

<style>

  .ivu-tabs.ivu-tabs-card>.ivu-tabs-bar .ivu-tabs-tab-active {
    height: 180px;
  }

  .ivu-tabs.ivu-tabs-card>.ivu-tabs-bar .ivu-tabs-nav-container  {
    height: 180px;
  }

  .ivu-tabs.ivu-tabs-card>.ivu-tabs-bar .ivu-tabs-tab {
    height: 180px;
  }

  .ivu-card {
    background: inherit;
  }

  .ivu-card-head {
    border-bottom: 0px;
  }




</style>
