/**
 * 将原始数据转换为城市列表
 * @param data
 * @returns {{}}
 */
function convertData(data) {
    var resultData = {};
    for (var key in data) {
        var tempObj = data[key];
        if (tempObj["depart"] in resultData) {
            resultData[tempObj["depart"]].push(tempObj["arrive"]);
        } else {
            resultData[tempObj["depart"]] = [];
            resultData[tempObj["depart"]].push(tempObj["arrive"]);
        }
    }
    return resultData;
}

/**
 * 获取城市列表
 * @param data 原始数据
 * @returns {{}}城市列表
 */
function getCityList(data) {
    var resultData = {};

    for (var key in data) {
        var tempObj = data[key];
        var depart = trimStr(tempObj["depart"]);
        var arrive = trimStr(tempObj["arrive"]);
        if (depart in resultData) {
        }
        else {
            resultData[depart] = [];
        }
        if (arrive in resultData) {
        } else {
            resultData[arrive] = [];
        }
    }
    return resultData;
}

function trimStr(str) {
    return str.replace(/(^\s*)|(\s*$)/g, "");
}

/**
 * 通过城市列表列表对象获取列表中每个城市的坐标
 * @param cityList 城市列表对象 eg:{"七台河市":{"lnt":null,"lat":null},"成都市":{"lnt":null,"lat":null}}
 */
function getGeoCoord(cityList) {

    var resultData = cityList;
    cityList = {"成都市": "", "重庆市": "", "深圳市": ""}
    for (var key in cityList) {
        resultData[key] = {};
        $.ajax({
            url: 'http://api.map.baidu.com/geocoder/v2/',
            method: 'GET',
            dataType: "jsonp",
            jsonpCallback: "cb", //这里的参数值和下面请求中的callback参数值必须一样，这是为了解决跨域问题，返回的是一个jsonp
            data: {
                address: key,
                output: "json",
                ak: "smMpXU250sXmmw42P3s7wsRH0vzpdgjo",
                callback: "cb"
            },
            success: function cb(res) {
                // 在这里坐相应的数据处理，res是api返回的数据
                // eg:{"status": 0,"result": {"location": {"lng": 117.01799673877318,"lat": 25.07868543351518},"precise": 0,"confidence": 10,"level": "城市"}}
                // resultData[key] = res.result.location;
                var temp = {};
                temp[key] = res.result.location;

                var dom = document.createElement('p');
                dom.innerHTML = JSON.stringify(temp);
                document.getElementById('main').appendChild(dom);

                // var div = document.getElementById("main");
                // console.log(div.innerHTML)
                // div.innerHTML = div.innerHTML + JSON.stringify(temp) + ',<br/>'
            }
        });
    }
}