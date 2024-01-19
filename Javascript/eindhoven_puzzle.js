let map;
let data;
let layers = []
let geojsonData = {
    "type": "FeatureCollection",
    "features": []
};

function setup() {
    noCanvas();
    loadStrings('./data/stijn_eindhoven_wijken.csv', csvLoaded);
    initMap();
}

function csvLoaded(data) {
    data.forEach((row, index) => {
        if(index === 0 || index === data.length - 1){
            return
        }
        const data_csv = row.split(';');
        const corrected_json = JSON.stringify(data_csv[7])
            .replace(/""/g, '"')
            .replace(/\\/g, '')
            .replace(/""/g, '"')
            .slice(1, -1);

        corrected_json_ = corrected_json.replace("}", ', \"centerpoint\": [' + data_csv[8] + ']}')
        const geojson_Data = JSON.parse(corrected_json_);
        geojsonData.features = geojsonData.features.concat(geojson_Data)
    })
    drawPolygons()
    shufflePieces()
}

function drawPolygons() {
    geojsonData.features.forEach(feature => {
        var layer = L.geoJSON([feature],{
            opacity: 1,
            weight: 5,
            fillOpacity: 0.8
            }).addTo(map);

        layer.eachLayer(function(l){
                if (l.dragging) {
                    l.dragging.enable();
                }

                l.on('drag', function(e){
                    console.log("dragging....")
                })

                l.on('dragend', function(e){
                    console.log(l.getCenter())
                    console.log(l.feature.geometry.centerpoint)
                    // console.log(l.getCenter().lat - l.feature.geometry.centerpoint[0])
                    // console.log(l.getCenter().lng - l.feature.geometry.centerpoint[1])
                    let distance = Math.sqrt((l.getCenter().lat - l.feature.geometry.centerpoint[0]) *
                        (l.getCenter().lat - l.feature.geometry.centerpoint[0]) +
                        (l.getCenter().lng - l.feature.geometry.centerpoint[1]) *
                        (l.getCenter().lng - l.feature.geometry.centerpoint[1]))
                    console.log(distance)
                    if(distance <= 0.002){
                        console.log("Correct placement")
                        placeCorrectPolygon(l)
                        checkProgress(layer)
                    }
                })
            layers.push(layer)
            }
        )
    });
}

function checkProgress(layer){
    layers.pop(layer)

    if(layers.length === 0){
        Swal.fire({
            title: "Puzzle Completed",
            text: "You have completed the puzzle",
            icon: "success"
        });
    }
}

function placeCorrectPolygon(polygon){
    console.log(polygon.feature.geometry)

    map.removeLayer(polygon)

    var layer = L.geoJSON([polygon.feature.geometry],{
        opacity: 1,
        weight: 5,
        fillOpacity: 0.8,
        color: 'green'
    }).addTo(map);
}

function shufflePieces() {
    let bounds = map.getBounds();
    let minX = bounds.getWest();
    let maxX = bounds.getEast();
    let minY = bounds.getSouth();
    let maxY = bounds.getNorth();

    console.log(bounds)

    let noGoCenter = map.getCenter();
    let noGoRadiusLat = 0.1;
    let noGoRadiusLng = 0.1;

    console.log(noGoCenter)

    layers.forEach(layer => {
        layer.eachLayer(function(l) {
            let newCenter;
            do {
                let randLat = minY + (Math.random() * (maxY - minY));
                let randLng = minX + (Math.random() * (maxX - minX));
                newCenter = L.latLng(randLat, randLng);
            } while (isInNoGoZone(newCenter, noGoCenter, noGoRadiusLat, noGoRadiusLng));

            let oldCenter = l.getBounds().getCenter();
            let latOffset = newCenter.lat - oldCenter.lat;
            let lngOffset = newCenter.lng - oldCenter.lng;

            let newLatLngs = l.getLatLngs();
            adjustLatLngs(newLatLngs, latOffset, lngOffset);
            l.setLatLngs(newLatLngs);
        });
    });
}

function isInNoGoZone(center, noGoCenter, latRadius, lngRadius) {
    return center.lat < noGoCenter.lat + latRadius && center.lat > noGoCenter.lat - latRadius &&
        center.lng < noGoCenter.lng + lngRadius && center.lng > noGoCenter.lng - lngRadius;
}

function adjustLatLngs(latlngs, latOffset, lngOffset) {
    if (Array.isArray(latlngs[0])) {
        latlngs.forEach(part => adjustLatLngs(part, latOffset, lngOffset));
    } else {
        latlngs.forEach((latlng, index, arr) => {
            arr[index] = L.latLng(latlng.lat + latOffset, latlng.lng + lngOffset);
        });
    }
}

function initMap() {
    map = L.map('map', {
        center: [51.45383, 5.4535],
        zoom: 13,
        maxZoom: 14,
        minZoom: 12,
        zoomControl: true,
        scrollWheelZoom: false,
        dragging: false,
        doubleClickZoom: false
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    setTimeout(function() {
        map.invalidateSize();
    }, 100);
}