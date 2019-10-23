var app = angular.module('blockusApp', ['ngMaterial']);

app.factory('backendService', ['$http', '$interval', '$timeout', function ($http, $interval, $timeout) {
  return {
    getGame: function (gid) {
      host_url = location.host;
      var promise = $http.get(host_url + '/api/get/?gid=' + gid).then(function (response) {
        return response.data;
      });
      return promise;
    },
    init: function () {
      host_url = 'http://' + location.host;
      data = new URLSearchParams();
      data.set('name', 'Maciej');
      // data.set('auto', '');
      url = host_url + '/api/init/';
      var promise = $http.post(url, data.toString(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(function (response) {
        return response.data;
      });
      return promise;
    },
    getMoves: function (gid, pid, bid, rotates, flip) {
      host_url = 'http://' + location.host;
      data = new URLSearchParams();
      data.set('gid', gid);
      data.set('pid', pid);
      data.set('bid', bid);
      data.set('rotates', rotates);
      data.set('flip', flip)


      var promise = $http.post(host_url + '/api/get_moves/', data.toString(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(function (response) {
        return response.data;

      })

      return promise;
    },
    checkMove: function (gid, pid, bid, rotates, x, y) {
      host_url = 'http://' + location.host;
      data = new URLSearchParams();
      data.set('gid', gid);
      data.set('pid', pid);
      mov = "{'id':" + bid + ",'x':" + x + ",'y':" + y + ",'rotates':" + rotates + ",'flip':0}";

      data.set('mov', mov);


      var promise = $http.post(host_url + '/api/check_move/', data.toString(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(function (response) {
        return response.data;

      })

      return promise;
    },
    doMove: function (gid, pid, bid, rotates, flip, x, y, callback) {
      host_url = 'http://' + location.host;
      data = new URLSearchParams();
      data.set('gid', gid);
      data.set('pid', pid);
      mov = "{'id':" + bid + ",'x':" + x + ",'y':" + y + ",'rotates':" + rotates + ",'flip':" + flip + "}";

      data.set('mov', mov);


      var promise = $http.post(host_url + '/api/move/', data.toString(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(function (response) {
        return response.data;


      })

      return promise;
    },
    getStatus: function (gid, pid, callback) {
      host_url = 'http://' + location.host;
      var promise = $http.get(host_url + '/api/get/?gid=' + gid).then(function (response) {
        return response;

      })

      callback(promise);
    },
    intervalRepeat: function (fun) {
      return $interval(function () {
        fun();
        //    console.log("Sent");
      }, 1500);
    }




  };
}]);
