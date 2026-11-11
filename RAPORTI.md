# Raporti i studentit: UrbanBike AI

Studenti:
Grupi (nëse punohet në grup):
Data:
GitHub-i im:
Figma:

## Qëllimi

Problemi që zgjidhim:
Target-i y:
Predictorët X:
Koha kur parashikojmë dhe çfarë informacioni është i njohur:

## Pastrimi

Burimet reale dhe çelësi i bashkimit:
Dallimi mes origjinaleve dhe kopjes didaktike:
Rreshtat para/pas:
Dublimet:
Mungesat para/pas konvertimit:
Arsyeja e imputimit vetëm me train:

## Grafikët

## Grafikët

**Vëzhgimi 1 dhe figura përkatëse:**

Figura `reports/01_daily_demand.png` paraqet ndryshimin e kërkesës ditore për biçikleta gjatë periudhës së analizuar.

Analiza tregon një tendencë përgjithësisht rritëse të numrit të qirave, por edhe luhatje të konsiderueshme nga një ditë në tjetrën.

Mesatarja ditore është 3,794.21 qira, ndërsa minimumi dhe maksimumi janë përkatësisht 431 dhe 8,362 qira.

**Vëzhgimi 2 dhe figura përkatëse:**

Figura `reports/02_monthly_demand.png` tregon kërkesën mesatare ditore sipas muajve.

Nga grafiku vërehet se kërkesa është më e lartë gjatë muajve të pranverës dhe verës, me kulmin në maj. Në muajt e dimrit, veçanërisht në janar, kërkesa është më e ulët.

Figura `reports/03_temperature_demand.png` tregon një lidhje pozitive midis temperaturës dhe numrit të qirave, megjithëse marrëdhënia nuk është plotësisht lineare.

**Pse një lidhje e dukshme nuk provon shkakësi:**

Një korrelacion midis temperaturës dhe kërkesës për biçikleta nuk do të thotë domosdoshmërisht se temperatura është shkaku i vetëm i ndryshimit të kërkesës.

Faktorë të tjerë, si sezoni, reshjet, ditët e punës, festat dhe sjellja e përdoruesve, mund të ndikojnë gjithashtu.

## Vlerësimi

| Modeli       | Validation MAE | Test MAE | Test RMSE | Test R² |
| ------------ | -------------: | -------: | --------: | ------: |
| Yesterday    |                |          |           |         |
| DummyMean    |                |          |           |         |
| Ridge        |                |          |           |         |
| RandomForest |                |          |           |         |

Modeli i zgjedhur nga validation dhe arsyeja:
Rezultati i provës me Random Forest:
Interpretimi i gabimit në qira për ditë:
Rezultati i klasifikimit, nëse u realizua:

## Kufizimet

1.
2.
3.

## Kontributet individuale

| Studenti | Skedari/ekrani | Puna dhe vendimi | Commit/prova |
| -------- | -------------- | ---------------- | ------------ |
|          |                |                  |              |
|          |                |                  |              |
|          |                |                  |              |

## Burimet

UCI: https://doi.org/10.24432/C5W894
NASA: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
Provenienca lokale: data/raw/provenance.json
