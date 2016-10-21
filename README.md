# Библиотеки для работы:

* https://github.com/taka-wang/py-beacon
* https://github.com/switchdoclabs/iBeacon-Scanner-

# Схема работы

![alt text][logo]
[logo]: https://habrastorage.org/files/e08/4ba/7ac/e084ba7accf74191b0e8da54f6ce891f.jpg

* Преамбула (4 байта) – префикс пакета, позволяющий установить, что мы имеем дело именно с Beacon-маячком. Всегда равен 4c000215. Преамбула состоит из 4х полей: идентификатор компании (2 байта, в данном примере — 4c00), тип (1 байт, в примере – 0x02) и длина данных (1 байт, значение – 0x15).

* Proximity UUID (16 байт) – Идентификатор группы Beacon-маяков. Например, у нас есть несколько торговых залов, в которых требуется разместить маяки. В таком случае во всех этих залах маяки будут иметь один и тот же UUID, назначенный нами, и это позволит отличать наши маяки от других, посторонних.

* Мажор (2 байта) – позволяет различать небольшой набор маяков внутри одной группы. То есть внутри одной большой группы маяков, идентифицируемой UUID, у нас может быть несколько подгрупп, каждая из которых идентифицируется по номеру мажора. Например, в нашем примере, каждому залу можно присвоить свой номер мажора. Если маяками требуется охватить несколько этажей здания – обычно с каждым этажом ассоциируют свой номер мажора.

* Минор (2 байта) – номер, идентифицирующий сам маяк внутри мажора. Связка uuid+мажор+минор позволяет нам однозначно идентифицировать маяк и по этим данным определить по таблице соответствия маячков их координатам, координату самого маячка.

* TX Power (параметр K на рисунке выше, 2 байта) – эталонное значение мощности маячка, представляющее собой силу сигнала на расстоянии в 1 метр от маячка. Измеряется и записывается в маячок 1 раз при его производстве. Данная константа используется при определения расстояния от пользователя до маячка. Первый бит является знаковым (1 – «-», 0 – «+»). Например, TX Power в нашем примере (см. рисунок выше, параметр «К») – 0xBE. Это 190 в десятичной системе счисления. Тогда эталонная сила сигнала на расстоянии 1м от маячка составляет 256 — 190 = -66 dBm. 

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