/**
 * @author hotsuitor@qq.com
 * @createTime 2018/2/23
 * @version v3.0  2018/4/3
 * @version v3.1  2018/4/10
 * @version v3.3  2018/4/12
 */
//地图容器
var chart = echarts.init(document.getElementById('main'))
chart.showLoading()

loadMap(searchtime)
/**
 * 封装绘制地图函数，month 改变 map重新渲染
 */
function loadMap(searchtime) {
  let mapName = '中国'
  //绘制全国地图
  $.getJSON(chinaJson, function (data) {
    chart.hideLoading()
    mapChina = data
    let mapJsonData = [] // 组装临时数据，用于地图上 label和value的渲染
    
    for (var i = 0; i < data.features.length; i++) {
      mapJsonData.push({
        id: data.features[i].id,
        name: data.features[i].properties.name,
      })
    }
    /** mapJsonData
      0: {id: '710000', name: '台湾'}
      1: {id: '130000', name: '河北'}
      2: {id: '140000', name: '山西'}
      3: {id: '150000', name: '内蒙古'}
      4: {id: '210000', name: '辽宁'}
      5: {id: '220000', name: '吉林'}
      6: {id: '230000', name: '黑龙江'}
      7: {id: '320000', name: '江苏'}
      8: {id: '330000', name: '浙江'}
      9: {id: '340000', name: '安徽'}
      10: {id: '350000', name: '福建'}
      11: {id: '360000', name: '江西'}
      12: {id: '370000', name: '山东'}
      13: {id: '410000', name: '河南'}
      14: {id: '420000', name: '湖北'}
      15: {id: '430000', name: '湖南'}
      16: {id: '440000', name: '广东'}
      17: {id: '450000', name: '广西'}
      18: {id: '460000', name: '海南'}
      19: {id: '510000', name: '四川'}
      20: {id: '520000', name: '贵州'}
      21: {id: '530000', name: '云南'}
      22: {id: '540000', name: '西藏'}
      23: {id: '610000', name: '陕西'}
      24: {id: '620000', name: '甘肃'}
      25: {id: '630000', name: '青海'}
      26: {id: '640000', name: '宁夏'}
      27: {id: '650000', name: '新疆'}
      28: {id: '110000', name: '北京'}
      29: {id: '120000', name: '天津'}
      30: {id: '310000', name: '上海'}
      31: {id: '500000', name: '重庆'}
      32: {id: '810000', name: '香港'}
      33: {id: '820000', name: '澳门'}
     */

    $('#select-date').val(searchtime)

    //注册地图
    echarts.registerMap(mapName, data)
    //绘制地图，样式，第一次渲染
    renderMap(mapName, data)

    /**获取省份数据*/
    Promise.all([ajaxRequest(getProvNumberUrl, searchtime)]).then(
      
      (result) => {
        renderPrimaryMap(result)
      },
      (error) => {
        console.error('拿不到省份数据')
        renderPrimaryMap(mapJsonData, true)
      }
    )

    /**
     * @description: 渲染二级地图，城市
     * @param {Array}  result=后台返回的地区关联数据
     * @param {Boolean} flag=不用后台数据渲染
     * @return:
     */
    function renderPrimaryMap(result, flag) {
      let tmp = []
      if (flag) {
        result.forEach((item) => {
          tmp.push({
            id: item.id,
            name: item.name,
            // value: Math.floor(Math.random() * 100 + parseInt(item.id)),
            // 数据
            value: 11,
          })
        })
      } else {
        console.log( "res" + result[0]);
        curMonthResult = stringToJson(result[0])
        console.log("cur " + curMonthResult.errcode);
        curMonthResult.msg.forEach(
          (v)=>{console.log(v);}
        )

        if (curMonthResult.errcode == 1) {
          /**通过id关联地图上对应位置的数据 */
          mapJsonData.forEach(function (val) {
            curMonthResult.msg.forEach(function (val2, index) {
              if (val.id === val2.provinceid) {
                tmp.push({
                  id: val.id,
                  name: val.name,
                  value: val2.num,
                  // 数据
                  // value: 111,
                })
              }
            })
          })
        }
      }
      //获取最大值，并排序
      let maxData = getMaxDataAndSort(tmp)
      //绘制地图，拿到数据后再渲染一次
      renderMap(mapName, data, tmp, maxData.maxData)
      // getRegionPreMonthRatio(maxData.maxDataId, searchtime)
    }
  })
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
    backgroundColor: '#F7EED6', //地图画布背景颜色  "#F7EED6"米黄色  "#efefef"灰色
    title: {
      //地图文本
      text: mapTitle,
      subtext: '右键返回上一级',
      left: 'center',
      textStyle: {
        color: '#000',
        fontSize: 26,
        fontWeight: 'normal',
        fontFamily: 'Microsoft YaHei',
      },
      subtextStyle: {
        color: 'rgb(55, 75, 113)',
        fontSize: 18,
        fontWeight: 'normal',
        fontFamily: 'Microsoft YaHei',
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
      trigger: 'item',
      formatter: '{b}\n{c}人',
    },
    toolbox: {
      //工具box
      show: true,
      orient: 'vertical',
      left: 'right',
      top: 'center',
      right: 20,
      feature: {
        dataView: { readOnly: false },
        restore: {},
        saveAsImage: {},
      },
      iconStyle: {
        normal: {
          color: '#fff',
        },
      },
    },
    //左下角的颜色条
    visualMap: {
      show: true,
      min: 0,
      max: colorMax,
      left: 'left',
      top: 'bottom',
      text: ['高', '低'], // 文本，默认为数值文本
      calculable: true,
      // seriesIndex: [1],    //会使颜色失效
      color: ['#c05050', '#e5cf0d', '#5ab1ef'], //色阶范围
      dimension: 0,
    },
    grid: {
      left: 130,
      top: 100,
      botton: 40,
      width: '20%',
    },
    xAxis: [
      {
        position: 'top',
        type: 'value',
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
          color: '#ff461f',
        },
      },
    ],
    yAxis: [
      {
        type: 'category',
        data: titledata,
        triggerEvent: true,
        axisTick: {
          alignWithLabel: true,
        },
        axisLine: {
          show: true,
          lineStyle: {
            show: true,
            color: '#2ec7c9',
          },
        },
      },
    ],
    series: [
      {
        name: mapTitle, //上面的下钻用到seriesName绑定下一级，换name绑定
        type: 'map',
        map: mapTitle,
        roam: false,
        height: '100%',
        zoom: 0.75,
        z: 1,
        label: {
          //地图上的文本标签
          normal: {
            show: true,
            position: 'inside', //文本标签显示的位置
            textStyle: {
              color: '#fff', //文本颜色
              fontSize: 14,
            },
            formatter: '{b}\n{c}', //文本上显示的值  data:[{name: "地名", value: 数据}],  {b}表示label信息,{c}代表value
          },
          emphasis: {
            show: true,
            position: 'inside',
            textStyle: {
              color: '#fff',
              fontSize: 13,
            },
          },
        },
        itemStyle: {
          normal: {
            areaColor: '#5ab1ef', //地图块颜色#DCE2F1  浅蓝#2B91B7
            borderColor: '#EBEBE4', //#EBEBE4灰色
          },
          emphasis: {
            areaColor: 'rgb(254,153,78)', //s鼠标放上去，地图块高亮显示的颜色
          },
        },
        data: customerNum,
      },
      {
        name: mapTitle,
        type: 'bar',
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
            color: 'rgb(254,153,78)',
          },
        },
        data: customerNum,
      },
    ],
    // 初始动画的时长，支持回调函数，可以通过每个数据返回不同的 delay 时间实现更戏剧的初始动画效果：
    animationDuration: 1000,
    animationEasing: 'cubicOut',
    // 数据更新动画的时长。
    animationDurationUpdate: 1000,
  }

  //渲染地图
  chart.setOption(option)
  //保存当前状态数据，用于入栈出栈
  curMap = {
    mapName: mapTitle,
    mapJson: mapJson,
    colorMax: colorMax,
    sortData: sortData,
    titledata: titledata,
  }
}

