var map, moveable_gt;
var width = 400;
var height = 200;
var data;
var geotags=[];

function mover(){
        var Height=document.body.scrollHeight;
        var foot=document.getElementById("Footer");
        foot.style.top=(Height-130)+"px"; }
var butn=document.getElementById("Load");
butn.addEventListener('click',mover);

function create_geotag(coords) {
    var geotag = new ymaps.Placemark(coords,
            {
                moveable: false,
                hintContent: 'Выберите геотег для видео'
            },
            {
                draggable: true,
                preset: 'islands#blueIcon'
            }
    );

    map.geoObjects.add(geotag);
    geotags.push(geotag);

    geotag.events.add('click', function(e) {
        var gt = e.get('target');
        if (typeof moveable_gt !== 'undefined' && moveable_gt !== null) {
            moveable_gt.properties.set('moveable', false);
            moveable_gt.options.set('preset', 'islands#blueIcon');
        }

        if (gt == moveable_gt) {
            moveable_gt = null;
        }
        else {
            moveable_gt = gt;
            gt.properties.set('moveable', true);
            gt.options.set('preset', 'islands#redIcon')
        }
    });

    geotag.events.add('contextmenu', function(e) {
        gt = e.get('target');

        var index = geotags.indexOf(gt);
        geotags.splice(index, 1);

        map.geoObjects.remove(gt);
        gt.devare;

        e.preventDefault();

    });
    }


function init () {
    map = new ymaps.Map("map", {
            center: [55, 47],
            zoom: 6,
            controls: [],
        },
        {
            autoFitToViewport: 'always'
        }
    );

    map.events.add('click', function(e) {
        if (moveable_gt) {
            moveable_gt.geometry.setCoordinates(e.get('coords'));
        }
    });

    map.events.add('dblclick', function(e) {
        create_geotag(e.get('coords'));
        e.preventDefault();
    });
}


function show_map() {
    $('#geotag_is_needed').addClass('btn_pushed');
    $('#map').css('width', width+'px');
    $('#map').css('height', height+'px');
    $('#map-info').show();
    map.container.fitToViewport();
}

function hide_map() {
    $('#map').css('width', '0px');
    $('#map').css('height', '0px');
    $('#geotag_is_needed').removeClass('btn_pushed');
    $('#map-info').hide();
    map.container.fitToViewport();
}

ymaps.ready(function () {
    data = JSON.parse($('#geotag_data').val())
    init();

    if (data['needed']) {
        for (var i in data['coords']) {
            create_geotag(data['coords'][i]);
        }
        show_map();
    }

    $('#geotag_is_needed').click(function(e) {
        if (data['needed']) {
            data['needed'] = false;
            hide_map();

        }
        else {
            data['needed'] = true;
            show_map();
        }
    });
    
    $('#submit').click(function() {
        if (data['needed'] && typeof geotags[0] === 'object') {

            data['coords'] = [];
            for (var i in geotags) {
                data['coords'].push(geotags[i].geometry.getCoordinates());
            }

        }
        $('#geotag_data').val(JSON.stringify(data));
    });
});
