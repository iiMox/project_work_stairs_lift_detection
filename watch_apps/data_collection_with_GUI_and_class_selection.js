var f = require("Storage").open("datalogs.txt", "w");
f.write("Time,Timestamp,X,Y,Z,Magnitude,Class\n");

var f1 = require("Storage").open("pressurelogs.txt", "w");
f1.write("Time,Timestamp,Pressure,Class\n");

Bangle.setBarometerPower(true);
var start = getTime();
var res = 0;

Bangle.setPollInterval(20);
Bangle.on('accel',function(accel){
    var time = new Date();
    var t1 = getTime() - start;
    t = (("0" + time.getHours()).slice(-2)   + ":" + 
        ("0" + time.getMinutes()).slice(-2) + ":" + 
        ("0" + time.getSeconds()).slice(-2));
    f.write([
        t,t1,
        accel.x,
        accel.y,
        accel.z,
        accel.mag,
        res,
      ].join(",")+"\n");
});


Bangle.setPollInterval(80);
Bangle.on('pressure',function(pressure){
    var time = new Date();
    var t2 = getTime() - start;
    t = (("0" + time.getHours()).slice(-2)   + ":" + 
        ("0" + time.getMinutes()).slice(-2) + ":" + 
        ("0" + time.getSeconds()).slice(-2));
    f1.write([
        t,t2,
        pressure.pressure,
        res,
      ].join(",")+"\n");
});

// First menu
var mainmenu = {
  "" : {
    "title" : "-- Main Menu --"
  },

  "Lift Up" : function() {res="LU";Bangle.beep(); },
  "Lift Down" : function() {res="LD";Bangle.beep(); },
  "NULL" : function() {res="N";Bangle.beep(); },
  "Stair Up" : function() {res="SU";Bangle.beep();},
  "Stair Down" : function() {res="SD";Bangle.beep();},
  "Exit" : function() { E.showMenu(mainmenu); },

};

// Actually display the menu
E.showMenu(mainmenu);




