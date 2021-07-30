// 最初に全画面に地図を表示
function initMap() {
    // 途中地点のピン用
    const markerArray = [];
    const directionsService = new google.maps.DirectionsService();
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: { lat: 35.6811673, lng: 139.7670516 },
    });
    // directionsRenderer.setMap(map);
    const directionsRenderer = new google.maps.DirectionsRenderer({
        draggable: true,
        map,
        panel: document.getElementById("sidebar"),
    });


    const stepDisplay = new google.maps.InfoWindow();

    const onChangeHandler = function () {
        calculateAndDisplayRoute(
            directionsRenderer,
            directionsService,
            markerArray,
            stepDisplay,
            map
        );
    };

    document.getElementById("search").addEventListener("click", onChangeHandler);
}

// 出発地、目的地、移動手段からルート検索
function calculateAndDisplayRoute(
    directionsRenderer,
    directionsService,
    markerArray,
    stepDisplay,
    map
){
    const startPoint = document.getElementById("start").value;
    const endPoint = document.getElementById("end").value;
    const selectedMode = document.getElementById("mode").value;

    // First, remove any existing markers from the map.
    for (let i = 0; i < markerArray.length; i++) {
        markerArray[i].setMap(null);
    }

    directionsService
    .route({
        origin: startPoint,
        destination: endPoint,
        travelMode: google.maps.TravelMode[selectedMode],
    })
    .then((result) => {
    // Route the directions and pass the response to a function to create
    // markers for each step.
        console.log(result)
        document.getElementById("warnings-panel").innerHTML =
            "<b>" + result.routes[0].warnings + "</b>";
        directionsRenderer.setDirections(result);
        showSteps(result, markerArray, stepDisplay, map);
    })
    .catch((e) => {
        window.alert("Directions request failed due to " + e);
    });
}

function showSteps(directionResult, markerArray, stepDisplay, map) {
    // For each step, place a marker, and add the text to the marker's infowindow.
    // Also attach the marker to an array so we can keep track of it and remove it
    // when calculating new routes.
    const myRoute = directionResult.routes[0].legs[0];
    for (let i = 0; i < directionResult.routes.length; i++) {
        console.log(directionResult.routes[i])
        
    }

    for (let i = 0; i < myRoute.steps.length; i++) {
        const marker = (markerArray[i] =
            markerArray[i] || new google.maps.Marker());
            marker.setMap(map);
            marker.setPosition(myRoute.steps[i].start_location);
            attachInstructionText(
                stepDisplay,
                marker,
            myRoute.steps[i].instructions,
            map
        );
    }
}

  function attachInstructionText(stepDisplay, marker, text, map) {
  google.maps.event.addListener(marker, "click", () => {
      // Open an info window when the marker is clicked on, containing the text
      // of the step.
      stepDisplay.setContent(text);
      stepDisplay.open(map, marker);
  });
  }
