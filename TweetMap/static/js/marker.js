var map;
var marker;
var points = [];
var mapOptions;
var markers = [];
var markerCluster;
var bounds;
var currentKeyword = null;
var clusterOptions;
var sentiment_pic;
var tempTweets = [];
var location;
var data1 = {
    "tweetsentiment" :  [
        {lat: -31.563910, lng: 147.154312},
        {lat: -33.718234, lng: 150.363181},
        {lat: -33.727111, lng: 150.371124},
        {lat: -33.848588, lng: 151.209834},
        {lat: -33.851702, lng: 151.216968},
        {lat: -34.671264, lng: 150.863657},
        {lat: -35.304724, lng: 148.662905},
        {lat: -36.817685, lng: 175.699196},
        {lat: -36.828611, lng: 175.790222},
        {lat: -37.750000, lng: 145.116667},
        {lat: -37.759859, lng: 145.128708},
        {lat: -37.765015, lng: 145.133858},
        {lat: -37.770104, lng: 145.143299},
        {lat: -37.773700, lng: 145.145187},
        {lat: -37.774785, lng: 145.137978},
        {lat: -37.819616, lng: 144.968119},
        {lat: -38.330766, lng: 144.695692},
        {lat: -39.927193, lng: 175.053218},
        {lat: -41.330162, lng: 174.865694},
        {lat: -42.734358, lng: 147.439506},
        {lat: -42.734358, lng: 147.501315},
        {lat: -42.735258, lng: 147.438000},
        {lat: -43.999792, lng: 170.463352}
    ]
};

function initMap(dropselect) {
    var uluru = {lat: 38.68551, lng: -96.503906};
     var mapi = document.getElementById('map');
     alert(mapi);
                  map = new google.maps.Map(document.getElementById('map'), {
                  zoom: 4,
                  center: uluru
                });
                clusterOptions = {
                        imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
                };
                markerCluster = new MarkerClusterer(map, markers, clusterOptions);
    tweetSearch(dropselect);
}

function tweetSearch(dropselect) {
    alert("inside tweetsearch")
    alert(dropselect);
    drawMarkers(data1);
    // $.getJSON("keywordfilter", {keyword: dropselect})
    //     .done(function (data1) {
    //         drawMarkers(data1);
    //     })
    //     .fail(function (error) {
    //         console.log(error);
    //     });
}

function drawMarkers(tweetJSON) {
    // alert("hi");
    // alert(tweetJSON);
    tweets = tweetJSON.tweetsentiment;
    // alert(tweets);
    removeMarkers();
    $('#map').empty();
    markerCluster = null;
    $.each(tweets, function(i, tweet){
        if(tweet != undefined){
            placeMarker(tweet);
        }
    });

    if(markerCluster === null){
        markerCluster = new MarkerClusterer(map, markers, clusterOptions);
    }
    else{
        markerCluster.redraw();
    }
}


function removeMarkers(){
    for(i = 0; i < markers.length; i++){
        markers[i].setMap(null);
    }
    markers.length = 0;
    markerCluster.clearMarkers();
    deleteTempMarkers();
}


function deleteTempMarkers() {
    for (var i = 0; i < tempTweets.length; i++) {
      tempTweets[i].setMap(null);
    }
    tempTweets = [];
}

function placeMarker(tweet) {
    //alert("place");
    // alert(tweet);
    location = new google.maps.LatLng(tweet.lat, tweet.lng);
    //alert("hi");
    //alert(location);
    locationret();
    // var text = tweet.text;
    // var sentiment = tweet.sentiment;
    // var score = tweet.score;
    // if(sentiment === "positive"){
    //     sentiment_pic = positive;
    // }
    // else if(sentiment === "negative"){
    //     sentiment_pic = negative;
    // }
    // else{
    //     sentiment_pic = neutral;
    // }

    // var tweetMarker = new google.maps.Marker({
    //     position: location,
    //     map: map,
    // });
    //
    // markers.push(tweetMarker);
};

function locationret() {
    document.getElementById("loca").value = location;
}


