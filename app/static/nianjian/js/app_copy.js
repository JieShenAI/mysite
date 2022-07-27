/**
 * @author hotsuitor@qq.com
 * @createTime 2018/2/23
 * @version v3.0  2018/4/3
 * @version v3.1  2018/4/10
 * @version v3.3  2018/4/12
 */
//地图容器
var chart = echarts.init(document.getElementById("main"));
chart.showLoading();

loadMap(searchtime);
/**
 * 封装绘制地图函数，month 改变 map重新渲染
 */
function loadMap(searchtime) {
  let mapName = "中国";
  //绘制全国地图
  $.getJSON(chinaJson, function (data) {
    chart.hideLoading();
    mapChina = data;
    let mapJsonData = []; // 组装临时数据，用于地图上 label和value的渲染

    for (var i = 0; i < data.features.length; i++) {
      mapJsonData.push({
        id: data.features[i].id,
        name: data.features[i].properties.name,
      });
    }
    /** mapJsonData
      0: {id: '710000', name: '台湾'}
      1: {id: '130000', name: '河北'}
     */

    //注册地图
    echarts.registerMap(mapName, data);
    //绘制地图，样式，第一次渲染
    renderMap(mapName, data);

    /**获取省份数据*/
    Promise.all([ajaxGet(getProvNumber2000Url)]).then(
      (result) => {
        renderPrimaryMap(result);
      },
      (error) => {
        console.error("拿不到省份数据");
        // renderPrimaryMap(mapJsonData, true);
      }
    );

    /**
     * @description: 渲染二级地图，城市
     * @param {Array}  result=后台返回的地区关联数据
     * @param {Boolean} flag=不用后台数据渲染
     * @return:
     */
    function renderPrimaryMap(result, flag) {
      let tmp = [];
      if (flag) {
        result.forEach((item) => {
          tmp.push({
            id: item.id,
            name: item.name,
            // 数据
            value: 11,
          });
        });
      } else {
        let curProvince = result[0]
        let gdp = 0
        mapJsonData.forEach(function (val) {
          t_id = Number(val.id)
          if (typeof curProvince[t_id] == 'undefined') {
            gdp = 0
          }
          else {
            gdp = curProvince[t_id].GDP
          }
          tmp.push({
            id: val.id,
            name: val.name,
            // 数据
            value: parseInt(gdp),
          });
        })
      }

      //获取最大值，并排序
      let maxData = getMaxDataAndSort(tmp);
      //绘制地图，拿到数据后再渲染一次
      renderMap(mapName, data, tmp, maxData.maxData);
      // getRegionPreMonthRatio(maxData.maxDataId, searchtime);
    }
  });
}

