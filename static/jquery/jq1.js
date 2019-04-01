$(document).ready(

function(){


$("#div1").mouseenter(function()
{
$("#div2").slideToggle(1000);
});
$("#a2").click(function()
{
var x=$("#input3").val();
//alert(x);
$("#input1").val(x);
$("#input3").fadeOut(3000,function(){$("#input2").fadeOut(1000,function(){$("#input1").fadeOut(1000,function(){$("#div2").slideUp(1000);});});});

});

});