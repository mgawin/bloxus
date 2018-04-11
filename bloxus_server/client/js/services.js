app.factory('backendService', function ($http, $interval, $timeout) {
  var backendService = {
    getGame: function (gid) {

      var promise = $http.get('https://127.0.0.1/api/get/?gid=' + gid).then(function (response) {
        return response.data;
      });
      return promise;
    },
    init: function () {

      data = new URLSearchParams();
      data.set('name', 'Maciej');
      data.set('auto', '');
      var promise = $http.post('http://127.0.0.1:8000/api/init/', data.toString(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(function (response) {
        return response.data;
      });
      return promise;
    },
    getMoves: function (gid, pid, bid, rotates, flip) {
      data = new URLSearchParams();
      data.set('gid', gid);
      data.set('pid', pid);
      data.set('bid', bid);
      data.set('rotates', rotates);
      data.set('flip', flip)


      var promise = $http.post('http://127.0.0.1:8000/api/get_moves/', data.toString(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(function (response) {
        return response.data;

      })

      return promise;
    },
    checkMove: function (gid, pid, bid, rotates, x, y) {
      data = new URLSearchParams();
      data.set('gid', gid);
      data.set('pid', pid);
      mov = "{'id':" + bid + ",'x':" + x + ",'y':" + y + ",'rotates':" + rotates + ",'flip':0}";

      data.set('mov', mov);


      var promise = $http.post('http://127.0.0.1:8000/api/check_move/', data.toString(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(function (response) {
        return response.data;

      })

      return promise;
    },
    doMove: function (gid, pid, bid, rotates, flip, x, y, callback) {
      data = new URLSearchParams();
      data.set('gid', gid);
      data.set('pid', pid);
      mov = "{'id':" + bid + ",'x':" + x + ",'y':" + y + ",'rotates':" + rotates + ",'flip':" + flip + "}";

      data.set('mov', mov);


      var promise = $http.post('http://127.0.0.1:8000/api/move/', data.toString(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(function (response) {
        return response.data;


      })

      return promise;
    },
    getStatus: function (gid, pid, callback) {
      var promise = $http.get('http://127.0.0.1:8000/api/get/?gid=' + gid).then(function (response) {
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
  return backendService;
});
