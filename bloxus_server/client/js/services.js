app.factory('backendService', function($http, $interval, $timeout) {
  var backendService = {
    getGame: function(gid) {
      var promise = $http.get('https://golang-mgawin.c9.io/status?id=' + gid).then(function(response) {
        return response.data;
      });
      return promise;
    },
    init: function() {

      var promise = $http.get('https://golang-mgawin.c9.io/_ah/api/blockus/v1/new').then(function(response) {
        return response.data;
      });
      return promise;
    },
    getMoves: function(gid, pid, bid, rotates) {
      var promise = $http.get('https://golang-mgawin.c9.io/_ah/api/blockus/v1/moves?gid=' + gid + '&pid=' + pid + '&bid=' + bid + '&rotates=' + rotates).then(function(response) {
        return response.data;

      })

      return promise;
    },
    doMove: function(gid, pid, bid, rotates, x, y) {
      var promise = $http.post('https://golang-mgawin.c9.io/_ah/api/blockus/v1/move?gid=' + gid + '&pid=' + pid + '&bid=' + bid + '&rotates=' + rotates + '&x=' + x + '&y=' + y).then(function(response) {
        return response.data;

      })

      return promise;
    },
    getStatus: function(gid, pid, callback) {
      var promise = $http.get('https://golang-mgawin.c9.io/_ah/api/blockus/v1/status?gid=' + gid + '&pid=' + pid).then(function(response) {
        return response;
        
      })

      callback(promise);
    },
    intervalRepeat: function(fun) {
      return $interval(function() {
        fun();
    //    console.log("Sent");
      }, 1500);
    }




  };
  return backendService;
});
