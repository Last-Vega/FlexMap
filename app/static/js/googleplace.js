function autoComplete() {
    var LatLngFrom = new google.maps.LatLng(35.692195,139.7576653);
    var LatLngTo   = new google.maps.LatLng(35.696157,139.7525771);
    //検索領域
    var bounds = new google.maps.LatLngBounds(LatLngFrom, LatLngTo);
    //検索
    var department = document.getElementById('id_department');
    var destination = document.getElementById('id_destination');
    //検索オプション
    var options = {
        bounds: bounds,
        // types: ['establishment'],
        componentRestrictions: {country: 'jp'}
    };
    //オートコンプリート
    autocomplete_department = new google.maps.places.Autocomplete(department,options);
    autocomplete_destination = new google.maps.places.Autocomplete(destination,options);
}
window.onload = autoComplete;