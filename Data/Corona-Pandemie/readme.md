- [csv dataset source](https://www.psycharchives.org/en/item/8a0c3db3-d4bf-46dd-8ffc-557430d45ddd)
- [pdf report source](https://www.psycharchives.org/en/item/6ca4de9a-180b-4d01-8ec3-f40151373f06)

- [CSV](https://github.com/BTW25-Data-Science-Challenge/AutoGluon/blob/main/Data/Corona-Pandemie/Bundeslaender_Anteile.csv) with State, Inhabitants, Percentage of Country; generated with population counts from [source](https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Bevoelkerungsstand/Tabellen/bevoelkerung-nichtdeutsch-laender.html)

## Political actions
Actions listed with further explanation and ranked by presumed influence on economy/workers and therefore power consumption:
0 None, 1 Possible, 2 Likely/Strong

| **csv key** | **influence** | **details** |
|-------------|---------------|-------------|
| leavehome   | 1             | Prohibition to leave the apartment without reason (i.e., for nutritional reasons or doctoral visits) |
| dist        | 0             | Recommendations to keep distance of 1.5 m to other persons |
| msk         | 1             | Duty to wear a face mask in public transport, within stores or throughout public space |
| shppng      | 2             | Closure of "non-essential" shops that do not relate to alimentation or medical care, such as bookstores, warehouses |
| hcut        | 2             | Closure of barbershops and related services in the field of body care (e.g., cosmetics studios, tattoo studios) |
| ess_shps    | 2             | Closure of "essential shops not related to alimentation such as car and bicycle dealers, building and gardening supplies markets, pharmacies, drugstores, medical supply stores, petrol stations and banks |
| zoo         | 0             | Closures of zoos |
| demo        | 0             | Prohibition to politically demonstrate in public | 
| school      | 1             | Closure of schools |
| church      | 0             | Closure of churches, mosques, or synagogues |
| onefriend   | 0             | Prohibition to stay in public space in the company of another person who does not belong to the same household |
| morefriends | 0             | Prohibition of meeting with several friends in public places |
| plygrnd     | 0             | Closures of playgrounds |
| daycare     | 2             | Closures of kindergartens or daycare |
| trvl        | 1             | Entry bans and travel restrictions |
| gastr       | 2             | Closure of bars, restaurants etc. |

The dataset contains values _0: Free, 1: Partially Restricted, 2: Fully Restricted_ for each political measure, state & day.

Proposed formula for dataset generation:

CovidInfluence<sub>date</sub> = $\sum_{datasetRows} min(value,1) * (\frac{value}{5}+0.6) * StateInhabitantsPercentage * ActionInfluenceOnEconomy$

- Sets value to 0 for "0 = No-Restriction" (* min(value,1))
- Weighs a value with factor 0.8 for "1 = Partially Restricted", with 1 for "2 = Fully Restricted" (arbitrary, may be adjusted) ($* \frac{value}{5}+0.6$)
- Weighs a value with the share of the population living in the corresponding state ($* StateInhabitantsPercentage$)
- Weighs a value with influence on economy (arbitrary, may be adjusted) ($* ActionInfluenceOnEconomy$)


