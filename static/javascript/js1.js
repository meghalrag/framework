function fun(){
var x=document.getElementById("input1").value;
x=parseInt(x, 10);

var y=document.getElementById("input2").value;
y=parseInt(y,10);

var z=x*y;

document.getElementById("input3").value=z;


}