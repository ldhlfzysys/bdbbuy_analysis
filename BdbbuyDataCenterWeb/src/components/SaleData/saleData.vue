<template>
  <div id="main" style="margin-left: 3%;margin-right: 3%;margin-top: 20px">
    <Row>
      <Col span="4">
        <h2 style="color: #363e4f;text-align: left;">销售数据一览</h2>
      </Col>

      <Col span="16">
        <Select v-model="timeModel" style="width:80px;float: right" size="large" @on-change="changeStatisticGroupKey">
          <Option v-for="item in timeList" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
        <el-date-picker
          v-model="dateValue"
          type="datetimerange"
          :picker-options="pickerOptions"
          range-separator="To"
          start-placeholder="Start date"
          end-placeholder="End date"
          v-on:change="timeChange"
          style="float: right;margin-right: 20px">
        </el-date-picker>


      </Col>
      <Col span="4">
        <Select v-model="areaModel" multiple style="width:200px;float: right" size="large" @on-change="getData">
          <Option v-for="item in areaList" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
      </Col>



    </Row>

    <br>
    <br>
    <Row>
      <Tabs type="card">
        <TabPane :label="saleCard" style="height: 800px">
          <div id="saleInfo" style="width: 1200px;height: 500px;margin:0 auto;margin-top: 20px;margin-left: 0px"></div>
        </TabPane>
        <TabPane :label="orderCard">
          <div id="orderInfo" style="width: 1200px;height: 500px;margin:0 auto;margin-top: 20px;margin-left: 0px"></div>
        </TabPane>
        <TabPane :label="areaOrderCard">
          <div id="areaInfo" style="width: 1200px;height: 500px;margin:0 auto;margin-top: 20px;margin-left: 0px"></div>
        </TabPane>
      </Tabs>

    </Row>

  </div>
</template>

