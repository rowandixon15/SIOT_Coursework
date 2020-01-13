function GetData() {
 var GusRange = SpreadsheetApp.getActiveSpreadsheet().getRange("G2");
 var GusHome = GusRange.getValue();
 var GusHomePast = SpreadsheetApp.getActiveSpreadsheet().getRange("G3").getValue();

 //var ui = SpreadsheetApp.getUi();


  if (GusHome == '1' &&
     GusHomePast == '0'){
    var emailAddress = 'rowan.dixon15@gmail.com';
    // Send Alert Email.
    var message = 'Person C Has just arrived home'; // Second column
    var subject = 'Person C';
    MailApp.sendEmail(emailAddress, subject, message);
    //ui.alert('Gus is home');
  }


}