/**
 * 获取城市数据
 * @param {省份} name
 * @param {省份id} id
 * @param {月份} searchtime
 * @param {地图json数据} data
 */
function getCityNumber(name, id, searchtime, data) {
  if (!id) {
    return
  }
  let postData2 = {
    parentid: 'provinceid',
    value: id,
  }
  Promise.all([ajaxRequest(getCityNumberUrl, searchtime, postData2)]).then(
    (result) => {
      Promise.all([ajaxRequest(getCityNumberUrl + id + '.json')])
        .then((resp) => {
          renderSecondMap(resp)
        })
        .catch(() => {
          // 请求后台数据或者mock数据异常，用地图自身数据渲染
          renderSecondMap(data, true)
        })
    },
    (error) => {
      console.error('请求城市数据失败', error)
      renderSecondMap(data, true)
    }
  )
  /**
   * @description: 渲染二级地图，城市
   * @param {JSONString} resp=请求后台返回的地区关联数据
   * @param {Boolean} flag=标识位，请求mock数据失败，用地图数据渲染的 true=地图数据渲染
   * @return:
   */
  function renderSecondMap(resp, flag = false) {
    let tmp = []
    if (flag) {
      resp.features.forEach((item) => {
        tmp.push({
          //需要加上cityid传递渲染，下一级地图渲染需要用到，点击的时候有判断，没有下级id直接return
          cityid: item.id,
          name: item.properties.name,
          // value: item.properties.childNum,
          // 数据
          value: 22,
        })
      })
    } else {
      curMonthResult = stringToJson(resp[0])
      if (curMonthResult.errcode == 1) {
        citySaleData = []
        for (let i = 0; i < curMonthResult.msg.length; i++) {
          tmp.push({
            cityid: curMonthResult.msg[i].cityid, //需要加上cityid传递渲染，下一级地图渲染需要用到
            name: curMonthResult.msg[i].city,
            // value: curMonthResult.msg[i].num,
            // 数据
            value: 222,
          })
        }
      }
    }
    let maxData = getMaxDataAndSort(tmp)
    renderMap(name, data, tmp, maxData.maxData)
    getRegionPreMonthRatio(maxData.maxDataId, searchtime)
  }
}


