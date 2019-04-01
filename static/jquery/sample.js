$(document).ready(

function(){

$("#demo").click(function()
{
$("#jqsample").animate({left:'800px'},1000).slideUp("slow").slideDown("slow",function(){

    $("#jqsample").css("background-color","#1a73e8");
});


});

});