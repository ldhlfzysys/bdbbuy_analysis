<template>
  <div id="main" style="margin-left: 3%;margin-right: 3%;margin-top: 20px">
    <Row>
      <Col :xs="8" :sm="8" :md="8" :lg="8">
        <h2 style="color: #363e4f;text-align: left;">销售数据一览</h2>
      </Col>

      <Select v-model="areaModel" multiple style="width:200px;float: right;margin-right: 10px">
        <Option v-for="item in areaList" :value="item.value" :key="item.value">{{ item.label }}</Option>
      </Select>

      <el-date-picker
        v-model="dateValue"
        type="datetimerange"
        :picker-options="pickerOptions"
        range-separator="To"
        start-placeholder="Start date"
        end-placeholder="End date"
        style="float: right;margin-right: 50px">
      </el-date-picker>
    </Row>

    <br>
    <br>
    <Row>
      <Tabs type="card">
        <TabPane :label="saleCard" style="height: 800px">
          销售数据内容
        </TabPane>
        <TabPane :label="saleCard">标签二的内容</TabPane>
      </Tabs>

    </Row>

  </div>
</template>

<script>
  import {serverBaseURL} from '../../globalConfig'

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

        areaModel:"",

        saleCard: (h) => {
        return h('div',
          {style:{
              width:'300px',
              height:'180px',
              backgroundColor:'transparent'}},
          [
            h('Card', {
              props: {
                title: "销售数据",
                bordered: false,
                padding: 0,
                backgroundColor:'transparent'
              }
            })
          ])
        }

      }
    },
    mounted: function () {
      // 页面加载
      console.log('这里是销售统计页面')
      // this.getData()
      this.getAreaList()
      this.getShotcuts()
    },
    methods: {
      showSaleMoney:function () {
        console.log('cccccc')
      },
      showOrderInfo:function () {

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
    height: 200px;
  }

  .ivu-tabs.ivu-tabs-card>.ivu-tabs-bar .ivu-tabs-nav-container  {
    height: 200px;
  }

  .ivu-tabs.ivu-tabs-card>.ivu-tabs-bar .ivu-tabs-tab {
    height: 200px;
  }

  .ivu-card {
    background: inherit;
  }

  .ivu-card-head {
    border-bottom: 0px;
  }




</style>
