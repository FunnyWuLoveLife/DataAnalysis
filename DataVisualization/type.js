var myChart = echarts.init(document.getElementById('main'));
// 模拟数据
var sourceData = {
    "COSCO-AIR": 37,
    "中通快运": 57603,
    "中铁物流": 120579,
    "传邦物流": 22404,
    "佳吉快运": 105508,
    "佳怡物流": 42245,
    "兴铁物流": 3752,
    "卡行天下": 19409,
    "天地华宇": 183474,
    "安能物流": 322279,
    "德邦": 611742,
    "恒路物流": 9682,
    "新邦物流": 147838,
    "昊昕物流": 955,
    "百世物流": 136847,
    "盛辉物流": 16505,
    "科捷物流": 6,
    "路易通物流": 1072,
    "远成快运": 156792,
    "铭龙物流": 31896
};

option = {
    color: ['#3398DB'],
    tooltip: {
        trigger: 'axis',
        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [
        {
            type: 'value'
        }
    ],
    yAxis: [

        {
            type: 'category',
            data: Object.keys(sourceData),
            axisTick: {
                alignWithLabel: true
            }
        }
    ],
    series: [
        {
            name: '线路数量',
            type: 'bar',
            barWidth: '60%',
            data: Object.values(sourceData)
        }
    ]
};
myChart.setOption(option);