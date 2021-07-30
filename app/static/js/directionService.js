var map
// var Points=[]

function initMap() {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: { lat: 35.6811673, lng: 139.7670516 },
    });
    directionsRenderer.setMap(map);
    directionsRenderer.setPanel(document.getElementById("sidebar"));
        
    // ルート地点の変数−−−−−−−−−−−−−
    var Points = [
        // { // 松山空港から目的地
        //     "start" :  "東京駅",
        //     "end" : "新宿駅",
        //     "color" : "#45A1CF"
        // },
        // { // JR松山駅から目的地
        //     "start" :  "新宿駅",
        //     "end" : "渋谷駅",
        //     "color" : "#DA6272"
        // }
    ]

    
    
    // ルートの表示−−−−−−−−−−−−−
    const onChangeHandler = function () {
        // htmlで受け取った出発地と目的地を登録
        var Points = []
        Points.push({
            "start" :  document.getElementById("start").value,
            "end" : document.getElementById("end").value,
            "color" : "#45A1CF"
        })

        // 2つ以上ルートがあったら同時に表示する
        if (Points.length > 1) {
            for(var i in Points){
                fCalcRoute(Points[i]['start'], Points[i]['end'], Points[i]['color']);
            }
        }
        console.log(Points[0])
        calculateAndDisplayRoute(directionsService, directionsRenderer, Points[0]['start'], Points[0]['end']);
    };
    

    document.getElementById("search").addEventListener("click", onChangeHandler);
}

function calculateAndDisplayRoute(directionsService, directionsRenderer, start, end) {
    const travelMode = document.getElementById("mode").value
    directionsService
        .route({
        origin: {
            query: start,
        },
        destination: {
            query: end,
        },
        travelMode: google.maps.TravelMode[travelMode],
        })
        .then((response) => {
        directionsRenderer.setDirections(response);
        })
        .catch((e) => window.alert("Directions request failed due to " + status));
}

//ルートを表示する関数
function fCalcRoute(start, end, color) {
    // ルート表示 設定
    const rendererOptions = {
        draggable: true, //ドラッグ操作の有効/無効を設定する
        preserveViewport: true //境界のボックスにセンタリングされズームするかどうか（地図の中心とズームの設定がないと、ビューポートは変更されない）
    };

    var directionsDisplay =  new google.maps.DirectionsRenderer(rendererOptions);
    directionsDisplay.setOptions({
        polylineOptions: { //ルートの形状
            strokeColor: color, //色
            strokeOpacity: 0.8, //透過
            strokeWeight: 6 //線幅
        }, 
        suppressMarkers: false, //true:マーカー非表示
        suppressInfoWindows: true //true:ルート線非表示
    });

    var directionsService =  new google.maps.DirectionsService();
    var request = {
        origin: start, //出発場所
        destination: end, //到着場所
        travelMode: google.maps.DirectionsTravelMode.DRIVING, //交通手段を指定する（DRIVING:運転ルート、WALKING:徒歩ルート、BICYLING:自転車ルート）
        unitSystem: google.maps.DirectionsUnitSystem.METRIC, //単位km表示
        optimizeWaypoints: true, //最適化された最短距離にする
        avoidHighways: false, //高速道路（false:使用しない）
        avoidTolls: false //有料区間（false:使用しない）
    };
    directionsService.route(request,
        function(response,status){
            if (status == google.maps.DirectionsStatus.OK){
                directionsDisplay.setDirections(response);
            }
        }
    );
    directionsDisplay.setMap(map);
}