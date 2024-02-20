const f = require("Storage").open("datalogs.txt", "w");
f.write("Time,Timestamp,X,Y,Z,Magnitue\n");

const f1 = require("Storage").open("pressurelogs.txt", "w");
f1.write("Time,Timestamp,Pressure\n");

Bangle.setBarometerPower(true);
var start = getTime();

const recordAccel = () => {
    const accel = Bangle.getAccel();
    const time = new Date();
    const t1 = getTime() - start;
    t =
        ("0" + time.getHours()).slice(-2) +
        ":" +
        ("0" + time.getMinutes()).slice(-2) +
        ":" +
        ("0" + time.getSeconds()).slice(-2);
    f.write([t, t1, accel.x, accel.y, accel.z, accel.mag].join(",") + "\n");
};

const recordPressure = () => {
    const pressure = Bangle.getPressure();
    const time = new Date();
    const t2 = getTime() - start;
    t =
        ("0" + time.getHours()).slice(-2) +
        ":" +
        ("0" + time.getMinutes()).slice(-2) +
        ":" +
        ("0" + time.getSeconds()).slice(-2);
    f1.write([t, t2, pressure.pressure].join(",") + "\n");
};

setInterval(() => {
    recordAccel();
    recordPressure();
}, 20);
