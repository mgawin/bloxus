var app = angular.module('blockusApp', [])
  .controller('GameController', ['$scope', 'backendService', function ($scope, backendService) {

    backendService.init().then(function (data) {
      backendService.intervalRepeat(function () {
        return backendService.getStatus($scope.gameId, $scope.playerId, $scope.manageStatus)
      });
      $scope.gameId = data.gid;
      $scope.state = '0';
      $scope.playerId = data.player.pid;
      $scope.blocks = data.player.bloxs;
      switch (data.status) {
        case 1:
          $scope.blocked = true;
          console.log("waiting");
          break;
        case 2:
          //         console.log("Player A move");
          console.log($scope.playerId)
          if ($scope.playerId == 1) {

            $scope.blocked = false;
            //  $scope.drawMove(successResponse.data.last, '#B164DE');

          }
          else $scope.blocked = true;

          break;
        case '3':
          //          console.log("Player B move");
          if ($scope.playerId == 2) {

            $scope.blocked = false;
            //  $scope.drawMove(successResponse.data.last, 'orange');

          }
          else $scope.blocked = true;


          break;

      }


      $scope.positionBlocks()


    });

    $scope.$on('$destroy', function () {
      intervalPinging.stop();
    });

    $scope.blocks = [];
    $scope.allowed_moves = [];
    $scope.selected = null;
    var canvas = document.getElementById('c1');

    paper.setup(canvas);

    var grid = 24;
    var shiftx = 96;
    var shifty = 48;

    for (var i = 0; i < 15; i++) {

      paper.Path.Line({
        from: [shiftx + i * grid, shifty],
        to: [shiftx + i * grid, shifty + 14 * grid],
        strokeColor: '#ccc'
      });


      paper.Path.Line({
        from: [shiftx, shifty + i * grid],
        to: [shiftx + 14 * grid, shifty + i * grid],
        strokeColor: '#ccc'
      });
    }

    var rect = paper.Path.Rectangle({
      point: [shiftx + 9 * grid, shifty + 9 * grid],
      size: [grid, grid],
      fillColor: '#ccc',

    });

    rect.fillColor.alpha = 0.5;

    rect = paper.Path.Rectangle({
      point: [shiftx + 4 * grid, shifty + 4 * grid],
      size: [grid, grid],
      fillColor: '#ccc',

    });

    rect.fillColor.alpha = 0.5;



    $scope.manageStatus = function (promise) {

      promise.then(function (successResponse) {
        //    console.log("Got game status code: " + successResponse.data.status);
        if ($scope.state != successResponse.data.status) {
          switch (successResponse.data.status) {
            case 1:
              $scope.blocked = true;
              console.log("waiting");
              break;
            case 2:
              //         console.log("Player A move");
              console.log($scope.playerId)
              if ($scope.playerId == 1) {

                $scope.blocked = false;
                //  $scope.drawMove(successResponse.data.last, '#B164DE');

              }
              else $scope.blocked = true;

              break;
            case '3':
              //          console.log("Player B move");
              if ($scope.playerId == 2) {

                $scope.blocked = false;
                //  $scope.drawMove(successResponse.data.last, 'orange');

              }
              else $scope.blocked = true;


              break;

          }

          $scope.state = successResponse.data.code;

        }



      },
        function (errorResponse) {
          console.log("Error: " + errorResponse.status + " " + errorResponse.statusText);
        })

    }

    $scope.drawMove = function (move, color) {
      var group = new paper.Group([]);
      y = move.x
      x = move.y
      for (var j = 0; j < move.blox.shp.length; j++) {

        for (var i = 0; i < move.blox.shp[0].length; i++) {

          if (move.blox.shp[j][i] > 0) {


            var rect = paper.Path.Rectangle({
              point: [shiftx + x * grid + grid * i, shifty + y * grid + grid * j],
              size: [grid, grid],
              fillColor: color,
              strokeWidth: 2,
              strokeColor: color

            });


            rect.fillColor.alpha = 0.75;
            group.addChild(rect);
          }
        }
      }


      group.opacity = 0.75;
      group.angle = 0;

      paper.view.draw();

    }






    $scope.doMove = function (x, y) {
      if ($scope.blocked) return;
      backendService.doMove($scope.gameId, $scope.playerId, $scope.selected.bid, $scope.selected.orientation_id, $scope.selected.flipped, x, y).then(function (data) {

        $scope.drawMove(data.last, '#B164DE');

      })
      console.log("moved")

    }

    $scope.move_allowed__ = function (x, y) {
      backendService.checkMove($scope.gameId, $scope.playerId, $scope.selected.bid, $scope.selected.orientation_id, x, y).then(function (data) {
        $scope.allowed_move = data.allowed;

      })

    }

    $scope.getMoves = function () {

      $scope.allowed_moves = [];
      backendService.getMoves($scope.gameId, $scope.playerId, $scope.selected.bid, $scope.selected.orientation_id, $scope.selected.flipped).then(function (data) {
        $scope.allowed_moves = data.moves;

      })


    }

    function sleep(time) {
      return new Promise((resolve) => setTimeout(resolve, time));
    }

    move_allowed = function (i, j) {

      var res = 0;
      $scope.allowed_moves.forEach(function (e) {

        n = parseInt(e[0]);
        m = parseInt(e[1]);
        if ((n == i) && (m == j)) res++;


      })
      if (res > 0) return true;
      else return false;

    }


    calculate_coords = function (val, horizontal) {

      if (horizontal) {
        return parseInt(Math.round((val - shiftx) / grid));


      }
      else {
        return parseInt(Math.round((val - shifty) / grid));

      }


    }


    $scope.positionBlocks = function () {
      var y = grid;
      var x = 450;
      var color;
      if ($scope.playerId == 1) color = 'orange';
      else color = '#B164DE';

      $scope.blocks.forEach(function (element, index) {
        x = x + 120;
        if (x > 450 + 600) {
          x = 450 + 120;
          y = y + 80;
        }



        var group = new paper.Group([]);
        group.bid = index;

        group.orientation_id = 0;
        group.flipped = 0;
        group.locked = false;


        for (var j = 0; j < element.shp.length; j++) {

          for (var i = 0; i < element.shp[0].length; i++) {

            if (element.shp[j][i] > 0) {



              var rect = paper.Path.Rectangle({
                point: [grid * i, grid * j],
                size: [grid, grid],
                fillColor: color,
                strokeWidth: 2,
                strokeColor: color

              });


              rect.fillColor.alpha = 0.75;
              group.opacity = 0.75;
              group.angle = 0;
              group.addChild(rect);

            }
          }

        };



        group.onMouseDown = function () {
          console.log("down");
          if (this.locked || $scope.blocked) return;
          if (event.button == 2) {
            console.log("I'm flipped");
            if (($scope.selected != null) && ($scope.selected.bid != this.bid)) {
              $scope.selected.opacity = 0.8;

            }
            $scope.selected = this;
            if (this.flipped == 0) this.flipped = 1; else this.flipped = 0;
            $scope.getMoves();
            console.log("I'm selected");
            this.scale(-1, 1);
            this.opacity = 1;
            this.bringToFront();

            return;
          }
          console.log($scope.selected)
          if (($scope.selected != null) && ($scope.selected.bid != this.bid)) {
            $scope.selected.opacity = 0.8;

          }
          if (($scope.selected == null) || ($scope.selected.bid != this.bid)) {
            $scope.selected = this;
            $scope.getMoves();
            console.log("I'm selected");
            this.opacity = 1;
            this.bringToFront();
          }
          if (event.detail == 1) {

          };

          // if (event.detail == 2) {
          //   this.orientation_id += 1;
          //   if (this.orientation_id >= 4) this.orientation_id = this.orientation_id - 4;

          //   $scope.getMoves();

          //   this.rotate(-90, this.center);
          //   console.log("I'm rotated");
          // }

        };

        group.onDoubleClick = function () {

          this.orientation_id += 1;
          if (this.orientation_id >= 4) this.orientation_id = this.orientation_id - 4;

          $scope.getMoves();

          this.rotate(-90, this.center);
          console.log("I'm rotated");

        }


        group.onMouseDrag = function (event) {
          if (this.locked || $scope.blocked) return;
          this.position = event.point;
          if ((this.bounds.left <= 435) && (this.bounds.top <= 370) && (this.bounds.left > 86) && (this.bounds.top > 32)) {

            var offsetx = Math.round(this.bounds.size.width / 2);
            var offsety = Math.round(this.bounds.size.height / 2);

            this.position = new paper.Point(offsetx + (Math.round((this.position.x - offsetx) / grid) * grid),
              offsety + (Math.round((this.position.y - offsety) / grid) * grid));
          };
          //   console.log("I'm dragged");
        };


        group.onMouseUp = function () {
          console.log("up");
          if (this.locked) return;
          if ($scope.blocked) {

            console.log('blocked');
            this.position = this.initialPosition;
            return;

          }
          var y = calculate_coords(this.bounds.left, true);
          var x = calculate_coords(this.bounds.top, false);
          console.log(y);
          if (y > 14) {
            this.position = this.initialPosition;
            return;
          }
          this.opacity = 0.75;

          if (this.bid != $scope.selected.bid) return;
          console.log("I'm dropped");
          console.log(x, y);
          if (move_allowed(x, y)) {
            this.locked = true;
            console.log('allowed')

            $scope.doMove(x, y)
            $scope.blocked = true;


          }
          else {

            console.log('not allowed')
            this.position = this.initialPosition;

          };
        }
        group.position = new paper.Point(x, y);
        group.initialPosition = group.position;


      });

      paper.view.draw();

    };

  }]);