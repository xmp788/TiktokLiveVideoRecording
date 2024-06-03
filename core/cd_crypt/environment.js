window = global;delete global;delete Buffer;
const myWindow={
  onwheelx:{_Ax: '0X21'},
  innerWidth:1920,
  innerHeight:150,
  outerWidth:1920,
  outerHeight:1050,
  screenX:0,
  screenY:0,
  pageYOffset:0,
  requestAnimationFrame:function () {return 'function requestAnimationFrame(){[native code]}'},
  getItem:function() {return 'function getItem(){[native code]}'},
  screen:{
    availHeight:1050,
    availLeft:0,
    availTop:0,
    availWidth:1920,
    colorDepth:24,
    height:1080,
    isExtended:false,
    onchange:null,
    orientation:ScreenOrientation={angle:0,type:'landscape-primary',onchange:null},
    pixelDepth:24,
    width:1920
  },
  _sdkGlueVersionMap:{sdkGlueVersion: '1.0.0.51', bdmsVersion: '1.0.1.5', captchaVersion: '4.0.2'},
  bdms:''
}
window ={
  ...window,...myWindow
}
// console.log(window)
XMLHttpRequest = function(){}
document={
  createElement: function (res) {
      // console.log("document.createElement ->", res)
      return '<span></span>'
  },
  documentElement: function (res) {
      console.log("document.documentElement ->", res)
  },
  createEvent: function (res) {
      console.log("document.createEvent ->", res)
  },
  all:[],
  body:'',
  referrer:''
}
navigator={
  appCodeName: "Mozilla",
  appName: "Netscape",
  appVersion:"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
  userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
  platform: "Win32",
  vendor: "Google Inc.",
  vendorSub: ""
}
//=====================================代理===============================
/* 
 function SetProxy(proxyArray){
  for (let i = 0; i < proxyArray.length; i++) {
    const handler = `{
      get: function (target, property, receiver) {
        if (target[property]==undefined){
          console.log('get:','${proxyArray[i]}.'+property+'=?',target[property], '该属性类型:',typeof(property));
        }
        return target[property];
      },
      set: function (target, property, value, receiver) {
        // if (target[property]==undefined){
          // console.log('set:','${proxyArray[i]}.'+property+'='+value, '\\n\\t属性类型:',typeof(property),'该属性值类型:', typeof(target[property]));
          // console.log('方法:', 'set', '对象:', '${proxyArray[i]}', '属性:', property, '属性类型:', typeof property, ',属性值:', value, ',属性值类型:', typeof target[property]);
        // }
        return Reflect.set(...arguments);
      }
    }`;
    eval(`try {
        ${proxyArray[i]};
        ${proxyArray[i]}=new Proxy(${proxyArray[i]},${handler})
      } catch (e) {
        ${proxyArray[i]}={};
        ${proxyArray[i]}=new Proxy(${proxyArray[i]},${handler})
    }`);
  }
};
SetProxy(['window','document','location','navigator','history', 'screen','localStorage']) 
 */