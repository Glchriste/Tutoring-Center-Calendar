    //This script gets the day of the week and tells the webpage what hours to display for the day.
    var myDate = new Date();
    var currDay = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][myDate.getDay()];
    var hours = document.getElementById("#hours");

    if (currDay == "Friday") {
        hours.innerHTML = "<b>Today's Hours: 8am-5pm</b>"
    } else if (currDay == "Saturday") {
        hours.innerHTML = "<b>Today's Hours: Closed</b>"
    } else if (currDay == "Sunday") {
        hours.innerHTML = "<b>Today's Hours: Closed</b>"
    } else if (currDay == "Monday") {
        hours.innerHTML = "<b>Today's Hours: 8am-8pm</b>"
    } else if (currDay == "Tuesday") {
        hours.innerHTML = "<b>Today's Hours: 8am-8pm</b>"
    } else if (currDay == "Wednesday") {
        hours.innerHTML = "<b>Today's Hours: 8am-8pm</b>"
    } else if (currDay == "Thursday") {
        hours.innerHTML = "<b>Today's Hours: 8am-8pm</b>"
    }