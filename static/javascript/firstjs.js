var count=0;
var arr=[];
function getInput(){
if(count<2){
count++;
var x=document.forms["f1"]["inp1"].value;

arr.push(x)
//document.forms["f1"]["inp1"].placeholder="password";
document.getElementById("input123").value="";
document.getElementById("input123").placeholder="Password";
//alert(x)
document.getElementById("demo").innerHTML='submitted:'+arr;
document.getElementById("demo").style.fontSize = "25px";
document.getElementById("next").style.backgroundColor = "green";
}
else{
alert('you are already submitted username and password')
}
}