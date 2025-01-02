dayOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
monthOfYear =  ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] 




$('.month').click(function() {
    var date = "";
    var month = $(this).text()
    month = month.trim()
    var month_number = monthOfYear.indexOf(month) + 1
    var month_number_as_string = month_number.toString()
    var today = new Date();
    var current_year = today.getFullYear();
    date = month_number_as_string + "/01/" + current_year
    console.log(month, month_number)
    $('#datepickerFACT').datepicker('setDate', date);
    $('#datepickerLAP').datepicker('setDate', date);
});


function highlight_all() {
    // not used
    var array = $(".day").toArray()
    array.forEach(element => {
        element.classList.add('active')
    });
};

$('#datepickerFACT').datepicker({
    maxViewMode: 0,
    multidate: true,
});

$('#datepickerLAP').datepicker({
    maxViewMode: 0,
    multidate: true,
});


function getDayNumbersHighlighted(datepicker)  {
    // select specific dates
    const dates_to_highlight = $(datepicker).datepicker('getDates');
    var days_of_month = []
    dates_to_highlight.forEach(date => {
    // get day number from dates
        var day_of_month = date.getDate()
        days_of_month.push(day_of_month)
    });
    return days_of_month
};

function highlightDatesOnDatepicker(datepicker_cells, days_of_month) {
    // select all dates on datepicker
    var all_cells = $(datepicker_cells).toArray()
    var cells_to_highlight = []
    // highlight cells
    days_of_month.forEach(day_of_month => {
        var cell_to_highlight = all_cells.filter((cell) => 
            cell.innerHTML == day_of_month);
        cell_to_highlight.forEach(cell => {
            cells_to_highlight.push(cell)
        });
    });
    cells_to_highlight.forEach(cell => {
        cell.classList.add('highlighted_cell')
    });
};

function highlightOtherDatePicker(IdDatepickerToGetFrom, IdDatepickerToChange) {
    //reset highlighted
    var days_of_month = getDayNumbersHighlighted(IdDatepickerToGetFrom)
    const datepicker_cells = IdDatepickerToChange + ' td'
    highlightDatesOnDatepicker(datepicker_cells, days_of_month)
};

function highlightBothDatePickers(datepicker1, datepicker2) {
    // reset previous highlights
    $('.highlighted_cell').removeClass('highlighted_cell');
    // highlight both depending on each other
    highlightOtherDatePicker(datepicker1, datepicker2);
    highlightOtherDatePicker(datepicker2, datepicker1);

}

function createDateString(dateObject) {
    var dateString = ""
    const monthNumber = dateObject.getMonth()
    const monthName = monthOfYear[monthNumber]
    const dayOfMonth = dateObject.getDate().toString()
    const dayOfWeekNumber = dateObject.getDay()
    const dayOfWeekName = dayOfWeek[dayOfWeekNumber]
    dateString = monthName + " " + dayOfMonth + " - " + dayOfWeekName;
    return dateString
}

function createListOfStrings(datesObject) {
    var dateStrings = []
    datesObject.forEach(date => {
        dateString = createDateString(date)
        dateStrings.push(dateString)
    });
    return dateStrings
}

function concatenateStringsFromLists(listOfStrings) {
    var datesString = ""
    listOfStrings.forEach(string => {
        datesString = datesString + "<br>" + string
    });
    datesString = datesString.slice(4,)
    return datesString
}


function addStringAsNewPara(string, targetDivLocater) {
    // make new p with date for every date
    const newP = document.createElement("p")
    newP.innerHTML = string
    newP.className = "date"
    targetDivJQ = $(targetDivLocater)[0] //same as get element by id - returns DOM HTML object 
    targetDivJQ.appendChild(newP)
}

function addDatesFromDatepickerAsPara(datepicker, target_div_id) {
    // get dates
    var datesObject = datepicker.datepicker('getDates')
    // sort dates by dayOfMonth
    datesObject.sort(function(a,b) {
        return new Date(a.getDate()) - new Date (b.getDate())
    });
    // convert date to readable for every date in dates
    const dateStrings =  createListOfStrings(datesObject)

    // delete previous p
    $(target_div_id)[0].textContent = '';

    var datesString = concatenateStringsFromLists(dateStrings)
    addStringAsNewPara(datesString, target_div_id)
}

function createDatePickerString(datepicker) {
    // get dates
    var datesObject = datepicker.datepicker('getDates')
    // sort dates by dayOfMonth
    datesObject.sort(function(a,b) {
        return new Date(a.getDate()) - new Date (b.getDate())
    });
    // convert date to readable for every date in dates
    const dateStrings =  createListOfStrings(datesObject)

    var datesString = ""
    dateStrings.forEach(string => {
        datesString = datesString + "\n" + string
    });
    // datesString = datesString.slice(0,-3)
    return datesString
}

// add string as para
$('#datepickerFACT').on('changeDate', function(){
    //update highlighted
    highlightBothDatePickers('#datepickerFACT', '#datepickerLAP')
    // addDatesFromDatepickerAsPara($(this), '#div')

    // create new string
    var default_email_form_text = "Hi,\n\nPlease find schedule attached below.\n\nFACT Shifts:\n\nLAP Shifts:\n\nThanks,\nAhmed"
    var array = default_email_form_text.split(":")
    console.log(createDatePickerString($(this)))
    array[0] = array[0].concat(": ",createDatePickerString($('#datepickerFACT')))
    array[1] = array[1].concat(": ",createDatePickerString($('#datepickerLAP')))
    console.log(array)
    var output = ""
    array.forEach(element =>  {
        output = output + element
    });
    // apply new string
    $('textarea')[0].value = output

});

$('#datepickerLAP').on('changeDate', function(){
    //update highlighted
    highlightBothDatePickers('#datepickerFACT', '#datepickerLAP')
    // addDatesFromDatepickerAsPara($(this), '#div2')

    // create new string
    var default_email_form_text = "Hi,\n\nPlease find schedule attached below.\n\nFACT Shifts:\n\nLAP Shifts:\n\nThanks,\nAhmed"
    var array = default_email_form_text.split(":")
    console.log(createDatePickerString($(this)))
    array[0] = array[0].concat(": ",createDatePickerString($('#datepickerFACT')))
    array[1] = array[1].concat(": ",createDatePickerString($('#datepickerLAP')))
    console.log(array)
    var output = ""
    array.forEach(element =>  {
        output = output + element
    });
    // apply new string
    $('textarea')[0].value = output
});

$('#gCalendarSubmit').click(function() {
    console.log("gCalendarSubmit")
    var FACTDates = $('#datepickerFACT').datepicker('getDates')
    var LAPDates = $('#datepickerLAP').datepicker('getDates')
    var FACTDatesStrings = []
    FACTDates.forEach(element => {
        var isodate = element.toISOString()
        FACTDatesStrings.push(isodate)
        console.log(isodate)
        console.log(typeof(isodate))
    }) 
    console.log(FACTDatesStrings)
    var LAPDatesStrings = []
    LAPDates.forEach(element => {
        var isodate = element.toISOString()
        LAPDatesStrings.push(isodate)
        console.log(isodate)
        console.log(typeof(isodate))
    }) 
    console.log(LAPDatesStrings)
    $.post("/scheduler", {"FACTDatesStrings": FACTDatesStrings, "LAPDatesStrings": LAPDatesStrings})
})