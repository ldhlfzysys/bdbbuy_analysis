webpackJsonp([1],{0:function(t,e){},KNwI:function(t,e){},N0nf:function(t,e){},NHnr:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=a("7+uW"),i={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"app"}},[a("Menu",{attrs:{mode:"horizontal","active-name":t.menuActiveName},on:{"on-select":t.gotoPage}},[a("MenuItem",{attrs:{name:"saleData"}},[a("Icon",{attrs:{type:"ios-stats"}}),t._v("\n      销售统计\n    ")],1),t._v(" "),a("Submenu",{attrs:{name:"2"}},[a("template",{slot:"title"},[a("Icon",{attrs:{type:"ios-warning"}}),t._v("\n        库存预警\n      ")],1),t._v(" "),a("MenuItem",{attrs:{name:"inventoryWarning_count",id:"inventoryWarning_1"}},[t._v("按个数筛选")]),t._v(" "),a("MenuItem",{attrs:{name:"inventoryWarning_ordercount",id:"inventoryWarning_2"}},[t._v("按销量筛选")]),t._v(" "),a("MenuItem",{attrs:{name:"inventoryWarning_date",id:"inventoryWarning_3"}},[t._v("筛选过期商品")])],2)],1),t._v(" "),a("router-view")],1)},staticRenderFns:[]};var o=a("VU/8")({name:"App",data:function(){return{menuActiveName:"saleData"}},mounted:function(){this.menuActiveName=this.$route.path.replace("/","")},methods:{gotoPage:function(t){var e=t,a={path:e};if(-1!=t.indexOf("inventoryWarning_")){var n=t.split("_");a={path:e=n[0],query:{type:n[1]}}}this.$router.push(a)}}},i,!1,function(t){a("N0nf")},null,null).exports,r=a("/ocq"),s=a("8+8L"),l=(a("hyYw"),a("L7Pj"),a("UQDN")),u=a.n(l),c=a("H93t"),p=a.n(c),d=(a("TsY+"),window.location.host),g="";g="http://"+d+"/bdbbuyanalysisserver/";var h={name:"inventoryWarning",watch:{$route:function(t,e){this.pageType=this.$route.query.type,this.setTableColumn(),this.getData()}},data:function(){return{page_size_opts:[20,40,50,100],pageSize:20,tableData:[],tableColumns:[],totalCount:0,allProductList:[],pageType:"count",countInfo:5,orderDay:7,pageCurrent:1,tableLoading:!1,cancelTokenFn:null}},mounted:function(){console.log("这里是库存预警页面"),this.pageType=this.$route.query.type,this.setTableColumn(),this.getData()},methods:{getData:function(){this.tableData=[],this.pageCurrent=1,this.totalCount=0,this.tableLoading=!0;var t=g+"product/getWarnigProduct";"count"==this.pageType?t=t+"?lowCount="+this.countInfo:"date"==this.pageType?t=t+"?outOfDate="+!0:"ordercount"==this.pageType&&(t=t+"?orderDay="+this.orderDay),this.$http.get(t).then(function(t){var e=t.status;if(this.tableLoading=!1,200==e){var a=t.body;this.allProductList=a.data.order_list,this.totalCount=a.data.totalCount,this.changePage(1)}},function(t){console.log("发生错误");var e=t.body.message;this.tableLoading=!1,this.$Message.success(e)})},setTableColumn:function(){if(this.tableColumns=[{title:"id",key:"product_id",width:100,align:"center"},{title:"中文名",key:"name",width:200,align:"left"},{title:"SKU",key:"sku",align:"center"},{title:"售价",key:"price",align:"center"},{title:"保质期",key:"quality_date",align:"center"},{title:"库存数量",key:"product_qty",align:"center"}],"ordercount"==this.pageType){var t={title:"过去"+this.orderDay+"天销量",key:"order_count",align:"center"};this.tableColumns.push(t);this.tableColumns.push({title:"库存差值",key:"delta_count",align:"center"})}},changePage:function(t){var e=0,a=this.allProductList.length;this.allProductList.length>this.pageSize&&(e=this.pageSize*(t-1),a=this.pageSize*t),this.tableData=this.allProductList.slice(e,a)}}},v={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticStyle:{"margin-left":"3%","margin-right":"3%","margin-top":"20px"},attrs:{id:"main"}},[a("div",{staticClass:"row"},[a("p",{staticStyle:{"margin-left":"0px",width:"400px"},attrs:{hidden:"count"!=t.pageType}},[a("label",[t._v("输入库存最低数量：")]),t._v(" "),a("input",{directives:[{name:"model",rawName:"v-model",value:t.countInfo,expression:"countInfo"}],staticClass:"normal",attrs:{type:"text"},domProps:{value:t.countInfo},on:{input:function(e){e.target.composing||(t.countInfo=e.target.value)}}}),t._v(" "),a("label",[t._v("件")]),t._v(" "),a("Button",{on:{click:t.getData}},[t._v("\n        刷新\n      ")]),t._v(" "),a("small")],1),t._v(" "),a("p",{staticStyle:{"margin-left":"0px",width:"300px"},attrs:{hidden:"ordercount"!=t.pageType}},[a("label",[t._v("按过去")]),t._v(" "),a("input",{directives:[{name:"model",rawName:"v-model",value:t.orderDay,expression:"orderDay"}],staticClass:"normal",attrs:{type:"text"},domProps:{value:t.orderDay},on:{input:function(e){e.target.composing||(t.orderDay=e.target.value)}}}),t._v(" "),a("label",[t._v("天销量")]),t._v(" "),a("Button",{on:{click:t.getData}},[t._v("\n        查找\n      ")]),t._v(" "),a("small")],1),t._v(" "),a("br"),t._v(" "),a("p",{staticStyle:{"margin-left":"0px",width:"360px"}},[a("label",{staticStyle:{"text-align":"left"}},[t._v("(查找的数据包含：库存低于"+t._s(t.orderDay)+"天销量的数据和总库存低于5的数据)")])])]),t._v(" "),a("br"),t._v(" "),a("Table",{attrs:{border:"",data:t.tableData,columns:t.tableColumns,stripe:"",loading:t.tableLoading}}),t._v(" "),a("div",{staticStyle:{margin:"20px",overflow:"hidden"}},[a("div",{staticStyle:{float:"right"}},[a("Page",{ref:"pages",attrs:{total:t.totalCount,current:t.pageCurrent,"page-size":t.pageSize,"show-sizer":"","page-size-opts":t.page_size_opts,"show-total":""},on:{"on-change":t.changePage}})],1)])],1)},staticRenderFns:[]};var m=a("VU/8")(h,v,!1,function(t){a("kjsh")},"data-v-1b0b68be",null).exports,y={name:"saleData",mounted:function(){console.log("这里是销售统计页面")}},f={render:function(){this.$createElement;this._self._c;return this._m(0)},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("div",[e("h1",[this._v("销售数据（暂时未上线）")])])}]};var _=a("VU/8")(y,f,!1,function(t){a("KNwI")},"data-v-97c4ab68",null).exports;n.default.config.productionTip=!1,n.default.use(r.a),n.default.use(s.a),n.default.use(u.a),n.default.use(p.a);var b=new r.a({mode:"history",base:"/bdbbuyanalysis/",routes:[{path:"/",component:_},{path:"/inventoryWarning",component:m},{path:"/saleData",component:_}]});new n.default({el:"#app",router:b,components:{App:o},template:"<App/>"})},"TsY+":function(t,e){},hyYw:function(t,e){},kjsh:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.90609cb8a6c4c3b29f65.js.map