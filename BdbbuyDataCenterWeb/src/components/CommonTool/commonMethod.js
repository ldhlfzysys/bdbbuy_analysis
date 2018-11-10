

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
