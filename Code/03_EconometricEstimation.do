/****************************************************
 * Script: EconometricEstimation.do
 * Author: Juan Felipe Agudelo
 * Date: Nov  2022
 ****************************************************/

 /*
 1. **Data Loading - Senators:**
   - The script starts by clearing existing data and loading electoral data for Senators from the specified CSV file.

2. **Variable Labeling - Senators:**
   - Relevant variables, such as "Sector social," "Justicia y seguridad," and others, are labeled for clarity in subsequent analyses.

3. **Regression Analysis - Senators:**
   - The script conducts regression analyses on various policy sectors for Senators, considering factors like centrality measures, proportion of new legislators, and clustering by party.

4. **Descriptive Statistics - Senators:**
   - Descriptive statistics, including means, standard deviations, and min/max values, are computed for selected variables and exported to separate files.

5. **Data Loading - Political Parties:**
   - Clearing data again, the script proceeds to load electoral data for Political Parties from a different CSV file.

6. **Regression Analysis - Political Parties:**
   - Similar regression analyses are conducted, this time focusing on the party level, considering variables like centrality measures and proportion of new parties.

7. **Descriptive Statistics - Political Parties:**
   - Descriptive statistics for selected variables at the party level are computed and exported for further examination.

8. **Data Cleanup:**
   - Unnecessary variables are dropped to streamline the dataset and improve clarity.

9. **Exporting Results:**
   - Various results, including regression outputs and descriptive statistics, are exported to LaTeX files for documentation.

10. **Summary Statistics:**
    - Additional summary statistics, such as means and standard deviations, are computed for certain variables and exported for reference.
 */
 
clear all
set more off 
import delimited "/Users/j.agudelo/Library/CloudStorage/OneDrive-UniversidaddelosAndes/HEC/data/Main_dfS.csv"
br

****
*
* SENADORES
* 
****

label var sector_social_per "Sector social"
label var justicia_seguridad_per "Justicia y seguridad"
label var infraestructura_per "Infrastructura"
label var deuda_publica_per "Deuda publica"
label var admon_estado_per "Administracion del estado"
label var degreecentr "Centralidad de Grado"
label var egivector "Centralidad de Bonanich"
label var closesnes "Centralidad de Cercania"
label var nuevo_s "1 si el congresista es nuevo"
label var prop_s "Proporcion de congresistas nuevos"
label var nuevo_p "1 si el partido es nuevo"


reg sector_social_per prop_s c.degreecentr#i.nuevo_s , cluster(nombre_partido)
eststo SD1
reg sector_social_per c.egivector#i.nuevo_s prop_s, cluster(nombre_partido)
eststo SE2
reg sector_social_per c.closesnes#i.nuevo_s prop_s, cluster(nombre_partido)
eststo SA3
esttab S*  using SSOCIAL_SEN.tex, label replace 


reg justicia_seguridad_per prop_s c.degreecentr#i.nuevo_s , cluster(nombre_partido)
eststo JD1
reg justicia_seguridad_per c.egivector#i.nuevo_s prop_s, cluster(nombre_partido)
eststo JE2
reg justicia_seguridad_per c.closesnes#i.nuevo_s prop_s, cluster(nombre_partido)
eststo JA3
esttab J*  using JJUSTICIA_SEN.tex, label replace 


reg infraestructura_per prop_s c.degreecentr#i.nuevo_s , cluster(nombre_partido)
eststo ID1
reg infraestructura_per c.egivector#i.nuevo_s prop_s, cluster(nombre_partido)
eststo IE2
reg infraestructura_per c.closesnes#i.nuevo_s prop_s, cluster(nombre_partido)
eststo IA3
esttab I*  using INF_SEN.tex, label replace 


reg deuda_publica_per prop_s c.degreecentr#i.nuevo_s , cluster(nombre_partido)
eststo DD1
reg deuda_publica_per c.egivector#i.nuevo_s prop_s, cluster(nombre_partido)
eststo DE2
reg deuda_publica_per c.closesnes#i.nuevo_s prop_s, cluster(nombre_partido)
eststo DA3
esttab D*  using DEU_SEN.tex, label replace 


