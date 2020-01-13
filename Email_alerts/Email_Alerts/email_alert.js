
function WeatherAlert() {
 var WeatherVal = SpreadsheetApp.getActiveSpreadsheet().getRange("C2").getValue();
 var WeatherPast = SpreadsheetApp.getActiveSpreadsheet().getRange("C3").getValue();

 //var ui = SpreadsheetApp.getUi();


  if (WeatherVal == 'Thunder' &&
     WeatherPast != 'Thunder'){
    var emailAddress = 'rowan.dixon15@gmail.com';
    // Send Alert Email.
    var message = 'A thunderstorm at your house has just started. Travel Safely!'; // Second column
    var subject = 'Weather Alert!';
    MailApp.sendEmail(emailAddress, subject, message);
    //ui.alert('Thunder Alert');
  }


}