//地图单击事件
chart.on("click", function (params) {
  console.log("点击");
  console.log(params);
  for (var key in params.data) {
    console.log(key + ":" + params.data[key]);
  }
  if (!(params.data.id || params.data.cityid)) {
    // 有省id，市id才有下一级
    console.error("该地图没有下一级地区了");
    return;
  }
  //隐藏右键返回菜单
  $("#contextMenu").hide();
  let mapJsonData = []; // 渲染地图name的数组
  if (params.name in provinces) {
    //二级直辖市数据渲染
    if (special.indexOf(params.name) >= 0) {
      Promise.all([ajaxRequest(getCityNumberUrl)]).then(
        (result) => {
          try {
            let curMonthResult = stringToJson(result[0]);
            if (curMonthResult.errcode == 1) {
              getAreaNumber(
                params.name,
                curMonthResult.msg[0].cityid,
                searchtime
              );
            }
          } catch (error) {
            getSecondMap(params);
          }
        },
        (error) => {
          console.error("请求市级数据失败", error);
          getSecondMap(params);
        }
      );
    } else {
      //如果点击的是34个省、市、自治区，绘制选中地区的二级地图
      getSecondMap(params);
    }
  } else {
    //显示县级地图
    getThridMap(params);
  }

  /**
   * @description: 请求获取二级地图json文件
   * @param {Object} params=地图参数
   * @return:
   */
  function getSecondMap(params) {
    //jie
    console.log("jie2: ");
    console.log(params.data.id);

    $.getJSON(provinceJson + provinces[params.name] + ".json", function (data) {
      echarts.registerMap(params.name, data);

      for (var i = 0; i < data.features.length; i++) {
        // 读取地图的 name 用来组成 echart 需要的形式
        mapJsonData.push({
          name: data.features[i].properties.name,
          value: Math.floor(Math.random() * 10000),
        });
      }

      // // jie
      // mapJsonData.forEach(
      //   (v)=>console.log(v)
      // )
      renderMap(params.name, mapJsonData);
      if (params.data.id !== "undifiend") {
        // 拿到第二级的数据
        getCityNumber(params.name, params.data.id, searchtime, data);
      }
    });
  }

  /**
   * @description: 请求获取三级地图json文件
   * @param {Object} params=地图参数
   * @return:
   */
  function getThridMap(params) {
    $.getJSON(cityJson + cityMap[params.name] + ".json", function (data) {
      echarts.registerMap(params.name, data);
      let mapJsonData = [];
      for (var i = 0; i < data.features.length; i++) {
        mapJsonData.push({
          name: data.features[i].properties.name,
        });
      }
      renderMap(params.name, mapJsonData);
      if (params.data.cityid) {
        // console.log('204', res.msg[0].cityid, res.msg[0].city)
        //这里传递的城市名有问题“北京市”，渲染地图的名字是“北京”，所以地图名要用原来的名字渲染
        // getAreaNumber(params.name, params.data.cityid, searchtime, data)
        // 需要把第3级的名称和数值传过去
        getAreaNumber(params.name, params.data.cityid, searchtime, data)
      }
    });
  }
  /**
   * 绑定数据入栈事件
   */
  let n = 1;
  if (special.indexOf(params.seriesName) == -1) {
    n = 2;
  }
  // FiXED:  2级下钻会有问题， 函数顶部加入下钻层级判断
  if (mapStack.length < n) {
    //将上一级地图信息压入mapStack
    mapStack.push({
      mapName: curMap.mapName,
      mapJson: curMap.mapJson,
      colorMax: curMap.colorMax,
      sortData: curMap.sortData,
      titledata: curMap.titledata,
    });
    console.log("数据入栈", mapStack);
  }
});

/**
 * 右键直接返回上一级
 */
chart.on("contextmenu", (params) => {
  goBack();
});
/**
 * 左上角返回按钮
 */
$("#goBack").on("click", function (data) {
  goBack();
});

/**
 * 封装返回上一级事件
 */
function goBack() {
  //获取上一级地图信息
  let map = mapStack.pop();
  if (!map) {
    console.log("没有入栈数据了");
    return;
  }
  echarts.registerMap(map.mapName, map.mapJson);
  sortData = map.sortData;
  titledata = map.titledata;
  renderMap(map.mapName, map.mapJson, map.sortData, map.colorMax);
}

/**
 *
 * @param {地图标题} mapTitle
 * @param {客户数} customerNum
 * @param {地图json数据} mapJson
 * @param {最大颜色值} colorMax
 */
