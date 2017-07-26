function getNumbers(newArray){
  var numbersOnly = [];

for (var i = 0; i < newArray.length; i++){
    if (typeof newArray[i] == "number"){
    numbersOnly.push(newArray[i])
    }
}   
    console.log(numbersOnly);
    return numbersOnly;
}
getNumbers([11, 'Eagles', 1, 'Redskins', 8, 'Giants', 5]);


