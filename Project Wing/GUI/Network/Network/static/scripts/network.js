var nodes = null, network = null, map = null, marker = null;
var bounds = null, position = null;

function distance(fromLat, fromLng, toLat, toLng) {
    //https://en.wikipedia.org/wiki/Haversine_formula
    var p = 0.017453292519943295;    // Math.PI / 180
    var c = Math.cos;
    return (12742 * Math.asin(Math.sqrt(
        0.5 - c((toLat - fromLat) * p) / 2 +
        c(fromLat * p) * c(toLat * p) *
        (1 - c((toLng - fromLng) * p)) / 2)));
}

function initMap() {
    var colors = ["blue", "green", "yellow", "orange", "red"];
    $(function () {
        map = new google.maps.Map(document.getElementById("map"), {
            zoom: 6,
            center: new google.maps.LatLng(-28.741943, 24.771944),
            mapTypeId: 'terrain'
        });
    });

    $(function () {
        $.getJSON("/static/data/Nodes.json", function (data) {
            nodes = data;
            console.log(nodes);
        }).done(function () {
            bounds = new google.maps.LatLngBounds();
            $.each(nodes, function (key, node) {
                var color = colors[Math.abs(node.Type)];
                if (nodes[key].Type == -1) {
                    color = colors[4];
                }
                marker = $(function () {
                    position = new google.maps.LatLng(node.Position[0], node.Position[1]);
                    return new google.maps.Marker({
                        title: "#" + key + " - " + nodes[key].Name,
                        icon: new google.maps.MarkerImage("http://maps.google.com/mapfiles/ms/icons/"+ color + "-dot.png"),
                        position: position,
                        map: map
                    });
                })
                $(function () {
                    bounds.extend(position);
                });
            });
            //console.log(bounds);            
            //map.fitBounds(bounds); //Auto-Zoom
            //map.panToBounds(bounds); //Auto-center
        });

    });

    $(function(){
        $.getJSON("/static/data/Network.json", function (data) {
            network = data;
            console.log(network);
        }).done(function () {
            $.each(network, function (key, head) {
                var color = colors[Math.abs(head.Type)];
                var distances = [];
                if (head.Type == -1) {
                    color = colors[4];
                }
                $.each(head.MEMBERS, function (i, node) {
                    console.log(node);
                    distances.push(distance(head.Position[0], head.Position[1], nodes[node].Position[0], nodes[node].Position[1]));
                    var line = $(function () {
                        return new google.maps.Polygon({
                            path: [new google.maps.LatLng(nodes[node].Position[0], nodes[node].Position[1]),
                                new google.maps.LatLng(head.Position[0], head.Position[1])],
                            strokeColor: color,
                            strokeOpacity: 1.0,
                            strokeWeight: 1,
                            map: map
                        });
                    });
                });
                var circle = $(function () {
                    return new google.maps.Circle({
                        strokeColor: color,
                        strokeOpacity: 0.35,
                        strokeWeight: 1,
                        fillColor: color,
                        fillOpacity: 0.15,
                        map: map,
                        center: new google.maps.LatLng(head.Position[0], head.Position[1]),
                        radius: Math.abs(Math.max(distances) *0)
                    });
                });
            });
        });
    });
}