function renderMap(mapTitle, mapJson, customerNum, colorMax = 1500) {
  //地图配置参数，参数按顺序渲染
  option = {
    backgroundColor: "#F7EED6", //地图画布背景颜色  "#F7EED6"米黄色  "#efefef"灰色
    title: {
      //地图文本
      text: mapTitle,
      subtext: "右键返回上一级",
      left: "center",
      textStyle: {
        color: "#000",
        fontSize: 26,
        fontWeight: "normal",
        fontFamily: "Microsoft YaHei",
      },
      subtextStyle: {
        color: "rgb(55, 75, 113)",
        fontSize: 18,
        fontWeight: "normal",
        fontFamily: "Microsoft YaHei",
      },
    },
    // 鼠标 hover 折线图
    // tooltip: {
    //   padding: 0,
    //   enterable: false,
    //   transitionDuration: 1,
    //   textStyle: {
    //     color: "#000",
    //     decoration: "none"
    //   },
    //   formatter: function(params) {
    //     console.log(params);
    //     let tipHtml = `
    //       <div style="height:360px;width:450px;border-radius:5px;background:#fff;box-shadow:0 0 10px 5px #aaa">
    //          <div style="height:40px;width:100%;border-radius:5px;background:#F8F9F9;border-bottom:1px solid #F0F0F0; text-align: center;">
    //               <span style="line-height:40px;">
    //               ${params.name}
    //               </span>
    //               <span style="color: #111; font-size: 12px;">---表示平均数</span>
    //           <div id="tooltipBarId" style="height:300px;width:100%;border-radius:0 0 5px 0;background:#fff"></div>
    //       </div>
    //       `;
    //     setTimeout(function() {
    //       tooltipCharts(params);
    //     }, 10);
    //     return tipHtml;
    //   }
    // },

    tooltip: {
      //提示框信息
      trigger: "item",
      // formatter: '{b}\n{c}人',
      formatter: "{b}\n{c}亿",
    },
    toolbox: {
      //工具box
      show: true,
      orient: "vertical",
      left: "right",
      top: "center",
      right: 20,
      feature: {
        dataView: { readOnly: false },
        restore: {},
        saveAsImage: {},
      },
      iconStyle: {
        normal: {
          color: "#fff",
        },
      },
    },
    //左下角的颜色条
    visualMap: {
      show: true,
      min: 0,
      max: colorMax,
      left: "left",
      top: "bottom",
      text: ["高", "低"], // 文本，默认为数值文本
      calculable: true,
      // seriesIndex: [1],    //会使颜色失效
      color: ["#c05050", "#e5cf0d", "#5ab1ef"], //色阶范围
      dimension: 0,
    },
    grid: {
      left: 130,
      top: 100,
      botton: 40,
      width: "20%",
    },
    xAxis: [
      {
        position: "top",
        type: "value",
        boundaryGap: false,
        splitLine: {
          show: false,
        },
        axisLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        axisLabel: {
          color: "#ff461f",
        },
      },
    ],
    yAxis: [
      {
        type: "category",
        data: titledata,
        triggerEvent: true,
        axisTick: {
          alignWithLabel: true,
        },
        axisLine: {
          show: true,
          lineStyle: {
            show: true,
            color: "#2ec7c9",
          },
        },
      },
    ],
    series: [
      {
        name: mapTitle, //上面的下钻用到seriesName绑定下一级，换name绑定
        type: "map",
        map: mapTitle,
        roam: false,
        height: "100%",
        zoom: 0.75,
        z: 1,
        label: {
          //地图上的文本标签
          normal: {
            show: true,
            position: "inside", //文本标签显示的位置
            textStyle: {
              color: "#fff", //文本颜色
              fontSize: 14,
            },
            formatter: "{b}\n{c}", //文本上显示的值  data:[{name: "地名", value: 数据}],  {b}表示label信息,{c}代表value
          },
          emphasis: {
            show: true,
            position: "inside",
            textStyle: {
              color: "#fff",
              fontSize: 13,
            },
          },
        },
        itemStyle: {
          normal: {
            areaColor: "#5ab1ef", //地图块颜色#DCE2F1  浅蓝#2B91B7
            borderColor: "#EBEBE4", //#EBEBE4灰色
          },
          emphasis: {
            areaColor: "rgb(254,153,78)", //s鼠标放上去，地图块高亮显示的颜色
          },
        },
        data: customerNum,
      },
      {
        name: mapTitle,
        type: "bar",
        z: 4,
        label: {
          normal: {
            show: true,
          },
          empahsis: {
            show: true,
          },
        },
        itemStyle: {
          emphasis: {
            color: "rgb(254,153,78)",
          },
        },
        data: customerNum,
      },
    ],
    // 初始动画的时长，支持回调函数，可以通过每个数据返回不同的 delay 时间实现更戏剧的初始动画效果：
    animationDuration: 1000,
    animationEasing: "cubicOut",
    // 数据更新动画的时长。
    animationDurationUpdate: 1000,
  };

  //渲染地图
  chart.setOption(option);
  //保存当前状态数据，用于入栈出栈
  curMap = {
    mapName: mapTitle,
    mapJson: mapJson,
    colorMax: colorMax,
    sortData: sortData,
    titledata: titledata,
  };
}

/**
 * 获取城市数据
 * @param {省份} name
 * @param {省份id} id
 * @param {月份} searchtime
 * @param {地图json数据} data
 */
