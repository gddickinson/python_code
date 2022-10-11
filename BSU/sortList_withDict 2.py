# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:07:59 2019

@author: GEORGEDICKINSON
"""

import numpy as np

centeroids = np.array([
        
           [255.65026699, 256.2699313 ],
           [255.65522196, 255.9542909 ],
           [255.65336587, 256.16112367],
           [255.66110178, 255.74295807],
           [255.74678208, 256.05605212],
           [255.74547016, 256.16300094],
           [255.75104081, 256.2720415 ],
           [255.75228561, 255.84415798],
           [255.75351785, 255.95273798],
           [255.75479689, 255.73969906],
           [255.84866381, 256.05934078],
           [255.84685329, 256.16708376],
           [255.85103522, 256.27369471],
           [255.85160587, 255.74273925],
           [255.85740968, 255.85026562],
           [255.94392418, 256.27673285],
           [255.94391768, 256.05966314],
           [255.94611554, 256.17014591],
           [255.95094813, 255.95014021],
           [255.95158306, 255.85177168],
           [255.95400055, 255.74037337],
           [256.03677785, 256.2720229 ],
           [256.03969133, 256.06114094],
           [256.04283514, 256.16603679],
           [256.04661846, 255.85896198],
           [256.04490558, 255.96022842],
           [256.05086907, 255.7461775 ],
           [256.14012688, 256.1753788 ],
           [256.14023585, 256.0697952 ],
           [256.140229  , 256.2836567 ],
           [256.14513271, 255.75414015],
           [256.14299781, 255.96175843],
           [256.2314431 , 256.17345542],
           [256.23032086, 256.28052939],
           [256.23801515, 256.06644361],
           [256.23637598, 255.96237802],
           [256.2397271 , 255.75018973],
           [256.23966435, 255.85825364],
           [256.32819487, 256.17121161],
           [256.33097833, 255.75340018],
           [256.32980017, 256.06243964],
           [256.32933863, 255.96060716],
           [256.33441629, 255.85686116],
           [256.144     , 255.865     ],
           [255.851     , 255.954     ],
           [255.652     , 256.057     ],
           [255.659     , 255.846     ],
           [256.327     , 256.281     ]]

)


remap={  33:2,
         29:3,
         21:4,
         15:5,
         12:6,
         6:7,
         0:8,
         38:9,
         32:10,
         27:11,
         23:12,
         17:13,
         11:14,
         5:15,
         2:16,
         40:17,
         34:18,
         28:19,
         22:20,
         16:21,
         10:22,
         4:23,
         41:25,
         35:26,
         31:27,
         25:28,
         18:29,
         44:30,
         8:31,
         1:32,
         42:33,
         37:34,
         43:35,
         24:36,
         19:37,
         14:38,
         7:39,
         39:41,
         36:42,
         30:43,
         26:44,
         20:45,
         13:46,
         9:47,
         3:48,
         47:1,
         45:24,
         46:40                                                                         
         }

centeroids = centeroids.tolist()

sortedList = []

#for key in sorted(remap.keys()):
#    print(remap[key]-1)
#    sortedList.append(centeroids[remap[key]-1])

def getKey(item):
    return item[1]    

for elem in sorted(remap.items(),key=getKey) :
    #print(elem[0] , " ::" , elem[1] )
    print(elem[0])
    sortedList.append(centeroids[elem[0]])