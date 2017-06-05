'use strict';

function Map() {
    this.zoom = 12;
    this.center = {
        lat: 48.50978134908701, lng: 32.2503662109375
    };
    this.elements = {
        map: $("#map")
    };
    this.map = new google.maps.Map(this.elements.map.get(0), {
        center: this.center,
        zoom: this.zoom,
        scrollwheel: true,
        clickableIcons: false
    });
    this.markers = [];
    this.infoWindows = [];
    this.url = {};
    this.data = window.testData;
}

Map.prototype.openInfoWindow = function (markerIndex) {
    var map = this.map;
    var markers = this.markers;

    this.infoWindows.forEach(function (infoWindow, i) {
        if (i == markerIndex) {
            infoWindow.open(map, markers[markerIndex])
        } else {
            infoWindow.close();
        }
    })
};

Map.prototype.createMarker = function (isOpenInfoWindow, taskData, latLng) {
    var map = this.map;

    if (!latLng) {
        var pos = taskData.pos.split(',');
        latLng = {
            lat: parseFloat(pos[0]),
            lng: parseFloat(pos[1])
        }
    }

    var marker = new google.maps.Marker({
        position: latLng,
        draggable: true,
        map: map
    });
    var markerIndex = this.markers.length;
    this.markers.push(marker);
    var infoWindow = this.createInfoWindow(taskData, markerIndex);

    isOpenInfoWindow && this.openInfoWindow(markerIndex);
    google.maps.event.addListener(marker, 'click', this.openInfoWindow.bind(this, markerIndex));

    return markerIndex;
};

Map.prototype.createInfoWindow = function (taskData, markerIndex) {
    var marker = this.markers[markerIndex];

    var infoWindow = new google.maps.InfoWindow({
        content: this.createForm(taskData, markerIndex)
    });

    this.infoWindows.push(infoWindow);
    return infoWindow;
};

Map.prototype.createForm = function (taskData, markerIndex) {
    var html = '';

    html += '<div class="wrap-task">'
        + '<h3><a href="/task/' + taskData.id +'">' + taskData.title + '</a></h3>'
        + printCurrentImages(taskData.images)
        + '<p>' + taskData.desc + '</p>'
        + '</div>';

    return html;

    function printCurrentImages(images) {
        var html = '';

        if (images && images.length) {
            html += '<div></div>';
            html += images.reduce(function (html, image) {
                html += '<span class="wrap-image">';
                html += '<img style="margin-right: 10px" src="' + image + '" height="100">';
                html += '</span>';
                return html;
            }, html);
        }

        return html;
    }
};

Map.prototype.showDate = function () {
    var data = this.data;
    var $this = this;
    var createMarker = this.createMarker.bind(this, false);
    data.forEach(function(task){
        var markerIndex = createMarker(task);
    });
};