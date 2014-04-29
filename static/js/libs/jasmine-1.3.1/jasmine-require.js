/* 
    utility global functions for jasmine, global to match existing jasmine global functions 

    It's expected that the last parameter is a function that you want to execute 
    within the context of the require all preceding parameters are passed to the require method

    The most likely way to call this is:

    waitsForRequire(['require_dep1', 'require_dep2',...], function(dep1, dep2) { 
        ...code that gets dependencies...
    }) 
*/
var waitsForRequire = function () {
  var argv = Array.prototype.slice.call(arguments),
      done = false;

  var callback = typeof _.last(argv) === 'function' ? argv.pop() : function(){};

  return function () {
    require.apply(null, argv.concat(function () {
      callback.apply(null, arguments);
      done = true;
    }));

    waitsFor(function () { return done; });
  };
};
