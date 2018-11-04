<template>
  <div id="main" style="margin-left: 3%;margin-right: 3%;margin-top: 20px">
    <Row>
      <Col :xs="8" :sm="8" :md="8" :lg="8">
        <h2 style="color: #363e4f;text-align: left">销售数据一览</h2>
      </Col>
      <el-date-picker
        v-model="dateValue"
        type="datetimerange"
        :picker-options="pickerOptions"
        range-separator="To"
        start-placeholder="Start date"
        end-placeholder="End date"
        style="float: right">
      </el-date-picker>
    </Row>

    <br>
        <!--<el-tabs v-model="activeName" @tab-click="handleClick" type="border-card">-->
            <!--<el-tab-pane name="first">-->
                <!--<span slot="icon">-->
                    <!--<el-card shadow="never" style="background-color: inherit">-->
                      <!--从不显示-->
                    <!--</el-card>-->
                <!--</span>-->
              <!--world-->
            <!--</el-tab-pane>-->
            <!--<el-tab-pane label="配置管理" name="second">-->
                <!--<span slot="label">-->
                    <!--<el-card shadow="never" style="margin:0 -20px -12px -20px;background-color: inherit">-->
                      <!--从不显示-->
                    <!--</el-card>-->
                <!--</span>-->
              <!--world-->
            <!--</el-tab-pane>-->
        <!--</el-tabs>-->
    </div>

  </div>
</template>

<script>
  export default {
    name: 'saleData',
    data () {
      return {
        split1: 0.5,
        pickerOptions: '',
        dateValue: '',
      }
    },
    mounted: function () {
      // 页面加载
      console.log('这里是销售统计页面')
      // this.getData()
      this.getShotcuts()
    },
    methods: {
      showSaleMoney:function () {
        console.log('cccccc')
      },
      showOrderInfo:function () {

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

<style scoped>
  .demo-tabs-style1 > .ivu-tabs-card > .ivu-tabs-content {
    height: 120px;
    margin-top: -16px;
  }

  .demo-tabs-style1 > .ivu-tabs-card > .ivu-tabs-content > .ivu-tabs-tabpane {
    background: #fff;
    padding: 16px;
  }

  .demo-tabs-style1 > .ivu-tabs.ivu-tabs-card > .ivu-tabs-bar .ivu-tabs-tab {
    border-color: transparent;
  }

  .demo-tabs-style1 > .ivu-tabs-card > .ivu-tabs-bar .ivu-tabs-tab-active {
    border-color: #fff;
  }
  .demo-tabs-style2 > .ivu-tabs.ivu-tabs-card > .ivu-tabs-bar .ivu-tabs-tab{
    border-radius: 0;
    background: #fff;
  }
  .demo-tabs-style2 > .ivu-tabs.ivu-tabs-card > .ivu-tabs-bar .ivu-tabs-tab-active{
    border-top: 1px solid #3399ff;
  }
  .demo-tabs-style2 > .ivu-tabs.ivu-tabs-card > .ivu-tabs-bar .ivu-tabs-tab-active:before{
    content: '';
    display: block;
    width: 100%;
    height: 1px;
    background: #3399ff;
    position: absolute;
    top: 0;
    left: 0;
  }

</style>
