
<template>
  <div id="app">
    <!--<img src="./assets/logo.png">-->
    <Menu mode="horizontal" :active-name="menuActiveName"  @on-select="gotoPage" style="z-index:99999999999" >
      <MenuItem name="orderData" id="orderData">
        <Icon type="ios-stats-outline" />
        销量统计
      </MenuItem>

      <Submenu name="2" id="inventoryWarning">
        <template slot="title">
          <Icon type="ios-warning"></Icon>
          库存预警
        </template>
        <MenuItem name="inventoryWarning_count" id="inventoryWarning_1">按个数筛选</MenuItem>
        <MenuItem name="inventoryWarning_ordercount" id="inventoryWarning_2">按销量筛选</MenuItem>
        <MenuItem name="inventoryWarning_date" id="inventoryWarning_3">筛选过期商品</MenuItem>
      </Submenu>

      <MenuItem name="saleData" id="saleData" v-bind:style="{display:displayType}">
        <Icon type="ios-stats" />
        销售统计
      </MenuItem>

      <MenuItem name="driverData" id="driverData" v-bind:style="{display:displayType}">
        <Icon type="md-car" />
        司机端统计
      </MenuItem>

    </Menu>
    <router-view></router-view>
  </div>
</template>

<script>
  import {setCookie, getCookie} from './cookie.js'
  import {serverBaseURL} from './globalConfig'

  export default {
    name: 'App',
    data() {
      return {
        menuActiveName: 'orderData',
        auth_num: -1,
        displayType: "none"
      }

    },

    mounted: function () {

      var user_cookie = getCookie('admin_cookie')
      var auth_cookie = getCookie('admin_auth')

      if (this.$route.query.user != undefined) {
        // 从后台跳转
        if ( user_cookie == null || auth_cookie == null || this.$route.query.user != user_cookie) {
          // 未登陆过或账户切换，请求权限
          let url = serverBaseURL + 'adminuser/getAuth?user=' + this.URLencode(this.$route.query.user)
          this.$http.get(url).then(function (response) {
            var status = response.status;
            if (status == 200) {
              var result = response.body
              this.auth_num = result['data']['auth'];
              setCookie('admin_user_name', result['data']['user_name'], 3600*24*365 )
              setCookie('admin_cookie', this.$route.query.user, 3600*24*365 )
              setCookie('admin_auth', this.auth_num, 3600*24*365 )

              this.menuActiveName = this.$route.path.split('?')[0].replace('/', '')
              this.dealAuthPage()
            }
          }, function (response) {
            console.log("发生错误")
            var str = response.body.message
            this.$Message.success(str)
          });


        } else {
          // 同一账户
          this.auth_num = getCookie('admin_auth')
          this.dealAuthPage()
        }

      } else {
        // 本系统登陆
        var user_cookie = getCookie('admin_user_name')
        if (user_cookie == null || auth_cookie == null) {
          // TODO:未登录状态,前往登录页面
          this.$router.push('login')
        } else {
          // 已登录状态
          this.auth_num = getCookie('admin_auth')
          this.dealAuthPage()
        }

      }


    },

    methods: {

      dealAuthPage:function (){
        var saleData_ele = document.getElementById('saleData')
        if (this.auth_num == 23) {
          if (saleData_ele != undefined) {
            saleData_ele.parentElement.removeChild(saleData_ele)
          }

        } else if (this.auth_num == 25) {
          this.displayType = "block";

        } else {

        }

      },

      gotoPage:function (name) {
        var pageName = name
        var routerParam = {path: pageName}
        if (name.indexOf('inventoryWarning_') != -1) {
          var pageNameList = name.split('_')
          pageName = pageNameList[0]
          routerParam = {path: pageName, query:{type: pageNameList[1]}}
        }

        this.$router.push(routerParam)
      },

      URLencode:function (sStr) {
        return escape(sStr).replace(/\+/g, '%2B').replace(/\"/g,'%22').replace(/\'/g, '%27').replace(/\//g,'%2F');
      }
    }
  }
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 10px;
}


</style>
