// variables = container to store values
// ~7 types: number , string , 
// command : prompt() -opens up a window



var prompt = require("prompt");
prompt.start();
console.log("I will now ask you for your name.");
prompt.get(["name"], function(err, res){
console.log("Hello ".concat(res.name, ". How are you"));
if (res.name == "Jonty"){
    console.log("Your Name is Jonty")
}
else{
    console.log("Your Name isnt Jonty!")
}
});