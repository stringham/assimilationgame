goog.provide('a.util');

a.util.map = function(a, f){
	for(var i=0; i<a.length; i++){
		f(a[i],i);
	}
};