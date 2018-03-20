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
      console.log(data)
      var promise = $http.post('http://127.0.0.1:8000/api/init/', data.toString(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(function (response) {
        return response.data;
      });
      return promise;
    },
    checkMove: function (gid, pid, bid, rotates, x, y) {
      data = new URLSearchParams();
      data.set('gid', gid);
      data.set('pid', pid);
      mov = "{'id':" + bid + ",'x':" + x + ",'y':" + y + ",'rotates':" + rotates + ",'flip':'false'}";

      data.set('mov', mov);


      var promise = $http.post('http://127.0.0.1:8000/api/check_move/', data.toString(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(function (response) {
        return response.data;

      })

      return promise;
    },
    doMove: function (gid, pid, bid, rotates, x, y) {
      var promise = $http.post('https://golang-mgawin.c9.io/_ah/api/blockus/v1/move?gid=' + gid + '&pid=' + pid + '&bid=' + bid + '&rotates=' + rotates + '&x=' + x + '&y=' + y).then(function (response) {
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