function getCityNumber(name, id, searchtime, data) {
  console.log("id: " + id);
  if (!id) {
    return;
  }
  id_name = {}
  for (let i = 0; i < data.features.length; i++) {
    let t_id = data.features[i].id;
    let t_name = data.features[i].properties.name;
    id_name[t_id] = t_name;
  }

  Promise.all([ajaxGet(secondUrl + id.slice(0, 2) + ".json")]).then(
    (result) => {
      renderSecondMap(result, id_name);
    },
    (error) => {
      console.error("请求城市数据失败", error);
    }
  );

  /**
   * @description: 渲染二级地图，城市
   * @param {JSONString} resp=请求后台返回的地区关联数据
   * @param {Boolean} flag=标识位，请求mock数据失败，用地图数据渲染的 true=地图数据渲染
   * @return:
   */
  function renderSecondMap(resp, id_name) {
    let tmp = [];
    for (var key in id_name) {
      var gdp = 0
      if (typeof resp[0][Number(key)] == "undefined") {
        gdp = 0
      } else {
        gdp = resp[0][Number(key)].GDP
      }
      tmp.push({
        cityid: key, //需要加上cityid传递渲染，下一级地图渲染需要用到
        name: id_name[key],
        // value: curMonthResult.msg[i].num,
        // 数据
        value: gdp,
      });
    }
    let maxData = getMaxDataAndSort(tmp);
    renderMap(name, data, tmp, maxData.maxData);
    // getRegionPreMonthRatio(maxData.maxDataId, searchtime);
  }
}

/**
 * 获取县区数据
 * @param {城市名} cityName
 * @param {城市id} cityId
 * @param {月份}  searchtime
 * @param {地图json数据} data
 */
function getAreaNumber(cityName, cityId, searchtime, data) {
  let postData3 = {
    parentid: "cityid",
    value: cityId,
  };

  Promise.all([ajaxRequest(secondUrl + cityId.slice(0, 2) + ".json")]).then(
    (result) => {

      // id_name = {}
      // for (let i = 0; i < data.features.length; i++) {
      //   let t_id = data.features[i].id;
      //   let t_name = data.features[i].properties.name;
      //   id_name[t_id] = t_name;
      // }
      // console.log("data: 123");
      // console.log(data);
      // console.log(id_name);
      prefix = cityId.slice(0, 4)
      console.log("prefix: " + prefix);
      let tmp = [];
      for (var key in result[0]) {
        if (key.slice(0, 4) == prefix && key.slice(-2) != "00") {

          let gdp = 0
          if (typeof result[0][key].GDP == "undefined") {
            gdp = 0
          } else {
            gdp = parseInt(result[0][key].GDP)
          }
          tmp.push({
            areaid: key,
            name: result[0][key]["COUNTY"],
            // value: Math.floor(Math.random() * 10 + 1),
            // 数据
            value: gdp,
          });

        }
      }

      let maxData = getMaxDataAndSort(tmp);
      renderMap(cityName, data, tmp, maxData.maxData);
      //getRegionPreMonthRatio(maxData.maxDataId, searchtime);
    },
    (error) => {
      console.error("获取县区数据失败", error);
    }
  );
}

let areaList = [];
let vm = new Vue({
  el: "#trend-line",
  data: {
    areaList: areaList,
    modalTitle: [],
    cpModalTitle: [],
    searchtime: searchtime,
    time: 0,
    otime: 0,
  },
  methods: {
    setAreaList(data) {
      // let $_self = this
      // $_self._data.areaList = data //这里有个坑，_data
      this.areaList = data; // vue是这样写的，内部有代理
    },
  },
  watch: {
    modalTitle(val, oldVal) {
      let $_self = this;
      if (val.length > oldVal) {
        this.time++;
        this.cpModalTitle.push(val);
      } else {
        // $_self._data.time--;
      }
      //TODO 取消不请求数据
      if (this.time > this.otime) {
        getRegionPreMonthRatio(val, this.searchtime);
      }
    },
  },
});

/**
 *
 * @param {未排序数据} originData
 * @return {倒序排序的数据} maxData
 */
function getMaxDataAndSort(originData) {
  if (originData == "undefined") {
    return;
  }
  titledata = [];
  sortData = [];
  sortData = originData.sort(numDescSort);
  let maxData = sortData.slice(-1)[0]["value"];
  let maxDataId = sortData.slice(-1)[0]["id"];
  if (!maxDataId) {
    maxDataId = sortData.slice(-1)[0]["cityid"]
      ? sortData.slice(-1)[0]["cityid"]
      : sortData.slice(-1)[0]["areaid"];
  }
  for (let i = 0; i < sortData.length; i++) {
    titledata.push(sortData[i].name);
  }
  areaList = [...sortData].reverse();
  vm.setAreaList(areaList);
  return {
    maxDataId,
    maxData,
  };
}
