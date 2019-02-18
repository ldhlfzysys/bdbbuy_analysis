import echarts from 'echarts'

export var chartTimeStatistic = function (dataDic) {

  var rotate = dataDic.rotate ?  dataDic.rotate : 0

  var endValue = dataDic.endValue ?   dataDic.endValue : 22

  var  option = {
    tooltip: {
      trigger: 'item',
      axisPointer: {
        type: 'cross'
      }
    },
    grid: {
      top: 50,
      left: 20,
      containLabel: true
    },
    legend: {
      top:30,
      data: dataDic.legendData,
      tooltip: {
        show: true
      }
    },
    xAxis: {
      type: dataDic.xAxisType,
      splitNumber: 20,
      axisLine: {
        onZero: false,
      },
      min: dataDic.minValue,
      max: dataDic.maxValue,
      data: dataDic.xAxisData,
      axisLabel:{
        interval:0,
        rotate:rotate
      }

    },
    yAxis: {
      type: 'value',
      name: dataDic.yUnit,
      minInterval : 1,

    },
    title: [{
      left: 'center',
      text: dataDic.title,
      subtext: dataDic.subtitle
    }],
    series: dataDic.series,
    dataZoom: [{
      type: 'inside',
      show: true,
      startValue: 0,
      endValue: endValue,
      disabled:true,
      xAxisIndex:[0],
    }, {
      startValue: 0,
      endValue: endValue,
      // height: 10,
      bottom: 0,
      type: 'slider',
      show: true,
      zoomLock:true,
      xAxisIndex:[0],
      handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
      handleSize: 0,
      handleColor: '#ddd',
      filterMode: 'filter',
      handleStyle: {
        color: '#fff',
        shadowBlur: 3,
        shadowColor: 'rgba(0, 0, 0, 0.6)',
        shadowOffsetX: 2,
        shadowOffsetY: 2
      }
    }],
  };
  return option;

}

export var chartAreaStatistic = function (dataDic) {

  var option = {
    title: {
      text: dataDic.title,
      left: 'center',
      top: 20,
      textStyle: {
        color: '#000'
      }
    },

    tooltip : {
      trigger: 'item',
      formatter: "{a} <br/>{b} : {c} ({d}%)"
    },

    visualMap: {
      show: false,
      min: dataDic.min,
      max: dataDic.max,
      inRange: {
        colorLightness: [0, 0.6]
      }
    },
    series : [
      {
        name:'区域数据',
        type:'pie',
        radius : '70%',
        center: ['50%', '50%'],
        data:dataDic.data.sort(function (a, b) { return a.value - b.value; }),
        roseType: 'radius',
        label: {
          normal: {
            textStyle: {
              color: 'rgba(0, 0, 0, 1)',
              formatter: "{a} <br/>{b} : {c} ({d}%)"
            }
          }
        },
        labelLine: {
          normal: {
            lineStyle: {
              color: 'rgba(0, 0, 0, 1)',
              formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            smooth: 0.2,
            length: 10,
            length2: 20
          }
        },
        itemStyle: {
          normal: {
            color: '#c23531',
            shadowBlur: 5000,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },

        animationType: 'scale',
        animationEasing: 'elasticOut',
        animationDelay: function (idx) {
          return Math.random() * 200;
        }
      }
    ]
  };
  return option;

}


