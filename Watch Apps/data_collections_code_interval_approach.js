const f = require("Storage").open("datalogs.txt", "w");
f.write("Time,Timestamp,X,Y,Z,Magnitude,Pressure\n");

Bangle.setBarometerPower(true);
var start = getTime();

const recordReadings = () => {
    Bangle.getPressure().then((pressure) => {
        const accel = Bangle.getAccel();
        const time = new Date();
        const t1 = getTime() - start;
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
        f.write(
            [
                t,
                t1,
                accel.x,
                accel.y,
                accel.z,
                accel.mag,
                pressure.pressure,
            ].join(",") + "\n"
        );
    });
};

setInterval(() => {
    recordReadings();
}, 20);
