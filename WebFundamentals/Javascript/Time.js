// If minutes less than 30, "just after" the hour, more than 30, "almost" the next hour
// AM / PM, "in the morning", "in the evening",


var hour = 8;
var minute = 50;
var period = 'AM'

if (minute < 30 && period === 'AM'){
    console.log("it's just after" , hour, "in the morning");
} else {
    console.log("it's almost", hour + 1, "in the morning");
}


var hour = 7;
var minute = 15;
var period = 'PM'

if (minute > 30 && period === 'PM'){
    console.log("it's almost", hour + 1, "in the evening");
} else { 
     console.log("it's just after", hour , "in the evening");
}



