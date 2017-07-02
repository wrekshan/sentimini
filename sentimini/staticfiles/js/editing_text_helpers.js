function getTime(hours, minutes) {
    var time = null;
    minutes = minutes + "";
    if (hours < 12) {
        time = "AM";
    }
    else {
        time = "PM";
    }
    if (hours == 0) {
        hours = 12;
    }
    if (hours > 12) {
        hours = hours - 12;
    }
    if (minutes.length == 1) {
        minutes = "0" + minutes;
    }
    return hours + ":" + minutes + " " + time;
}

function slideTime_start(event, ui){
    console.log("IN FUCTION staticfiles")
    var val0 = slider.noUiSlider.get()[0],
        val1 = slider.noUiSlider.get()[1],
        minutes0 = parseInt(val0 % 60, 10),
        hours0 = parseInt(val0 / 60 % 24, 10),
        minutes1 = parseInt(val1 % 60, 10),
        hours1 = parseInt(val1 / 60 % 24, 10);
        startTime = getTime(hours0, minutes0);
        endTime = getTime(hours1, minutes1);
        return startTime
}



function slideTime_end(event, ui){
    var val0 = slider.noUiSlider.get()[0],
        val1 = slider.noUiSlider.get()[1],
        minutes0 = parseInt(val0 % 60, 10),
        hours0 = parseInt(val0 / 60 % 24, 10),
        minutes1 = parseInt(val1 % 60, 10),
        hours1 = parseInt(val1 / 60 % 24, 10);
        startTime = getTime(hours0, minutes0);
        endTime = getTime(hours1, minutes1);
        return endTime       
}


