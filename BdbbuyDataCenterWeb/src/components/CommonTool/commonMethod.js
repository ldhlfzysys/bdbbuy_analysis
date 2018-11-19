

export function formatDate (date, fmt) {
  if (/(y+)/.test(fmt)) {
    fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length));
  }
  let o = {
    'M+': date.getMonth() + 1,
    'd+': date.getDate(),
    'h+': date.getHours(),
    'm+': date.getMinutes(),
    's+': date.getSeconds()
  };
  for (let k in o) {
    if (new RegExp(`(${k})`).test(fmt)) {
      let str = o[k] + '';
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? str : padLeftZero(str));
    }
  }
  return fmt;
};

function padLeftZero (str) {
  return ('00' + str).substr(str.length);
};

export function isString(obj){ //判断对象是否是字符串
  return Object.prototype.toString.call(obj) === "[object String]";
};

export function customDateParse(date_str) {
  return new Date(date_str.replace(/-/g,"/").replace(/Z/g,"").replace(/T/g," "))
}

export function range(x, y){
  var range_list = []
  for (let i = x; i <= y; i++) {
    range_list.push(i)
  }
  return range_list
}

export function getTimeByTimeZone(timeZone) {
  var d = new Date();
  var localTime = d.getTime();
  var localOffset = d.getTimezoneOffset() * 60000; //获得当地时间偏移的毫秒数,这里可能是负数
  var utc = localTime + localOffset; //utc即GMT时间
  var offset = timeZone; //时区，北京市+8  加拿大为 -5
  var  localSecondTime = utc + (3600000 * offset);  //本地对应的毫秒数
  var date = new Date(localSecondTime);
  console.log("根据本地时间得知" + timeZone + "时区的时间是 " + date.toLocaleString());
  console.log("系统默认展示时间方式是：" + date);
  return date;
}
