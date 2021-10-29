function sort() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheets()[0].sort(4,false);
  var url = "https://docs.google.com/spreadsheets/d/1N1BPr5nNdDdCBQnolp7yjRF4uWirnFtZZXnIy_7D2NE/edit#gid=0";
  GmailApp.sendEmail('bahadiryalcin23@gmail.com','Scrapted data','Scrap edilmiş datayı aşağıdaki linkten ulaşabilirsiniz    \n'+ url)
}
