# Библиотеки для работы:

* https://github.com/taka-wang/py-beacon
* https://github.com/switchdoclabs/iBeacon-Scanner-

# Пример кода определения расстояния:

`function get_distance(rssi, tx_power) {
   if (rssi == 0) {
      return -1; // Невозможно определить расстояние
   }
   var ratio = rssi / tx_power;
   if (ratio < 1) {
      return Math.pow(ratio, 10);
   } else {
      return 0.89976 * Math.pow(ratio, 7.7095) + 0.111;
   }
}`
* tx_power - Мощность на дистанции 1 метр(Производитель)
* rssi - Текущая определяемая мощность от метки