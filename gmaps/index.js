/**
 * Created by Maddy on 6/30/17.
 */
function initMap() {
    let map;
    // Constructor creates a new map - only center and zoom are required.
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.7413549, lng: -73.9980244},
        zoom: 13
    });
    mark = new google.maps.Marker(
        map: map,
        position: {lat: 40.7163, lng: 74.0086},
        title: 'tribeca'
    )
}