# Raporti i studentit: UrbanBike AI

Studenti: Raport i përbashkët i grupit

Grupi: Tea Muca, Dion Guzja, Antea Ibra, Erastus Bakalli

Data: 13/11/2026

GitHub: [https://github.com/muca69/urbanbike-ai](https://github.com/muca69/urbanbike-ai)

Figma: [https://www.figma.com/design/4uZMOi64HaewjqsX52OgC7/UrbanBikes_AI?node-id=0-1&t=4AQuy6JcpPp2khbk-1](https://www.figma.com/design/4uZMOi64HaewjqsX52OgC7/UrbanBikes_AI?node-id=0-1&t=4AQuy6JcpPp2khbk-1)

## Qëllimi

Problemi që zgjidhim: Qëllimi i projektit UrbanBike AI është të parashikojë kërkesën ditore për biçikleta me qira duke përdorur të dhëna historike, informacione meteorologjike dhe algoritme të Machine Learning.  
Përmes këtij projekti synojmë të kuptojmë se si ndryshon kërkesa për biçikleta në varësi të faktorëve të ndryshëm, si temperatura, reshjet, ditët e javës dhe sezonaliteti. Parashikimet mund të ndihmojnë në planifikimin më të mirë të disponueshmërisë së biçikletave dhe menaxhimin e shërbimit.  

Target-i y: Variabli që synojmë të parashikojmë është `rentals`, i cili përfaqëson numrin total të biçikletave të marra me qira gjatë një dite.

Ky është një problem regresioni, sepse modeli parashikon një vlerë numerike dhe jo një kategori.

Predictorët X: Për parashikimin e kërkesës përdorim disa variabla të krijuara gjatë përgatitjes së të dhënave:

- `rentals_lag1` – numri i qirave një ditë më parë.
- `rentals_lag7` – numri i qirave shtatë ditë më parë.
- `rentals_mean7` – mesatarja e qirave gjatë shtatë ditëve të mëparshme.
- `temp_c_lag7` – temperatura e regjistruar shtatë ditë më parë.
- `rain_mm_lag7` – reshjet e regjistruara shtatë ditë më parë.
- `wind_ms_lag7` – shpejtësia e erës shtatë ditë më parë.
- `trend_days` – numri i ditëve të kaluara nga fillimi i periudhës së analizuar.
- `weekday` – dita e javës.
- `month` – muaji i vitit.
- `workingday` – nëse dita është ditë pune.
- `holiday` – nëse dita është festë.

Koha kur parashikojmë dhe çfarë informacioni është i njohur: Parashikimi realizohet për një ditë të caktuar, duke përdorur vetëm informacionin që do të ishte i disponueshëm përpara fillimit të asaj dite.

  Për këtë arsye, përdorim të dhënat historike të qirave, kushtet meteorologjike të mëparshme dhe informacionin kalendarik, si dita e javës dhe muaji.

  Të dhënat ndahen në mënyrë kronologjike në Train, Validation dhe Test, për të respektuar rendin kohor dhe për të shmangur përdorimin e informacionit nga e ardhmja gjatë trajnimit.

  Në aplikacionin web, përdoruesi mund të zgjedhë një datë nga periudha historike e testimit dhe të shohë parashikimin e modelit Ridge Regression, vlerën reale të qirave dhe gabimin absolut të parashikimit.

## Pastrimi

Burimet reale dhe çelësi i bashkimit:  
Në këtë projekt u mora me përgatitjen dhe pastrimin e të dhënave për përdorim në modelet Machine Learning. Përdora dy burime kryesore: UCI Bike Sharing Dataset, që përmban numrin ditor të biçikletave të marra me qira, dhe NASA POWER, që përmban të dhëna meteorologjike.

Me Python dhe bibliotekën Pandas bashkova të dy datasetet përmes kolonës `date`, duke përdorur validimin `one_to_one` për të siguruar që çdo datë të kishte vetëm një rekord. Dataset-i i bashkuar përmbante 731 rreshta.  

Dallimi mes origjinaleve dhe kopjes didaktike:  
Të dhënat origjinale i ruajta të pandryshuara në `data/raw/`. Pas bashkimit të dy burimeve, ruajta dataset-in e bashkuar në `data/processed/merged_original.csv`, përpara krijimit të kopjes didaktike me probleme. Më pas krijova një kopje didaktike në `data/teaching/dirty.csv`, ku simulova probleme të zakonshme si vlera që mungojnë, të dhëna tekstuale të pavlefshme dhe dublikime.

Kjo më mundësoi të demonstroja procesin e pastrimit pa ndryshuar burimet origjinale.

Rreshtat para/pas:  

- UCI Bike Sharing Dataset: 731 rreshta.
- NASA POWER: 731 rreshta.
- Dataset-i pas bashkimit: 731 rreshta.
- Kopja didaktike: 743 rreshta.
- Pas heqjes së dublikimeve: 731 rreshta.
- Dataset-i përfundimtar: 724 rreshta dhe 16 kolona.

Dublimet:  
Në kopjen didaktike krijova 12 rreshta të dyfishuar. Për identifikimin dhe eliminimin e tyre përdora `drop_duplicates()` dhe kontrollova që datat të ishin unike dhe të renditura kronologjikisht.  

Mungesat para/pas konvertimit:  
Në kopjen didaktike simulova 30 qeliza bosh: 18 në temperaturë dhe 12 në reshje. Gjithashtu, vendosa 6 vlera tekstuale `"gabim"` në kolonën e temperaturës.

  Me `pd.to_numeric(errors="coerce")`, vlerat e pavlefshme u konvertuan në `NaN`, duke rezultuar në 36 mungesa meteorologjike.

  Në dataset-in përfundimtar u identifikuan 72 qeliza bosh, të shpërndara në kolonat `temp_c`, `rain_mm`, `temp_c_lag7` dhe `rain_mm_lag7`.  

  Arsyeja e imputimit vetëm me train: Vendosa të mos i zëvendësoja mungesat me zero, sepse zero mund të jetë një vlerë reale meteorologjike.

  Imputimi realizohet në fazën Machine Learning përmes një `Pipeline`, ku mediana llogaritet vetëm mbi të dhënat e trajnimit. Kjo shmang *data leakage*, duke mos lejuar që informacioni nga validation ose test të ndikojë në trajnimin e modelit.

  **Përfundimi:**

  Në përfundim përgatita dataset-in për Machine Learning dhe krijova variabla kohore si `rentals_lag1`, `rentals_lag7`, `rentals_mean7` dhe `trend_days`.

  Gjithashtu, gjenerova raportet `data_quality.json` dhe `teaching_changes.json` për dokumentimin e procesit të pastrimit.

## Grafikët

**Vëzhgimi 1 dhe figura përkatëse:**

Figura `reports/01_daily_demand.png` paraqet ndryshimin e kërkesës ditore për biçikleta gjatë periudhës së trajnimit, nga 08.01.2011 deri më 30.04.2012.

Janë analizuar 479 ditë. Mesatarja ditore është 3,700.77 qira, minimumi 431, maksimumi 8,362 dhe devijimi standard 1,482.30.

**Vëzhgimi 2 dhe figura përkatëse:**

Figura `reports/02_monthly_demand.png` paraqet kërkesën mesatare ditore sipas muajve dhe evidenton ndryshimet sezonale të kërkesës.

Figura `reports/03_temperature_demand.png` paraqet marrëdhënien midis temperaturës dhe numrit të qirave. Koeficienti i korrelacionit Pearson është 0.5820, duke treguar një lidhje pozitive mesatare.

**Pse një lidhje e dukshme nuk provon shkakësi:**

Korrelacioni pozitiv nuk provon që temperatura është shkaku i vetëm i rritjes së kërkesës. Faktorë të tjerë, si sezoni, reshjet, festat dhe ditët e punës, mund të ndikojnë gjithashtu.

**Metodologjia:**

Analiza eksploruese është realizuar vetëm mbi periudhën train, duke përdorur të njëjtin dataset dhe të njëjtat data trajnimi si modelet e Machine Learning. Të dhënat e validimit dhe testimit nuk janë përdorur në grafikët e analizës eksploruese.

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

**Rezultati i klasifikimit, nëse u realizua: N**ë këtë projekt nuk u implementua klasifikimi, pasi objektivi kryesor ishte parashikimi i numrit ditor të qirave, i cili është një problem regresioni. Për këtë arsye, u përdorën modelet e regresionit dhe metrikat MAE, RMSE dhe R².

## Kufizimet

1. **Kufizimet e të dhënave:** Projekti përdor të dhëna historike nga UCI Bike Sharing dhe NASA POWER për periudhën 2011–2012. Për këtë arsye, modeli nuk është testuar me të dhëna më të fundit dhe nuk mund të garantojmë që do të ketë të njëjtën performancë në kushte aktuale. Gjithashtu, disa vlera meteorologjike mungojnë dhe trajtohen përmes imputimit, gjë që mund të ndikojë në saktësinë e parashikimeve.
2. **Kufizimet e modelit Machine Learning:** Megjithëse Ridge Regression rezultoi modeli më i mirë gjatë validimit, në test arriti MAE = 893.251 dhe R² = 0.591. Kjo do të thotë se parashikimet devijojnë mesatarisht me rreth 893 qira në ditë nga vlerat reale. Modeli mund të ketë vështirësi në parashikimin e ndryshimeve të papritura të kërkesës, të cilat mund të ndikohen nga faktorë që nuk përfshihen në dataset.
3. **Kufizimet e aplikacionit web:** Aplikacioni UrbanBike AI demonstron parashikimet e modelit Ridge Regression duke përdorur datat historike të periudhës së testimit. Aktualisht, përdoruesi nuk mund të parashikojë kërkesën për data të ardhshme, sepse aplikacioni mbështetet në variablat historike të përgatitura paraprakisht. Për përdorim real do të nevojitej integrimi i të dhënave të përditësuara dhe një mekanizëm për gjenerimin e predictorëve për data të reja.

## Kontributet individuale

| Studenti | Skedari/ekrani | Puna dhe vendimi | Commit/prova |  

**Tea Muca — Data Preprocessing**

- Përgjegjëse për përgatitjen, bashkimin dhe pastrimin e të dhënave të projektit UrbanBike AI.
- Realizova bashkimin e dataset-eve UCI Bike Sharing dhe NASA POWER përmes kolonës `date`, duke kontrolluar integritetin dhe unikësinë e të dhënave.
- Krijova një kopje didaktike për simulimin dhe trajtimin e dublikimeve, mungesave dhe vlerave të pavlefshme.
- Implementova konvertimin e vlerave numerike, heqjen e dublikimeve dhe krijimin e variablave kohore për Machine Learning.
- Ruajta mungesat si `NaN`, duke mundësuar imputimin vetëm mbi të dhënat e trajnimit për të shmangur *data leakage*.
- Gjenerova dataset-in përfundimtar me 724 rreshta dhe 16 kolona, si dhe raportet e cilësisë së të dhënave.
- Skedarët kryesorë: `scripts/01_clean.py`, `data/processed/model_data.csv`, `data/teaching/dirty.csv`, `reports/data_quality.json` dhe `reports/teaching_changes.json`.

**Branch:** `feature/data-preprocessing` — bashkuar në `main` përmes Pull Request.

**Dion Guzja — Machine Learning**

- Përgjegjës për zhvillimin dhe implementimin e komponentit Machine Learning të projektit UrbanBike AI.
- Kontributet përfshijnë konfigurimin e ndarjes kronologjike Train / Validation / Test, implementimin e modeleve Yesterday, DummyMean, Ridge Regression dhe RandomForest, ndërtimin e Pipeline për përpunimin e të dhënave, trajnimin dhe vlerësimin e modeleve përmes metrikave MAE, RMSE dhe R².
- Gjithashtu, realizoi përzgjedhjen e modelit përfundimtar bazuar në rezultatet e validimit, gjenerimin e parashikimeve për periudhën e testimit, krijimin e grafikut krahasues dhe ruajtjen e rezultateve për integrimin në aplikacion.
- Skedarët kryesorë: `config/common.py`, `scripts/03_train.py`, `reports/regression_metrics.csv`, `reports/results_summary.json`, `reports/test_predictions.csv` dhe `reports/figures/04_predictions.png`.

**Erastus Bakalli — EDA & Visualization**

- Përgjegjës për analizën eksploruese të të dhënave dhe vizualizimin e rezultateve në projektin UrbanBike AI.
- Realizova analizën statistikore të 479 ditëve të trajnimit, duke llogaritur mesataren, minimumin, maksimumin, devijimin standard dhe korrelacionin ndërmjet temperaturës dhe kërkesës.
- Krijova tre grafikë për kërkesën ditore, kërkesën mesatare mujore dhe marrëdhënien temperaturë–kërkesë.
- Harmonizova periudhën e analizës me ndarjen train të modelit Machine Learning, nga 08.01.2011 deri më 30.04.2012.
- Skedarët kryesorë: `scripts/02_visualize.py`, `reports/01_daily_demand.png`, `reports/02_monthly_demand.png` dhe `reports/03_temperature_demand.png`.

**Commit/prova:** `b98f776` — Align EDA with final ML training period.  

**Antea Ibra — Web Application & UI/UX Design**

- Përgjegjëse për zhvillimin e aplikacionit web dhe dizajnimin e ndërfaqes së përdoruesit në projektin UrbanBike AI.
- Realizoi një dashboard modern dhe responsive duke përdorur Python, HTML dhe CSS, me qëllim që përdoruesi të ndërveprojë lehtësisht me modelin Machine Learning.
- Integroi modelin Ridge Regression në aplikacion, duke mundësuar zgjedhjen e një date nga periudha historike e testimit dhe shfaqjen e parashikimit të kërkesës për biçikleta.
- Implementoi paraqitjen e numrit të parashikuar të qirave, numrit real të qirave dhe gabimit absolut ndërmjet tyre.
- Shtoi seksionin e performancës së modelit me metrikat MAE, RMSE dhe R², grafikun krahasues të vlerave reale me ato të parashikuara dhe tabelën e krahasimit të modeleve Yesterday, DummyMean, Ridge dhe RandomForest.
- U mor edhe me konceptimin e dizajnit UI/UX në Figma, për të krijuar një ndërfaqe të qartë, të organizuar dhe të përshtatshme për përdoruesin.
- Skedari kryesor: `app.py`.

**Commit/prova:** `3ca202a` — Implement UrbanBike AI Web Dashboard.

## Burimet

UCI: https://doi.org/10.24432/C5W894
NASA: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
Provenienca lokale: data/raw/provenance.json