let areaList = []
let vm = new Vue({
  el: '#trend-line',
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
      this.areaList = data // vue是这样写的，内部有代理
    },
  },
  watch: {
    modalTitle(val, oldVal) {
      let $_self = this
      if (val.length > oldVal) {
        this.time++
        this.cpModalTitle.push(val)
      } else {
        // $_self._data.time--;
      }
      //TODO 取消不请求数据
      if (this.time > this.otime) {
        getRegionPreMonthRatio(val, this.searchtime)
      }
    },
  },
})


/**
 *
 * @param {未排序数据} originData
 * @return {倒序排序的数据} maxData
 */
 function getMaxDataAndSort(originData) {
  if (originData == 'undefined') {
    return
  }
  titledata = []
  sortData = []
  sortData = originData.sort(numDescSort)
  let maxData = sortData.slice(-1)[0]['value']
  let maxDataId = sortData.slice(-1)[0]['id']
  if (!maxDataId) {
    maxDataId = sortData.slice(-1)[0]['cityid'] ? sortData.slice(-1)[0]['cityid'] : sortData.slice(-1)[0]['areaid']
  }
  for (let i = 0; i < sortData.length; i++) {
    titledata.push(sortData[i].name)
  }
  areaList = [...sortData].reverse()
  vm.setAreaList(areaList)
  return {
    maxDataId,
    maxData,
  }
}