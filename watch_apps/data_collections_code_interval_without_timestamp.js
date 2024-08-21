const f = require("Storage").open("datalogs.txt", "w");

const now = new Date();
const hours = now.getHours().toString().padStart(2, "0");
const minutes = now.getMinutes().toString().padStart(2, "0");
const seconds = now.getSeconds().toString().padStart(2, "0");
const milliseconds = now.getMilliseconds().toString().padStart(3, "0");
const currentTime = `${hours}:${minutes}:${seconds}:${milliseconds}`;

f.write("Start Time:");
f.write(currentTime);
f.write("\nTimestamp,X,Y,Z,Magnitude,Pressure\n");

Bangle.setBarometerPower(true);
var start = getTime();

const recordReadings = () => {
    Bangle.getPressure().then((pressure) => {
        const accel = Bangle.getAccel();
        const t1 = getTime() - start;
        f.write(
            [t1, accel.x, accel.y, accel.z, accel.mag, pressure.pressure].join(
                ","
            ) + "\n"
        );
    });
};

setInterval(() => {
    recordReadings();
}, 20);