<script>
  import {serverBaseURL} from '../../globalConfig'
  import {formatDate, customDateParse, range, getTimeByTimeZone}from '../CommonTool/commonMethod'
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
        timeModel:"day",
        timeList: [{
          'label': '日',
          'value': 'day'
        }],

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
      const end = getTimeByTimeZone(-5);
      const start = getTimeByTimeZone(-5);
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 1);
      this.dateValue = [start, end]
      this.changeStasticTimeList()
      this.areaModel = ['all']
      this.getAreaList()
      this.getShotcuts()
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
            self.updateSaleData()
            self.updateOrderData()
            self.chartSaleData()
            self.updateAreaOrderData()
            self.chartAreaOrderData()
            self.chartOrderData()

          }
        }, function (response) {
          console.log("发生错误")
          var str = response.body.message
          self.$Message.success(str)
        });
      },

      timeChange:function () {
        this.changeStasticTimeList()
        this.getData()

      },

      changeStatisticGroupKey:function () {
        this.chartSaleData()
      },

      changeStasticTimeList:function () {
        var delta_time = this.dateValue[1] - this.dateValue[0];

        var date0_year = this.dateValue[0].getUTCFullYear()
        var date1_year = this.dateValue[1].getUTCFullYear()

        var date0_month = this.dateValue[0].getUTCMonth()
        var date1_month = this.dateValue[1].getUTCMonth()

        var date0_week = this.getWeek(this.dateValue[0])
        var date1_week = this.getWeek(this.dateValue[1])

        this.timeList = []

        let time_dic = {
          'year': {
            'label': '年',
            'value': 'year'
          },
          'month': {
            'label': '月',
            'value': 'month'
          },
          'week' : {
            'label': '周',
            'value': 'week'
          },
          'day' : {
            'label': '日',
            'value': 'day'
          }
        }

        var list = []
        if (date0_year != date1_year) {
          // 图表默认展示年组
          list = ['year', 'month', 'week', 'day']
          this.timeModel = 'year'
        } else if (date0_month != date1_month) {
          // 图表默认展示月组
          list = ['month', 'week', 'day']
          this.timeModel = 'month'
        } else if (date0_week != date1_week) {
          list = [ 'week', 'day']
          this.timeModel = 'week'
        } else {
          list = ['day']
          this.timeModel = 'day'
        }

        this.timeList = []
        for (var i = 0; i < list.length;i++) {
          var key = list[i]
          this.timeList.push(time_dic[key])
        }

      },

      getWeek:function (date) {
        // 先计算出该日期为第几周
        let week = Math.ceil(date.getDate()/7);
        let month = date.getMonth() + 1;
        // 判断这个月前7天是周几，如果不是周一，则计入上个月
        if  (date.getDate() < 7) {
          if (date.getDay() !== 1) {
            week = 5;
            month = date.getMonth() + 1;
          }
        }
        return `${month}-${week}`
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
        var elementIdList = ['saleInfo', 'orderInfo','areaInfo']
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

        var group_dic = {}
        var title = '日销售额'
        this.orderData['validate_order_list'].forEach(function (order) {
          var group_key = ''
          var crate_time_str = order['create_at'].replace('T', ' ').replace('Z', '')
          var crate_time = new Date(Date.parse(crate_time_str.replace(/-/g, '/')))
          if (self.timeModel == 'year') {
            // 按照年组group统计图数据
            var year = crate_time.getUTCFullYear()
            group_key = year
            title = '年销售额'

          } else if (self.timeModel == 'month') {
            // 按照月组group统计图数据
            var month = crate_time.getUTCMonth() + 1
            group_key = crate_time.getUTCFullYear() + '年' + month.toString() + '月'
            title = '月销售额'

          } else if (self.timeModel == 'week') {
            // 按照周组group统计图数据
            var origin_week = self.getWeek(crate_time)
            var week = crate_time.getUTCFullYear() + '年' + origin_week.split('-')[0] + '月第' + origin_week.split('-')[1] + '周'
            group_key = week
            title = '周销售额'

          } else {
            // 按照日组group统计图数据
            var date = crate_time_str.split(' ')[0]
            group_key = date
            title = '日销售额'
          }
          var total = parseFloat(order['total'])
          if (group_dic.hasOwnProperty(group_key)) {
            group_dic[group_key] = group_dic[group_key] + total
          } else {
            group_dic[group_key] = total
          }
        })

        // 统计图数据
        var sorted_keys = Object.keys(group_dic).sort()
        sorted_keys.forEach(function (key) {
          var total_sale = group_dic[key].toFixed(2)
          var dic = {'value': [key, total_sale]}
          dataList.push(dic)
        })

        if (sorted_keys.length > 15) {
          dataDic['rotate'] = 45
        }

        var serie_dic = {
          'name':title,
          'type':'bar',
          'barWidth' : 30,
          'itemStyle':{
            'normal':{
              'color': '#63a2c3',
              'label': {
                'show': true, //开启显示
                'position': 'top', //在上方显示
                'textStyle': { //数值样式
                  'color': 'black',
                  'fontSize': 12
                }
              }
            },
          },
          'data': dataList,
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

        dataDic['title'] = title
        dataDic['subtitle'] = ''
        dataDic['yUnit'] = 'CAD'
        dataDic['series'] = [serie_dic]
        dataDic['xAxisType'] = 'category'
        dataDic['minValue'] = this.customFormatDate(this.dateValue[0])
        dataDic['maxValue'] = this.customFormatDate(this.dateValue[1])

        chart.setOption(chartTimeStatistic(dataDic));
      },

      chartOrderData:function () {
        var self = this
        let chart = this.chartDic['orderInfo']
        chart.hideLoading()

        var dataDic = {}
        var dataList = []
        var hourOrderDic = {}

        for (var hour in range(0, 23)) {
          hourOrderDic[hour] = 0
        }

        this.orderData['validate_order_list'].forEach(function (order) {
          var hour = customDateParse(order['create_at']).getHours()
          if (hourOrderDic.hasOwnProperty(hour)) {
            hourOrderDic[hour] = hourOrderDic[hour] + 1
          } else {
            hourOrderDic[hour] = 1
          }

        })

        var xAxisData = []

        for (var key in hourOrderDic) {
          var order_count = hourOrderDic[key]
          var key_str = key + '时'
          var dic = {'value': [key_str, order_count]}
          dataList.push(order_count)
          xAxisData.push(key_str)
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
          'markLine': {
            'data' : [
              {'type' : 'average', 'name': '平均订单数'}
            ],
            'itemStyle': {
              'normal': {
                'label': {show: true,
                  'formatter': function(params) {
                    return '平均:$' + params.value + '(单)'
                  }},

              }
            },
          }
        }

        dataDic['title'] = '各时段订单数统计'
        dataDic['subtitle'] = ''
        dataDic['series'] = [serie_dic]
        dataDic['xAxisType'] = 'category'
        dataDic['xAxisData'] = xAxisData
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
        var strYear = date.getUTCFullYear();
        if(strYear%4 == 0 && strYear%100 != 0){
          daysInMonth[2] = 29;
        }

        var past_days = 0
        for (var i = month; i > 0; i--) {
          var searchMonth = date.getUTCMonth()  - i;
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
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 1);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去一周',
            onClick(picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去一个月',
            onClick(picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * self.getMonthDays(1));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去三个月',
            onClick(picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * self.getMonthDays(3));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去六个月',
            onClick(picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * self.getMonthDays(6));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去一年',
            onClick(picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
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
