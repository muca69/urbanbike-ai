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

Vëzhgimi 1 dhe figura përkatëse:
Vëzhgimi 2 dhe figura përkatëse:
Pse një lidhje e dukshme nuk provon shkakësi:

## Vlerësimi

| Modeli       | Validation MAE | Test MAE | Test RMSE | Test R² |
| ------------ | -------------: | -------: | --------: | ------: |
| Yesterday    |        775.203 |  916.402 |  1330.386 |   0.539 |
| DummyMean    |       2953.866 | 2494.628 |  2790.064 |  -1.027 |
| Ridge        |        687.558 |  893.251 |  1252.655 |   0.591 |
| RandomForest |       1821.528 | 1671.499 |  2042.654 |  -0.087 |

**Modeli i zgjedhur nga validation dhe arsyeja:**

Modeli i përzgjedhur është **Ridge Regression**, pasi arriti vlerën më të ulët të MAE në validation (687.558), krahasuar me RandomForest (1821.528). Në test, Ridge arriti MAE = 893.251, RMSE = 1252.655 dhe R² = 0.591, duke treguar performancën më të mirë ndër modelet e vlerësuara.

**Rezultati i provës me Random Forest:**

RandomForest u trajnua me 200 pemë vendimmarrjeje, thellësi maksimale 8 dhe `min_samples_leaf=4`. Në validation arriti MAE = 1821.528, RMSE = 2017.942 dhe R² = -3.595. Në test arriti MAE = 1671.499, RMSE = 2042.654 dhe R² = -0.087. Këto rezultate tregojnë se RandomForest performoi më dobët se Ridge dhe modeli bazë Yesterday.

**Interpretimi i gabimit në qira për ditë:**

Modeli Ridge ka një MAE prej 893.251 në test. Kjo do të thotë se parashikimet e tij devijojnë mesatarisht me rreth **893 qira biçikletash në ditë** nga vlerat reale. Krahasuar me Yesterday (MAE = 916.402), Ridge reduktoi gabimin mesatar me rreth 2.5%. Megjithatë, gabimi mbetet i konsiderueshëm, veçanërisht në ditët me ndryshime të mëdha të kërkesës.

**Rezultati i klasifikimit, nëse u realizua:**

## Kufizimet

1.
2.
3.

## Kontributet individuale

| Studenti | Skedari/ekrani | Puna dhe vendimi | Commit/prova |
| | | | |
| | | | |
| | | | |

**Dion Guzja — Machine Learning**

- Përgjegjës për zhvillimin dhe implementimin e komponentit Machine Learning të projektit UrbanBike AI.
- Kontributet përfshijnë konfigurimin e ndarjes kronologjike Train / Validation / Test, implementimin e modeleve Yesterday, DummyMean, Ridge Regression dhe RandomForest, ndërtimin e Pipeline për përpunimin e të dhënave, trajnimin dhe vlerësimin e modeleve përmes metrikave MAE, RMSE dhe R².
- Gjithashtu, realizoi përzgjedhjen e modelit përfundimtar bazuar në rezultatet e validimit, gjenerimin e parashikimeve për periudhën e testimit, krijimin e grafikut krahasues dhe ruajtjen e rezultateve për integrimin në aplikacion.
- Skedarët kryesorë: `config/common.py`, `scripts/03_train.py`, `reports/regression_metrics.csv`, `reports/results_summary.json`, `reports/test_predictions.csv` dhe `reports/figures/04_predictions.png`.

## Burimet

UCI: https://doi.org/10.24432/C5W894
NASA: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
Provenienca lokale: data/raw/provenance.json
