const f = require("Storage").open("datalogs.txt", "w");
f.write("Time,Timestamp,X,Y,Z,Magnitude,Pressure\n");

Bangle.setBarometerPower(true);
var start = getTime();

let temp = [];
let write = true;

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
        temp.push(
            `${t},${t1},${accel.x},${accel.y},${accel.z},${accel.mag},${pressure.pressure}`
        );
    });
};

const writeData = () => {
    if (!write) return; // Do not write if writing is in progress
    write = false;
    f.write(temp.join("\n") + "\n");
    temp = [];
    write = true;
};

setInterval(() => {
    recordReadings();
}, 20);

setInterval(writeData, 5000); // Write data every 2 seconds
