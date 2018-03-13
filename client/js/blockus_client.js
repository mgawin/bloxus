var app = angular.module('blockusApp', [])
  .controller('GameController', ['$scope', 'backendService', function($scope, backendService) {

    backendService.init().then(function(data) {
      $scope.gameId = data.gid;
      $scope.state = '0'
      $scope.blocked = true;
      $scope.playerId = data.pid;
      if ($scope.playerId == 1) $scope.blocks = data.game.PlayerA.Blocks;
      else $scope.blocks = data.game.PlayerB.Blocks;

      $scope.positionBlocks();
      backendService.intervalRepeat(function() {
        return backendService.getStatus($scope.gameId, $scope.playerId, $scope.manageStatus)
      });

    });

    $scope.$on('$destroy', function() {
      intervalPinging.stop();
    });

    $scope.blocks = [];
    $scope.allowed_moves = [];
    var selected = null;
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
      point: [shiftx + 4 * grid, shifty + 9 * grid],
      size: [grid, grid],
      fillColor: '#ccc',

    });

    rect.fillColor.alpha = 0.5;

    rect = paper.Path.Rectangle({
      point: [shiftx + 9 * grid, shifty + 4 * grid],
      size: [grid, grid],
      fillColor: '#ccc',

    });

    rect.fillColor.alpha = 0.5;



    $scope.manageStatus = function(promise) {

      promise.then(function(successResponse) {
          console.log("Got game status code: " + successResponse.data.code);
          if ($scope.state != successResponse.data.code) {
            switch (successResponse.data.code) {
              case '1':
                $scope.blocked = true;
                console.log("waiting");
                break;
              case '2':
                console.log("Player A move");
                if ($scope.playerId == 1) {

                  $scope.blocked = false;
                  if (successResponse.data.lastmove) $scope.drawMove(successResponse.data.lastmove, '#B164DE');

                }
                else $scope.blocked = true;

                break;
              case '3':
                console.log("Player B move");
                if ($scope.playerId == 2) {

                  $scope.blocked = false;
                  if (successResponse.data.lastmove) $scope.drawMove(successResponse.data.lastmove, 'orange');

                }
                else $scope.blocked = true;


                break;

            }

            $scope.state = successResponse.data.code;

          }



        },
        function(errorResponse) {
          console.log("Error: " + errorResponse.status + " " + errorResponse.statusText);
        })

    }

    $scope.drawMove = function(move, color) {

      var group = new paper.Group([]);

      move.forEach(function(e) {

        x = parseInt(e[0]);
        y = parseInt(e[1]);




        var rect = paper.Path.Rectangle({
          point: [shiftx + x * grid, shifty + y * grid],
          size: [grid, grid],
          fillColor: color,
          strokeWidth: 2,
          strokeColor: color

        });


        rect.fillColor.alpha = 0.75;
        group.addChild(rect);



      })
      group.opacity = 0.75;
      group.angle = 0;

      paper.view.draw();

    }


    $scope.getMoves = function() {

      $scope.allowed_moves = [];
      backendService.getMoves($scope.gameId, $scope.playerId, selected.bid, selected.orientation_id).then(function(data) {
        $scope.allowed_moves = data.moves;

      })


    }



    $scope.doMove = function(x, y) {

      backendService.doMove($scope.gameId, $scope.playerId, selected.bid, selected.orientation_id, x, y)
      console.log("moved")



    }


    move_allowed = function(i, j) {

      var res = 0;
      $scope.allowed_moves.forEach(function(e) {

        n = parseInt(e[0]);
        m = parseInt(e[1]);
        if ((n == i) && (m == j)) res++;


      })
      if (res > 0) return true;
      else return false;

    }


    calculate_coords = function(val, horizontal) {

      if (horizontal) {
        return parseInt(Math.round((val - shiftx) / grid));


      }
      else {
        return parseInt(Math.round((val - shifty) / grid));

      }


    }


    $scope.positionBlocks = function() {
      var y = grid;
      var x = 450;
      var color;
      if ($scope.playerId == 1) color = 'orange';
      else color = '#B164DE';

      $scope.blocks.forEach(function(element, index) {
        x = x + 120;
        if (x > 450 + 600) {
          x = 450 + 120;
          y = y + 80;
        }



        var group = new paper.Group([]);
        group.bid = index;
        group.orientation_id = 0;
        group.locked = false;


        for (var j = 0; j < element.shape.length; j++) {

          for (var i = 0; i < element.shape[0].length; i++) {

            if (element.shape[j][i] > 0) {



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



        group.onMouseDown = function() {
          console.log("down");
          if (this.locked || $scope.blocked) return;

          if ((selected == null) || (selected.bid != this.bid)) {
            selected = this;
            $scope.getMoves();
            console.log("I'm selected");
          }

          if (event.detail == 2) {
            this.orientation_id += 1;
            if (this.orientation_id >= 4) this.orientation_id = this.orientation_id - 4;

            $scope.getMoves();

            this.rotate(90, this.center);
            console.log("I'm rotated");
          }
          if (event.detail == 1) {
            this.opacity = 1;
            this.bringToFront();
          };
        };


        group.onMouseDrag = function(event) {
          if (this.locked || $scope.blocked) return;
          this.position = event.point;
          if ((this.bounds.left <= 435) && (this.bounds.top <= 370) && (this.bounds.left > 86) && (this.bounds.top > 32)) {

            var offsetx = Math.round(this.bounds.size.width / 2);
            var offsety = Math.round(this.bounds.size.height / 2);

            this.position = new paper.Point(offsetx + (Math.round((this.position.x - offsetx) / grid) * grid),
              offsety + (Math.round((this.position.y - offsety) / grid) * grid));
          };
          console.log("I'm dragged");
        };


        group.onMouseUp = function() {
          console.log("up");
          if ($scope.blocked) {

            console.log('blocked');
            this.position = this.initialPosition;
            return;

          }
          this.opacity = 0.75;
          if (this.bid != selected.bid) return;
          console.log("I'm dropped");

          var x = calculate_coords(selected.bounds.left, true);
          var y = calculate_coords(selected.bounds.top, false);

          if (move_allowed(x, y)) {
            $scope.doMove(x, y)
            this.locked = true;
            console.log('allowed')

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