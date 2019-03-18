<template>
  <div id="main" style="margin-top: 20px" class="main">
    <Row>
      <Col span="2">
        <label style="margin-top: 12px;margin-right: 0px;">时间段选择：</label>

      </Col>

      <Col span="8">
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
    </Row>
    <br>
    <br>

    <Row>
      <Col span="12">
        <Table id="driverTable"  border :data="driverData" :columns="driverColumns" :loading="tableLoading" style="margin-left: 20px"></Table>

      </Col>
    </Row>
    <br>
    <br>
    <Row>
      <Col span="2">
        <label>
          选择司机：
        </label>
      </Col>
      <Col span="3">
        <Select v-model="driverModel" style="width:150px;" size="small" @on-change="changeDriver">
          <Option v-for="item in allDriverList" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
      </Col>
    </Row>

    <br>
    <br>
    <Row>
      <Col span="23">
        <Table id="orderTable"  border :data="orderData" :columns="orderColumns" stripe :loading="tableLoading" style="margin-left: 20px"></Table>
        <div style="margin: 20px;overflow: hidden">
          <div style="float: right;">
            <Page ref="pages" :total="totalCount" :current="pageCurrent"
                  :page-size="pageSize"
                  show-total @on-change="changePage"></Page>
          </div>
        </div>
      </Col>

    </Row>
  </div>
</template>

<script>
  import {formatDate, customDateParse, range, getTimeByTimeZone, getMonthDays}from '../CommonTool/commonMethod'
  import {serverBaseURL} from '../../globalConfig'

  export default {
    name: 'DriverData',
    data () {
      return {
        dateValue: [],
        pickerOptions: {},
        filterDriverList: [],

        allOrderList: [],
        showOrderList: [],
        tableLoading: false,
        originDriverList: [],

        totalCount: 0,
        pageSize: 10,
        pageCurrent: 1,

        driverColumns: [],
        driverData: [],

        orderColumns: [],
        orderData: [],

        driverModel: "all",
        allDriverList: [{'label': '全部司机', 'value': 'all'}]

      }
    },

    mounted : function () {
      this.getAllDriverData()
      const end = getTimeByTimeZone(-5);
      const start = getTimeByTimeZone(-5);
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 1);
      this.dateValue = [start, end]
      this.getShotcuts()
      this.getData()

    },

    methods : {
      changeDriver:function (value) {
        if (value == 'all') {
          this.showOrderList = this.allOrderList
        } else {

          var list = []
          for (var i = 0;i < this.originDriverList.length;i++) {
            var driver = this.originDriverList[i]
            if (value == driver['driver_id']) {
              list.push.apply(list, driver['order_list'])

              break;
            }
          }
          this.showOrderList = list

        }

        this.totalCount = this.showOrderList.length
        this.changePage(1)
      },

      changePage:function (index) {
        var startPosition = 0
        var endPosition = this.showOrderList.length
        if (this.showOrderList.length > this.pageSize) {
          startPosition = this.pageSize * (index - 1)
          endPosition = this.pageSize * index
        }
        this.orderData = this.showOrderList.slice(startPosition, endPosition)

      },

      initData:function () {
        this.allOrderList = []
        this.driverData = []
        this.orderData = []
        this.filterDriverList = []
        this.showOrderList = []
        this.originDriverList = []
        this.totalCount = 0

        this.driverColumns = [
          {
            title: '司机ID',
            key: 'driver_id',
            align: 'center',
          },
          {
            title: '司机姓名',
            key: 'driver_name',
            align: 'center',
          },
          {
            title: '配送订单数',
            key: 'count',
            align: 'center',
          },]

        this.orderColumns = [
          {
            title: '司机',
            key: 'driver',
            align: 'center',
          },
          {
            title: '订单号',
            key: 'order_id',
            align: 'center',
          },
          {
            title: '用户ID',
            key: 'customer_id',
            align: 'center',
          },
          {
            title: '用户名',
            key: 'customer_name',
            align: 'center',
          },
          {
            title: '地区',
            key: 'area',
            align: 'center',
          },
          {
            title: '城市',
            key: 'city',
            align: 'center',
          },
          {
            title: '邮编',
            key: 'post_code',
            align: 'center',
          },
          {
            title: '地址',
            key: 'address',
            align: 'center',
          },
          {
            title: '金额',
            key: 'total',
            align: 'center',
          },
        ]


      },

      setDriverData:function (driverList) {
        this.driverData = driverList

      },
      setAllOrderData:function (driverList) {
        var data_list = []
        for(var i = 0; i < driverList.length;i++) {
          var driver_data = driverList[i]
          data_list.push.apply(data_list, driver_data['order_list'])
        }
        this.allOrderList = data_list
        this.showOrderList = data_list
        this.changePage(1)
      },

      getAllDriverData:function () {
        this.allDriverList = [{'label': '全部司机', 'value': 'all'}]
        let url = serverBaseURL + 'adminuser/getDriver'
        this.$http.get(url).then(function (response) {
          var status = response.status;
          if (status == 200) {
            var result = response.body;
            var driver_list = result['data']
            for(var i = 0;i < driver_list.length;i++) {
              var driver = driver_list[i]
              var driver_dic = {
                'label': driver['name'],
                'value': driver['id'],
              }
              this.allDriverList.push(driver_dic)
            }

          }
        }, function (response) {
          console.log("发生错误")
          var str = response.body.message
          this.$Message.success(str)
        });

      },

      getData:function () {
        var self = this
        this.tableLoading = true

        this.initData()
        let url = serverBaseURL + 'order/getDriverDeliveredOrder?fromDate='
          + this.customFormatDate(this.dateValue[0]) + '&toDate='+ this.customFormatDate(this.dateValue[1])
        this.$http.get(url).then(function (response) {
          self.tableLoading = false
          var status = response.status;
          if (status == 200) {
            var result = response.body;
            var driver_list = result['data']['driver_list']
            this.originDriverList = driver_list
            self.setDriverData(driver_list)
            self.setAllOrderData(driver_list)
            self.totalCount = result['data']['total_count']

          }
        }, function (response) {
          console.log("发生错误")
          var str = response.body.message
          this.$Message.success(str)
        });
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
              start.setTime(start.getTime() - 3600 * 1000 * 24 * getMonthDays(1));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去三个月',
            onClick(picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * getMonthDays(3));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去六个月',
            onClick(picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * getMonthDays(6));
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '过去一年',
            onClick(picker) {
              const end = getTimeByTimeZone(-5);
              const start = getTimeByTimeZone(-5);
              start.setTime(start.getTime() - 3600 * 1000 * 24 * getMonthDays(12));
              picker.$emit('pick', [start, end]);
            }
          }]
        }
      },

      customFormatDate:function (date) {
        let format = 'yyyy-MM-dd hh:mm:ss'
        return formatDate(date, format)
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
