const f = require("Storage").open("datalogs.txt", "w");
f.write("Time,Timestamp,X,Y,Z,Magnitude\n");

const f1 = require("Storage").open("pressurelogs.txt", "w");
f1.write("Time,Timestamp,Pressure\n");

Bangle.setBarometerPower(true);
var start = getTime();

const recordAccel = () => {
    const accel = Bangle.getAccel();
    const time = new Date();
    const t1 = getTime() - start;
    t = `${time.getHours().toString().padStart(2, 0)}:${time
        .getMinutes()
        .toString()
        .padStart(2, 0)}:${time.getSeconds().toString().padStart(2, 0)}.${time
        .getMilliseconds()
        .toString()
        .padStart(3, 0)}`;
    f.write([t, t1, accel.x, accel.y, accel.z, accel.mag].join(",") + "\n");
};

const recordPressure = () => {
    Bangle.getPressure().then((pressure) => {
        const time = new Date();
        const t2 = getTime() - start;
        t = `${time.getHours().toString().padStart(2, 0)}:${time
            .getMinutes()
            .toString()
            .padStart(2, 0)}:${time
            .getSeconds()
            .toString()
            .padStart(2, 0)}.${time
            .getMilliseconds()
            .toString()
            .padStart(3, 0)}`;
        f1.write([t, t2, pressure.pressure].join(",") + "\n");
    });
};

setInterval(() => {
    recordAccel();
    recordPressure();
}, 20);