reg admon_estado_per prop_s c.degreecentr#i.nuevo_s, cluster(nombre_partido)
eststo AD1
reg admon_estado_per c.egivector#i.nuevo_s prop_s, cluster(nombre_partido)
eststo AE2
reg admon_estado_per c.closesnes#i.nuevo_s prop_s, cluster(nombre_partido)
eststo AA3
esttab A*  using ADMIN_SEN.tex, label replace 

drop vivienda  unnamed0 trabajo salud sectorsocial relacionesexteriores prop_p policianacional otros obraspúblicas nuevo_p nombres_completos minasyenergía justicia justiciayseguridad infraestructura inf hacienda gobierno gastototal educación desarrollo departamentosadmin defensa deudapublicaintereses congresonacional comunicaciones cgr agricultura admondelestadoyotros codigo_partido votos ano v1



estpost tabstat closesnes degreecentr egivector,by(nuevo_s) statistics(mean sd) columns(statistics) listwise
esttab, main(mean) aux(sd) nostar unstack noobs nonote nomtitle nonumber
eststo DESN
esttab DESN  using DescriptivasNUEVO.tex, main(mean) aux(sd)  label nostar unstack noobs nonote nomtitle nonumber replace 

estpost summarize sector_social_per justicia_seguridad_per infraestructura_per deuda_publica_per admon_estado_per closesnes degreecentr egivector prop_s nuevo_s, listwise
esttab, cells("obs mean sd min max") nomtitle nonumber
eststo DES
esttab DES  using Descriptivas.tex, cells("obs mean sd min max") nomtitle nonumber label replace 



clear all
set more off 
import delimited "/Users/j.agudelo/Library/CloudStorage/OneDrive-UniversidaddelosAndes/HEC/data/Main_dfP.csv"
br



reg sector_social_per prop_p c.degreecentr#i.nuevo_p , cluster(nombre_partido)
eststo SD1
reg sector_social_per c.egivector#i.nuevo_p prop_p, cluster(nombre_partido)
eststo SE2
reg sector_social_per c.closesnes#i.nuevo_p prop_p, cluster(nombre_partido)
eststo SA3
esttab S*  using SSOCIAL_PAR.tex, label replace 


reg justicia_seguridad_per prop_p c.degreecentr#i.nuevo_p , cluster(nombre_partido)
eststo JD1
reg justicia_seguridad_per c.egivector#i.nuevo_p prop_p, cluster(nombre_partido)
eststo JE2
reg justicia_seguridad_per c.closesnes#i.nuevo_p prop_p, cluster(nombre_partido)
eststo JA3
esttab J*  using JJUSTICIA_PAR.tex, label replace 


reg infraestructura_per prop_p c.degreecentr#i.nuevo_p , cluster(nombre_partido)
eststo ID1
reg infraestructura_per c.egivector#i.nuevo_p prop_p, cluster(nombre_partido)
eststo IE2
reg infraestructura_per c.closesnes#i.nuevo_p prop_p, cluster(nombre_partido)
eststo IA3
esttab I*  using INF_PAR.tex, label replace 


reg deuda_publica_per prop_p c.degreecentr#i.nuevo_p , cluster(nombre_partido)
eststo DD1
reg deuda_publica_per c.egivector#i.nuevo_p prop_p, cluster(nombre_partido)
eststo DE2
reg deuda_publica_per c.closesnes#i.nuevo_p prop_p, cluster(nombre_partido)
eststo DA3
esttab D*  using DEU_PAR.tex, label replace 


reg admon_estado_per prop_p c.degreecentr#i.nuevo_p, cluster(nombre_partido)
eststo AD1
reg admon_estado_per c.egivector#i.nuevo_p prop_p, cluster(nombre_partido)
eststo AE2
reg admon_estado_per c.closesnes#i.nuevo_p prop_p, cluster(nombre_partido)
eststo AA3
esttab A*  using ADMIN_PAR.tex, label replace 

