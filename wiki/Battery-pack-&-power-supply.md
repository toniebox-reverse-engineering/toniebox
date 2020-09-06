# Battery
* Voltage: 3.6V
* Chemistry: NiMH
* Cells: 3
* Size: AA

## NTC (Thermistor) white cable
* 22°C - 10kOhm
* 35°C - 6kOhm
* 5°C  - 30kOhm 
* MF58 10kOhm 3950K (Confirmed by Boxine)

## Plug
* JST PH 2mm 3pin

## Cable Length for custom battery packs
* Black: 17cm
* Red: 15cm
* White: 15cm

## ADC Voltage Map
| Box ID | User | voltage in V | ADC raw | charging| original battery | notes |
| -- | -- | -- | -- | -- | -- | -- |
| B-Dev Blue | SciLor | 3.975 | 2701 | 0 | 1 |  |
| B-Dev Blue | SciLor | 4.16 | 2824 | 0 | 1 |  |
| B-Dev Blue | SciLor | 4.25 | 2882 | 0 | 1 | Max |
| B-Dev Blue | SciLor | 4.39 | 3188 | 1 | 1 |  |
| B-Dev Blue | SciLor | 4.44 | 3195 | 1 | 1 | Max |
| Lila | SciLor | 3.686 | 2489 | 0 | 0 |  |
| Lila | SciLor | 3.659 | 2478 | 0 | 0 | Shut Off Message |
| Lila | SciLor | 4.26 | 2870 | 0 | 0 | Max |
| Lila | SciLor | 4.47 | 3180 | 1 | 0 | Max |
| Red | SciLor | 3.641 | 2456 | 0 | 0 |  |
| Red | SciLor | 3.540 | 2400 | 0 | 0 | Shut Off Message |

Voltage measurement TP38
```
from machine import Pin
from machine import ADC
p_charger = Pin('GP17', mode=Pin.IN)
p_charger.value()
adc = ADC()
p_battery = adc.channel(pin='GP5')
p_battery.value()
```

## Photos (Custom Battery Pack) 
![](https://raw.githubusercontent.com/toniebox-reverse-engineering/toniebox/master/pics/battery_custom_compare.jpg)
![](https://raw.githubusercontent.com/toniebox-reverse-engineering/toniebox/master/pics/battery_custom1.jpg)
![](https://raw.githubusercontent.com/toniebox-reverse-engineering/toniebox/master/pics/battery_custom2.jpg)
![](https://raw.githubusercontent.com/toniebox-reverse-engineering/toniebox/master/pics/battery_custom3.jpg)

# Power supply
* Voltage: 9V
* Current: 1.5A
* Plug 5.5x2.1mm (+9V inner side)

## Photo
![](https://raw.githubusercontent.com/toniebox-reverse-engineering/toniebox/master/pics/powersupply_station.jpg)
