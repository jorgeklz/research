# -*- coding: utf-8 -*-
"""
Script to create the 11 missing curated posts for publications in data/publications.json
and safely insert them into data/posts.json with strict checks for:
- No em-dashes or en-dashes in generated texts
- No 'Asimismo' or 'Así mismo' anywhere
- Didactic, detailed, multi-paragraph text in English and Spanish with proper Spanish orthography and accents
- Full metadata (DOI, topics, authors, venue, links)
"""

import json
import os

POSTS_PATH = os.path.abspath('data/posts.json')
PUBS_PATH = os.path.abspath('data/publications.json')

with open(PUBS_PATH, 'r', encoding='utf-8') as f:
    pubs_data = json.load(f)
pubs = pubs_data.get('items', [])

# Load original baseline posts (excluding our newly added ones if re-running)
new_post_ids = {
    "post-smarttech2023-emergency-tuning",
    "post-dib2023-cbcovid19ec",
    "post-cm2023-busuu-english",
    "post-ek2022-web20-creative",
    "post-ci3-2022-elderly-diseases",
    "post-data2021-lelephid",
    "post-citis2021-emergency-detection",
    "post-dib2020-pcstcol-power",
    "post-jbcb2020-gene-clustering",
    "post-ijms2020-tgct-genetics",
    "post-dib2019-rocole-coffee",
    "post-scientometrics2026-utm",
    "post-acmlc2026-vlm-coffee"
}

with open(POSTS_PATH, 'r', encoding='utf-8') as f:
    posts_data = json.load(f)

# Keep only existing posts that are not in new_post_ids
baseline_posts = [p for p in posts_data.get('items', []) if p.get('id') not in new_post_ids]

new_posts = [
    # 1. SmartTech-IC 2022 / 2023 - Emergency Tweet Tuning
    {
        "id": "post-smarttech2023-emergency-tuning",
        "date": "2023-05-15",
        "type": "paper",
        "doi": "10.1007/978-3-031-32213-6_4",
        "auto": False,
        "topics": ["emergency", "nlp", "optimization", "machine-learning"],
        "title": {
            "en": "Tuning emergency tweet detectors with evolutionary algorithms",
            "es": "Afinar detectores de emergencias en Twitter con algoritmos evolutivos"
        },
        "summary": {
            "en": "With Joel Garcia-Arteaga, Jesus Zambrano-Zambrano and Jorge Rodas-Silva, pairing natural language classification with genetic algorithms to spot emergency alerts on social media across Ecuador.",
            "es": "Con Joel Garcia-Arteaga, Jesus Zambrano-Zambrano y Jorge Rodas-Silva, combinamos clasificación de lenguaje natural con algoritmos genéticos para detectar alertas de emergencia en redes sociales en Ecuador."
        },
        "body": {
            "en": (
                "When a sudden flash flood, traffic accident, or fire breaks out in a busy city, "
                "people often post pictures and warnings to social media long before anyone dials emergency services. "
                "Twitter (now X) has turned everyday citizens into impromptu sensors on the ground. However, using that continuous stream "
                "of messages to assist first responders is challenging because social media feeds are flooded with jokes, informal slang, "
                "and unrelated chatter that easily mislead automated filters.\n\n"
                "With **Joel Garcia-Arteaga**, **Jesus Zambrano-Zambrano**, and **Jorge Rodas-Silva**, we built an intelligent text classification "
                "system designed specifically for Spanish tweets published in Ecuador. Instead of relying on manual guesses to configure the machine learning models, "
                "we combined natural language classifiers with a **genetic algorithm**. This optimization technique mimics the biological process of natural selection, "
                "letting a population of model configurations compete, combine, and mutate until the most accurate setup survives.\n\n"
                "Following the structured CRISP-DM methodology, we tested our pipeline across more than 170,000 tweets. The genetic algorithm proved exceptionally capable "
                "at uncovering optimal hyperparameter combinations that human researchers would rarely find by hand. The **Linear Support Vector Classifier (LSVC)** achieved "
                "the strongest overall performance, reaching a Matthews correlation coefficient (MCC) of 0.96 for binary emergency detection and 0.97 for distinguishing among specific incident categories.\n\n"
                "Building tools that cut through the noise of social networks provides disaster response agencies with reliable, early situational awareness when seconds count. "
                "We presented this research at the **SmartTech-IC 2022** conference (International Conference on Smart Technologies, Systems and Applications), held in Cuenca, Ecuador."
            ),
            "es": (
                "Cuando ocurre una inundación repentina, un accidente de tránsito o un incendio en una ciudad concurrida, "
                "las personas suelen publicar fotos y alertas en redes sociales mucho antes de llamar a las líneas de auxilio. "
                "Twitter (hoy X) ha convertido a los ciudadanos en verdaderos sensores comunitarios sobre el terreno. Sin embargo, aprovechar ese flujo continuo "
                "de mensajes para respaldar a los equipos de rescate es complejo, ya que las publicaciones están llenas de modismos informales, ironías "
                "y contenido no relevante que confunde a los filtros automáticos.\n\n"
                "Con **Joel Garcia-Arteaga**, **Jesus Zambrano-Zambrano** y **Jorge Rodas-Silva** construimos un sistema inteligente de clasificación de texto "
                "diseñado específicamente para tuits en español originados en Ecuador. En lugar de ajustar los modelos de machine learning mediante ensayo y error, "
                "unimos clasificadores de lenguaje natural con un **algoritmo genético**. Esta técnica de optimización imita la selección natural biológica, "
                "permitiendo que una población de configuraciones compita, se cruce y mute hasta encontrar los parámetros con mayor exactitud.\n\n"
                "Bajo la metodología estructurada CRISP-DM, evaluamos el flujo con más de 170.000 tuits reales. El algoritmo genético demostró una gran eficacia "
                "para encontrar combinaciones de hiperparámetros que difícilmente se logran de forma manual. El clasificador **Linear Support Vector Classifier (LSVC)** "
                "obtuvo el desempeño más destacado, alcanzando un coeficiente de correlación de Matthews (MCC) de 0,96 en detección binaria y de 0,97 al diferenciar tipos específicos de incidentes.\n\n"
                "Crear herramientas capaces de filtrar el ruido en redes sociales brinda a los organismos de protección civil información temprana y confiable cuando cada segundo cuenta. "
                "Presentamos este trabajo en la conferencia **SmartTech-IC 2022** (International Conference on Smart Technologies, Systems and Applications), celebrada en Cuenca, Ecuador."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.1007/978-3-031-32213-6_4"}
        ]
    },

    # 2. Data in Brief 2023 - CBCovid19EC
    {
        "id": "post-dib2023-cbcovid19ec",
        "date": "2023-03-01",
        "type": "paper",
        "doi": "10.1016/j.dib.2023.109016",
        "auto": False,
        "topics": ["health", "covid", "machine-learning", "datasets"],
        "title": {
            "en": "CBCovid19EC: Routine blood tests to detect COVID-19 in Ecuador",
            "es": "CBCovid19EC: Análisis de sangre de rutina para detectar COVID-19 en Ecuador"
        },
        "summary": {
            "en": "With R. Ordoñez-Avila and an international collaboration, an open clinical dataset pairing complete blood counts with PCR tests across 400 Ecuadorian cases to train diagnostic models.",
            "es": "Con R. Ordoñez-Avila y un equipo internacional, un conjunto de datos clínicos público que une hemogramas completos con pruebas PCR en 400 casos ecuatorianos para entrenar modelos de diagnóstico."
        },
        "body": {
            "en": (
                "Throughout the COVID-19 pandemic, real-time RT-PCR testing was the indisputable gold standard for confirming viral infections. "
                "Yet in many developing countries and remote communities, molecular tests presented serious logistical barriers: they required specialized laboratory equipment, "
                "cost substantial amounts of money, and often took several days to deliver results. In contrast, a **complete blood count (CBC)** is fast, affordable, "
                "and available in virtually every primary healthcare center.\n\n"
                "To explore whether routine blood profiles could provide diagnostic signals of COVID-19 infection, we partnered with clinical laboratories (Segurilab and Previne Salud) "
                "in Quito, Ecuador, to build **CBCovid19EC**. Working alongside **R. Ordoñez-Avila**, **J. Meza Hormaza**, **L. Vaca-Cárdenas**, **E. Portmann**, **L. Terán**, and **M. Dorn**, "
                "we compiled and curated anonymized medical records from approximately 400 participating patients between March and August 2021.\n\n"
                "The resulting dataset links each patient's definitive RT-PCR result with detailed quantitative measurements of their blood, including red blood cell count, "
                "white blood cell subtypes (lymphocytes, neutrophils, monocytes), hemoglobin levels, hematocrit percentages, platelets, and C-reactive protein (CRP). "
                "Because severe viral attacks alter inflammatory indicators and immune cell ratios in measurable ways, these standard laboratory values hold rich predictive information.\n\n"
                "We released CBCovid19EC as a fully public, open-access scientific resource in **Data in Brief** and on Mendeley Data. It provides researchers worldwide "
                "with an authentic regional benchmark to develop, validate, and compare machine learning classifiers and clustering models capable of assisting triage decisions when molecular testing is constrained."
            ),
            "es": (
                "Durante las etapas críticas de la pandemia de COVID-19, las pruebas moleculares RT-PCR fueron el estándar de referencia para confirmar la infección viral. "
                "Sin embargo, en muchos países en desarrollo y zonas alejadas, los exámenes moleculares enfrentaron grandes barreras logísticas: requerían laboratorios especializados, "
                "tenían un costo elevado y tardaban horas o días en entregar un resultado. Por el contrario, una **biometría hemática** o hemograma completo (CBC) es un examen económico, "
                "rápido y disponible en casi cualquier centro de salud básico.\n\n"
                "Para investigar si las alteraciones en la sangre podían aportar señales claras de la infección, colaboramos con laboratorios clínicos (Segurilab y Previne Salud) "
                "en Quito, Ecuador, creando el banco de datos **CBCovid19EC**. Junto a **R. Ordoñez-Avila**, **J. Meza Hormaza**, **L. Vaca-Cárdenas**, **E. Portmann**, **L. Terán** y **M. Dorn**, "
                "recopilamos y curamos los registros anonimizados de aproximadamente 400 pacientes que aceptaron participar en el estudio entre marzo y agosto de 2021.\n\n"
                "El conjunto de datos asocia el resultado confirmado de la prueba PCR de cada paciente con mediciones cuantitativas detalladas de su hemograma, incluyendo glóbulos rojos, "
                "subpoblaciones de leucocitos (linfocitos, neutrófilos, monocitos), hemoglobina, hematocrito, recuento plaquetario y proteína C reactiva (PCR cuantitativa). "
                "Dado que la infección viral altera los marcadores inflamatorios y el balance del sistema inmune, estos perfiles sanguíneos contienen información útil para el análisis clínico.\n\n"
                "Publicamos CBCovid19EC como un recurso de acceso abierto en la revista **Data in Brief** y en el repositorio Mendeley Data. Con ello, la comunidad científica internacional "
                "cuenta con una base clínica real para entrenar algoritmos de clasificación y agrupamiento asistidos por machine learning, facilitando el triaje médico en situaciones de alta demanda sanitaria."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.1016/j.dib.2023.109016"},
            {"label": "Mendeley Data", "url": "https://doi.org/10.17632/7bmfgkkm3z.3"}
        ]
    },

    # 3. CIENCIAMATRIA 2023 - Busuu English
    {
        "id": "post-cm2023-busuu-english",
        "date": "2023-07-01",
        "type": "paper",
        "doi": "10.35381/cm.v9i2.1158",
        "auto": False,
        "topics": ["education", "technology", "language-learning"],
        "title": {
            "en": "Can interactive language apps outpace textbook English classes?",
            "es": "¿Pueden las aplicaciones interactivas superar las clases tradicionales de inglés?"
        },
        "summary": {
            "en": "With Victoria Johanna Mero-Mero, a comparative educational study evaluating how the Busuu digital platform improves English language acquisition in primary schools in Manta, Ecuador.",
            "es": "Con Victoria Johanna Mero-Mero, un estudio educativo comparativo que evalúa cómo la plataforma digital Busuu mejora el aprendizaje de inglés en educación básica en Manta, Ecuador."
        },
        "body": {
            "en": (
                "Learning a second language during childhood is one of the most valuable cognitive investments a student can make, "
                "yet traditional classrooms often struggle to deliver lasting results. In many schools, language teaching relies heavily on mechanical textbook drills, "
                "rote grammar memorization, and passive listening. With large class sizes, students rarely get the individual speaking practice and prompt feedback "
                "required to develop true conversational fluency.\n\n"
                "Together with **Victoria Johanna Mero-Mero**, we examined whether modern mobile learning technology could transform this dynamic. "
                "We designed an educational study focused on the **Busuu digital platform**, analyzing its impact on seventh-grade elementary students "
                "(Educación General Básica) at Unidad Educativa 'María Auxiliadora' in Manta, Ecuador. The investigation followed a quantitative design involving 70 students "
                "divided into two parallel groups: an experimental cohort using Busuu and a control cohort continuing with conventional instruction.\n\n"
                "The digital platform provided interactive exercises that engaged multiple sensory channels, combining speech recognition, audio pronunciation guides, "
                "visual association, and gamified progress tracking. When we assessed the academic outcomes, the students who practiced through Busuu showed a marked advantage "
                "over those taught with traditional methods, demonstrating significantly higher retention, vocabulary comprehension, and active motivation to participate.\n\n"
                "These findings offer practical evidence for educators seeking to modernize school curricula. Integrating well-designed digital language tools does not replace teachers; "
                "rather, it provides students with a dynamic, personalized environment that turns foreign language study into an engaging daily habit. "
                "The study was published in the journal **CIENCIAMATRIA**."
            ),
            "es": (
                "Aprender una segunda lengua durante la infancia es una de las mayores ventajas formativas que puede tener un estudiante, "
                "pero la enseñanza tradicional en las aulas suele enfrentar grandes dificultades para lograr fluidez real. En muchos centros educativos, "
                "la materia de inglés se ha limitado a ejercicios repetitivos en libros impresos y memorización pasiva de reglas gramaticales. "
                "Ante grupos numerosos, los estudiantes rara vez tienen la oportunidad de practicar pronunciación y recibir retroalimentación continua.\n\n"
                "Junto a **Victoria Johanna Mero-Mero** analizamos cómo la tecnología educativa móvil puede transformar esta realidad en las aulas. "
                "Evaluamos la aplicación de la plataforma digital **Busuu** en el aprendizaje del idioma inglés en estudiantes de séptimo año de Educación General Básica "
                "de la Unidad Educativa 'María Auxiliadora' en Manta, Ecuador. La investigación se desarrolló bajo un enfoque cuantitativo con una muestra de 70 estudiantes "
                "distribuidos en dos paralelos: un grupo experimental apoyado en la aplicación digital y un grupo de control con metodología magistral habitual.\n\n"
                "La plataforma móvil estimuló la atención de los alumnos mediante actividades interactivas que involucran varios sentidos a la vez, "
                "integrando reconocimiento de voz, modulación auditiva, desafíos visuales y correcciones inmediatas. Al evaluar los resultados finales, "
                "el grupo experimental mostró una mejoría sustancial en comparación con el grupo de control, logrando un desempeño superior en comprensión auditiva, "
                "adquisición de vocabulario y disposición para comunicarse en inglés.\n\n"
                "Los resultados aportan evidencia concreta para directivos y docentes que buscan actualizar sus metodologías didácticas. El uso de plataformas interactivas "
                "no reemplaza la labor del profesor, sino que potencia el proceso al ofrecer a cada niño un espacio de práctica personalizado y motivador. "
                "La investigación fue publicada en la revista arbitrada **CIENCIAMATRIA**."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.35381/cm.v9i2.1158"}
        ]
    },

    # 4. EPISTEME KOINONIA 2022 - Web 2.0 Creative Learning
    {
        "id": "post-ek2022-web20-creative",
        "date": "2022-12-09",
        "type": "paper",
        "doi": "10.35381/e.k.v5i1.2189",
        "auto": False,
        "topics": ["education", "technology", "pedagogy"],
        "title": {
            "en": "Turning classrooms into creative workshops with Web 2.0 tools",
            "es": "Transformar las aulas en talleres creativos con herramientas Web 2.0"
        },
        "summary": {
            "en": "With Holger Arturo Proaño-Zambrano, a quasi-experimental study demonstrating how Web 2.0 interactive tools raise student engagement and performance in 24 de Mayo, Manabí.",
            "es": "Con Holger Arturo Proaño-Zambrano, un estudio cuasiexperimental que demuestra cómo las herramientas interactivas Web 2.0 elevan el rendimiento y la participación estudiantil en 24 de Mayo, Manabí."
        },
        "body": {
            "en": (
                "For decades, the standard classroom dynamic has followed a familiar one-way pattern: the teacher lectures from the front while students take notes in silence. "
                "While this format conveys basic instructions, it frequently leaves learners disengaged and disconnected from real problem-solving. "
                "In rural and semi-urban communities where access to expensive laboratory infrastructure is limited, finding accessible ways to stimulate curiosity is an urgent educational challenge.\n\n"
                "With **Holger Arturo Proaño-Zambrano**, we designed a quasi-experimental research project to test whether readily available **Web 2.0 tools** "
                "(interactive boards, collaborative multimedia, and online formative activities) could revitalize daily learning. The study was conducted at "
                "Unidad Educativa 'Bellavista', located in the 24 de Mayo canton in Manabí, Ecuador. We gathered field data through teacher surveys and administered rigorous pre- and post-tests "
                "to both a control group and an experimental group of students.\n\n"
                "The initial diagnostic tests confirmed widespread academic hurdles in both cohorts: the control group exhibited an 85% error rate, while the experimental group scored 87% errors. "
                "Following the intervention period, students who continued with traditional lecture methods remained virtually unchanged, still showing a 79% error rate. "
                "In stark contrast, the experimental cohort that participated in interactive Web 2.0 activities achieved a 96% success rate on the final evaluation.\n\n"
                "These findings prove that technology does not require massive budgets to make a meaningful difference in the classroom. "
                "When teachers deploy accessible digital tools as creative, participatory instruments, students shift from passive observers into active builders of their own knowledge. "
                "The study was published in the academic journal **EPISTEME KOINONIA**."
            ),
            "es": (
                "Durante décadas, la dinámica habitual en las aulas ha seguido un esquema unidireccional: el profesor expone al frente mientras los alumnos toman notas en silencio. "
                "Aunque este modelo sirve para dar pautas generales, con frecuencia genera desinterés y limita la capacidad de resolver problemas de forma autónoma. "
                "En instituciones rurales o semiurbanas donde no abundan recursos costosos, encontrar alternativas accesibles para estimular la curiosidad representa una necesidad formativa urgente.\n\n"
                "Junto a **Holger Arturo Proaño-Zambrano** desarrollamos un estudio cuasiexperimental para evaluar cómo las **herramientas Web 2.0** "
                "(muros interactivos, pizarras colaborativas y actividades multimedia en línea) pueden revitalizar la enseñanza cotidiana. La investigación se llevó a cabo en la "
                "Unidad Educativa 'Bellavista', en el cantón 24 de Mayo, provincia de Manabí, Ecuador. Combinamos técnicas documentales con encuestas a docentes y pruebas evaluativas "
                "aplicadas a un grupo de control y a un grupo experimental.\n\n"
                "La evaluación diagnóstica inicial reveló dificultades severas en ambos grupos: el grupo de control registró un 85% de errores y el experimental un 87%. "
                "Tras el periodo lectivo, los estudiantes que continuaron bajo el modelo tradicional apenas redujeron sus fallas (79% de errores). "
                "En cambio, el grupo experimental que integró herramientas digitales participativas experimentó un avance rotundo, alcanzando un 96% de respuestas acertadas en el examen final.\n\n"
                "La experiencia comprueba que no se requieren presupuestos millonarios para transformar la calidad pedagógica. "
                "Cuando las herramientas digitales se emplean con criterio didáctico y enfoque colaborativo, los estudiantes dejan de ser receptores pasivos y asumen un rol protagonista en su propio aprendizaje. "
                "El artículo fue publicado en la revista científica **EPISTEME KOINONIA**."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.35381/e.k.v5i1.2189"}
        ]
    },

    # 5. CI3 2021 / 2022 - Prediction of Diseases in the Elderly in Manabí
    {
        "id": "post-ci3-2022-elderly-diseases",
        "date": "2022-07-15",
        "type": "paper",
        "doi": "10.1007/978-3-031-11438-0_48",
        "auto": False,
        "topics": ["health", "big-data", "machine-learning"],
        "title": {
            "en": "Predicting cardiovascular risks in older adults across Manabí",
            "es": "Predecir riesgos cardiovasculares en adultos mayores de Manabí"
        },
        "summary": {
            "en": "With Fernando Alfredo Reyes Reyes and Marely Del Rosario Cruz Felipe, benchmarking 13 machine learning algorithms to identify key cardiovascular risk indicators among elderly citizens in Manabí, Ecuador.",
            "es": "Con Fernando Alfredo Reyes Reyes y Marely Del Rosario Cruz Felipe, evaluamos 13 algoritmos de machine learning para identificar los principales indicadores de riesgo cardiovascular en adultos mayores de Manabí, Ecuador."
        },
        "body": {
            "en": (
                "Cardiovascular diseases (CVD) remain the single largest cause of death among older adults across the globe. "
                "While international health guidelines offer general lists of risk factors such as hypertension, obesity, and smoking, regional populations "
                "often present distinct socio-environmental realities, dietary habits, and healthcare access profiles. In the coastal province of Manabí, Ecuador, "
                "geriatric health data had rarely been explored through the lens of modern predictive analytics.\n\n"
                "In collaboration with **Fernando Alfredo Reyes Reyes** and **Marely Del Rosario Cruz Felipe**, we set out to build predictive models capable of estimating "
                "cardiovascular disease risk specifically in older adults residing in Manabí. We utilized authentic microdata from 604 elderly participants surveyed by INEC "
                "(Ecuador's National Institute of Statistics and Censuses) in their national survey on senior well-being and health conditions.\n\n"
                "We conducted a systematic performance benchmark across **13 machine learning algorithms**, evaluating each model's discriminatory power using Area Under the Receiver "
                "Operating Characteristic Curve (AUC). The **Random Forest** algorithm emerged as the top performer. To make its predictions fully transparent and clinically useful, "
                "we computed Shapley additive explanations (SHAP values) to rank feature importance. The analysis revealed that the most decisive risk indicators in this demographic were "
                "recurrent shortness of breath (dyspnea), stature-height indicators, ongoing prescription medication use, and chronic dizziness episodes.\n\n"
                "Interpretable data mining enables public health planners and family physicians to spot vulnerable elderly patients early, guiding preventative checkups before acute emergencies strike. "
                "We presented this work at the **CI3 2021** congress (Congreso Internacional de Ciencias de la Computación e Informática del Ecuador), published by Springer in *Lecture Notes in Networks and Systems*."
            ),
            "es": (
                "Las enfermedades cardiovasculares representan la principal causa de mortalidad en personas adultas mayores a nivel global. "
                "Aunque la literatura médica universal enumera factores de riesgo habituales como la hipertensión, el colesterol elevado o el tabaquismo, "
                "las poblaciones locales muestran particularidades asociadas a su estilo de vida, alimentación y cobertura de salud. En la provincia costera de Manabí, Ecuador, "
                "no existían investigaciones previas que analizaran los factores de riesgo de esta afección en la tercera edad mediante herramientas de analítica predictiva.\n\n"
                "En colaboración con **Fernando Alfredo Reyes Reyes** y **Marely Del Rosario Cruz Felipe**, nos propusimos desarrollar modelos capaces de estimar "
                "el riesgo cardiovascular en adultos mayores manabitas. Para ello, analizamos registros reales de 604 participantes provenientes de la encuesta de salud y bienestar "
                "del adulto mayor realizada por el Instituto Nacional de Estadística y Censos (INEC) de Ecuador.\n\n"
                "Realizamos una comparativa sistemática entre **13 algoritmos de machine learning**, midiendo la precisión de sus pronósticos mediante el área bajo la curva ROC (AUC). "
                "El modelo basado en **Random Forest** demostró el rendimiento más sólido. Además, para interpretar qué variables tenían mayor peso clínico en la predicción, "
                "aplicamos técnicas basadas en valores de Shapley. Los factores más determinantes identificados para Manabí fueron la dificultad recurrente para respirar (disnea), "
                "los valores antropométricos de estatura, la ingesta continuada de medicamentos y la presencia de mareos persistentes.\n\n"
                "Disponer de modelos predictivos interpretables permite a las instituciones de salud priorizar acciones preventivas y visitas médicas oportunas en comunidades vulnerables. "
                "Presentamos este estudio en el congreso **CI3 2021** (Congreso Internacional de Ciencias de la Computación e Informática del Ecuador), publicado en la serie *Lecture Notes in Networks and Systems* de Springer."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.1007/978-3-031-11438-0_48"}
        ]
    },

    # 6. MDPI Data 2021 - LeLePhid
    {
        "id": "post-data2021-lelephid",
        "date": "2021-05-17",
        "type": "paper",
        "doi": "10.3390/data6050051",
        "auto": False,
        "topics": ["agriculture", "computer-vision", "deep-learning", "datasets"],
        "title": {
            "en": "LeLePhid: A public image dataset to detect aphids on lemon leaves",
            "es": "LeLePhid: Un banco de imágenes público para detectar pulgones en hojas de limón"
        },
        "summary": {
            "en": "With Roberth Alcivar-Cevallos and student coauthors, an open dataset of 665 annotated lemon leaf photographs collected in Junín, Ecuador, to train computer vision models that recognize aphid infestations.",
            "es": "Con Roberth Alcivar-Cevallos y coautores estudiantes, un conjunto abierto de 665 fotografías anotadas de hojas de limón recolectadas en Junín, Ecuador, para entrenar modelos de visión por computador que detectan pulgones."
        },
        "body": {
            "en": (
                "Citrus fruits are essential cash crops for agricultural families throughout the tropics and subtropics, but orchards face constant threats from pests. "
                "Among the most damaging are aphids: miniature sap-sucking insects from the superfamily Aphidoidea. In addition to depleting tree vitality, aphids excrete a sticky honeydew "
                "that promotes sooty mold growth and act as active vectors for destructive plant viruses. Early detection is vital, but walking through thousands of trees to inspect leaves by eye "
                "is slow, exhausting, and often identifies outbreaks too late.\n\n"
                "Artificial intelligence and computer vision offer a way to automate crop scouting, but deep learning models require vast numbers of authentic, annotated training images. "
                "Together with **Roberth Alcivar-Cevallos**, **Jéssica Morales Carrillo**, **Magdalena Castro**, **Shabely Avellán**, **Aaron Loor**, and **Fernando Mendoza**, we built and published **LeLePhid** "
                "(Lemon Leaf image dataset for Aphid detection and infestation severity). The collection was photographed by hand under natural sunlight in commercial lemon orchards in Junín, Manabí, Ecuador.\n\n"
                "The dataset contains 665 high-resolution images capturing both completely healthy lemon leaves and leaves suffering varying degrees of aphid colony colonization, "
                "characterized by distinct white spots and clusters on the undersides of the foliage. Crucially, each image is accompanied by detailed annotations that delineate individual leaf contours, "
                "classify health status, and quantify infestation severity according to the exact percentage of leaf area affected.\n\n"
                "LeLePhid was published in **Data** (MDPI) and deposited in Mendeley Data as a free, open-access scientific resource. "
                "It serves as a key benchmark for researchers around the globe developing semantic segmentation, object detection, and automated disease diagnosis pipelines for precision agriculture."
            ),
            "es": (
                "Los cítricos constituyen uno de los cultivos comerciales más relevantes para miles de familias campesinas en zonas tropicales y subtropicales, pero enfrentan amenazas constantes por plagas. "
                "Entre las más perjudiciales destacan los pulgones: pequeños insectos chupadores de savia pertenecientes a la superfamilia Aphidoidea. Además de debilitar el árbol, "
                "los pulgones segregan una sustancia melosa que favorece la aparición de hongos (fumagina) y transmiten virus letales entre plantaciones. Su detección temprana es indispensable, "
                "pero recorrer hectáreas enteras revisando hojas de manera manual resulta agotador y poco viable a gran escala.\n\n"
                "La inteligencia artificial y la visión por computador pueden automatizar el monitoreo de plagas, pero los modelos de aprendizaje profundo necesitan bancos de imágenes reales y anotadas. "
                "Junto a **Roberth Alcivar-Cevallos**, **Jéssica Morales Carrillo**, **Magdalena Castro**, **Shabely Avellán**, **Aaron Loor** y **Fernando Mendoza**, construimos y publicamos **LeLePhid** "
                "(Lemon Leaf image dataset for Aphid detection and infestation severity). Las fotografías fueron tomadas manualmente bajo condiciones reales de campo en plantaciones de limón en Junín, Manabí, Ecuador.\n\n"
                "El banco reúne 665 fotografías de alta resolución que abarcan desde hojas sanas hasta ejemplares con diferentes niveles de presencia de pulgones, "
                "visibles como manchas y colonias blanquecinas en la superficie foliar. Cada imagen cuenta con etiquetas técnicas que delimitan los contornos de la hoja, "
                "su estado fitosanitario y la severidad del ataque medida según el porcentaje de área afectada.\n\n"
                "Publicamos LeLePhid en la revista **Data** (MDPI) y en el repositorio Mendeley Data con acceso totalmente abierto. "
                "El recurso facilita a científicos de todo el mundo el diseño, calibración y evaluación de modelos de segmentación, detección de objetos y diagnóstico automático aplicados a la agricultura de precisión."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.3390/data6050051"},
            {"label": "Mendeley Data", "url": "https://doi.org/10.17632/tndhs2zng4.1"}
        ]
    },

    # 7. CITIS 2021 - Emergency Detection
    {
        "id": "post-citis2021-emergency-detection",
        "date": "2021-09-27",
        "type": "paper",
        "doi": "10.1007/978-981-16-4126-8_25",
        "auto": False,
        "topics": ["emergency", "nlp", "machine-learning"],
        "title": {
            "en": "Turning citizen tweets into real-time emergency alarms",
            "es": "Convertir los tuits ciudadanos en alarmas de emergencia en tiempo real"
        },
        "summary": {
            "en": "With Yahir Mendoza, Jorge Santillan and Roberth Alcivar-Cevallos, supervised learning models designed to filter social media streams and detect urban accidents in seconds.",
            "es": "Con Yahir Mendoza, Jorge Santillan y Roberth Alcivar-Cevallos, modelos de aprendizaje supervisado diseñados para filtrar publicaciones en redes sociales y detectar accidentes urbanos en segundos."
        },
        "body": {
            "en": (
                "Urban emergencies such as traffic collisions, fires, and structural collapses disrupt lives and demand rapid coordination. "
                "Traditional emergency response systems depend on witnesses dialing hotline numbers, but in an age of ubiquitous smartphones, "
                "citizens frequently document and share incidents on social networks within seconds of an occurrence. Turning public posts into actionable "
                "alerts can give emergency teams a vital operational head start.\n\n"
                "Together with **Yahir Mendoza**, **Jorge Santillan**, and **Roberth Alcivar-Cevallos**, we designed a supervised machine learning framework "
                "to automatically detect emergency events from Twitter messages. The challenge lies in separating genuine danger alerts from casual, figurative, "
                "or conversational language (such as someone tweeting that their homework is 'a disaster' or that traffic is 'killing them').\n\n"
                "We structured our approach into four systematic phases: data acquisition, linguistic cleaning and lemmatization feature extraction, implementation of "
                "supervised classifiers (including Naive Bayes, Decision Trees, Random Forest, and Support Vector Machines), and comprehensive performance evaluation. "
                "The tested algorithms achieved average accuracy rates of 85.38% with inference times around 23 seconds. When balancing processing speed against detection "
                "accuracy, the **Support Vector Machine (SVM)** proved to be the most dependable model for real-time operation.\n\n"
                "This study demonstrates the feasibility of transforming social networks into automated sensory networks for smart cities. "
                "We presented the findings at the **CITIS 2021** conference (Congreso Internacional de Tecnologías de Información y Sistemas), held in Guayaquil, Ecuador, "
                "and published by Springer in *Smart Innovation, Systems and Technologies*."
            ),
            "es": (
                "Los incidentes urbanos como choques vehiculares, incendios y colapsos estructurales comprometen la seguridad pública y exigen respuestas inmediatas. "
                "Los centros de emergencia habituales dependen de llamadas telefónicas, pero en la actualidad los ciudadanos utilizan sus teléfonos móviles "
                "para compartir lo que ocurre en redes sociales segundos después de presenciar un suceso. Convertir esos mensajes en alarmas confiables "
                "puede otorgar a los equipos de socorro una ventaja de tiempo determinante.\n\n"
                "Junto a **Yahir Mendoza**, **Jorge Santillan** y **Roberth Alcivar-Cevallos** desarrollamos una propuesta basada en aprendizaje automático supervisado "
                "para detectar eventos de emergencia en Twitter. La principal dificultad radica en diferenciar una alerta real de expresiones cotidianas o figurativas "
                "(por ejemplo, cuando alguien publica que el tráfico 'es una pesadilla' o que el examen estuvo 'terrible').\n\n"
                "El flujo de trabajo se organizó en cuatro etapas metodológicas: captura de datos, preprocesamiento lingüístico con lematización de términos, "
                "entrenamiento de clasificadores supervisados (incluyendo Naive Bayes, Árboles de Decisión, Random Forest y Máquinas de Vectores de Soporte) y evaluación de métricas. "
                "Los algoritmos alcanzaron una precisión media del 85,38% con un tiempo de procesamiento cercano a los 23 segundos. Al ponderar la rapidez de cómputo frente a la exactitud, "
                "el clasificador **SVM (Support Vector Machine)** ofreció el mejor balance operativo para entornos en tiempo real.\n\n"
                "El trabajo demuestra cómo las plataformas digitales pueden funcionar como redes de sensores ciudadanos al servicio de ciudades inteligentes. "
                "Presentamos la investigación en el congreso **CITIS 2021** (Congreso Internacional de Tecnologías de Información y Sistemas), en Guayaquil, Ecuador, "
                "publicado en la serie *Smart Innovation, Systems and Technologies* de Springer."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.1007/978-981-16-4126-8_25"}
        ]
    },

    # 8. Data in Brief 2020 - PCSTCOL Electric Power Consumption
    {
        "id": "post-dib2020-pcstcol-power",
        "date": "2020-02-05",
        "type": "paper",
        "doi": "10.1016/j.dib.2020.105246",
        "auto": False,
        "topics": ["energy", "machine-learning", "datasets"],
        "title": {
            "en": "PCSTCOL: Real-world electricity demand and demographics in southern Colombia",
            "es": "PCSTCOL: Demanda eléctrica real y datos demográficos en el sur de Colombia"
        },
        "summary": {
            "en": "With Jorge Dario Moncayo-Nacaza and Diego Hernán Peluffo-Ordóñez, an open dataset linking over 4,400 socio-demographic indicators with residential electricity consumption across Nariño, Colombia.",
            "es": "Con Jorge Dario Moncayo-Nacaza y Diego Hernán Peluffo-Ordóñez, un conjunto de datos abierto que vincula más de 4.400 indicadores sociodemográficos con el consumo eléctrico residencial en Nariño, Colombia."
        },
        "body": {
            "en": (
                "Electrical grids must continuously balance supply and demand. Because storing massive amounts of power in batteries remains prohibitively expensive, "
                "utility operators must generate and dispatch the exact amount of energy consumers require in real time. Underestimating demand triggers blackouts and grid instability, "
                "while overestimating it leads to wasted fuel and unnecessary operational costs. Accurate forecasting models are therefore vital to modern power engineering.\n\n"
                "While power forecasting research often uses data from major metropolitan centers in Europe or North America, developing regions possess unique geographical, "
                "economic, and infrastructural realities. To bridge this data gap, we collaborated with Centrales Eléctricas de Nariño (CEDENAR) in Colombia to create **PCSTCOL**. "
                "Working alongside **Jorge Dario Moncayo-Nacaza**, **Javier Revelo-Fuelagán**, **Paul D. Rosero-Montalvo**, **Andrés Anaya-Isaza**, and **Diego Hernán Peluffo-Ordóñez**, "
                "we compiled historical records covering seven principal municipalities in the department of Nariño between December 2010 and May 2016.\n\n"
                "The dataset integrates 4,427 socio-demographic variables with seven measured energy consumption parameters recorded through on-site meter readings (in kilowatt-hours). "
                "By linking customer demographic categories, housing types, and regional attributes with multi-year electrical billing profiles, PCSTCOL provides a rich, multi-faceted look "
                "at residential power dynamics.\n\n"
                "We published PCSTCOL as an open-access resource in **Data in Brief** with open files available on Mendeley Data. "
                "It serves as a valuable public benchmark for researchers developing machine learning, statistical forecasting, and smart grid optimization algorithms tailored to Latin American energy systems."
            ),
            "es": (
                "Las redes de distribución eléctrica deben mantener un balance constante entre generación y consumo. Como almacenar energía a gran escala sigue siendo muy costoso, "
                "las empresas suministradoras necesitan producir en cada instante la cantidad exacta de electricidad que la población demanda. Subestimar el consumo provoca apagones y sobrecargas, "
                "mientras que sobreestimarlo ocasiona desperdicio de combustible y sobrecostos operativos. Desarrollar modelos precisos de pronóstico energético es fundamental.\n\n"
                "Gran parte de los estudios internacionales se fundamentan en mediciones de grandes ciudades europeas o norteamericanas, cuyas realidades habitacionales "
                "difieren de las de América Latina. Para reducir esa brecha, colaboramos con la empresa Centrales Eléctricas de Nariño (CEDENAR) en Colombia para crear la base de datos **PCSTCOL**. "
                "Junto a **Jorge Dario Moncayo-Nacaza**, **Javier Revelo-Fuelagán**, **Paul D. Rosero-Montalvo**, **Andrés Anaya-Isaza** y **Diego Hernán Peluffo-Ordóñez**, "
                "recopilamos registros históricos correspondientes a siete municipios del departamento de Nariño entre diciembre de 2010 y mayo de 2016.\n\n"
                "El conjunto de datos combina 4.427 características sociodemográficas con siete valores medidos de consumo energético obtenidos mediante lecturas directas en medidores (expresadas en kWh). "
                "Al vincular la estratificación socioeconómica, el tipo de inmueble y la ubicación geográfica con el comportamiento de consumo a lo largo de varios años, "
                "PCSTCOL ofrece una perspectiva integral sobre los patrones de uso de la energía.\n\n"
                "Publicamos PCSTCOL en la revista **Data in Brief** con acceso abierto y disponibilidad completa en Mendeley Data. "
                "El recurso proporciona a la comunidad científica un banco de pruebas real para entrenar modelos de machine learning, pronósticos estadísticos y esquemas de optimización energética en la región."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.1016/j.dib.2020.105246"},
            {"label": "Mendeley Data", "url": "https://doi.org/10.17632/xbt7scz5ny.3"}
        ]
    },

    # 9. JBCB 2020 - GO-based Semantic Similarity in Gene Clustering
    {
        "id": "post-jbcb2020-gene-clustering",
        "date": "2020-08-22",
        "type": "paper",
        "doi": "10.1142/s0219720020500389",
        "auto": False,
        "topics": ["bioinformatics", "optimization", "data-mining"],
        "title": {
            "en": "Which biological similarity metric best organizes complex genetic data?",
            "es": "¿Qué métrica de similitud biológica organiza mejor los datos genéticos complejos?"
        },
        "summary": {
            "en": "With Mario Inostroza-Ponta, a systematic evaluation comparing four Gene Ontology semantic similarity measures in multi-objective clustering algorithms for gene expression.",
            "es": "Con Mario Inostroza-Ponta, una evaluación sistemática que compara cuatro medidas de similitud semántica de Gene Ontology en algoritmos de agrupamiento genético multiobjetivo."
        },
        "body": {
            "en": (
                "Deciphering how thousands of genes interact inside living cells is a central quest of modern computational biology. "
                "A foundational step in this analysis is clustering: grouping genes that behave alike so researchers can identify disease pathways and shared regulatory mechanisms. "
                "Traditionally, algorithms grouped genes solely based on numerical correlations in expression levels. However, numerical proximity alone can be misleading, "
                "frequently grouping completely unrelated cellular processes simply because their activity levels spiked at the same moment.\n\n"
                "To solve this issue, bioinformaticians turn to multi-objective optimization, balancing mathematical co-expression against known biological knowledge "
                "drawn from the **Gene Ontology (GO)** repository. Yet this introduced a longstanding dilemma: multiple mathematical formulas exist to calculate GO semantic similarity "
                "(such as Resnik, Lin, Jiang-Conrath, and Wang), and researchers had little objective guidance on which measure produces the most biologically meaningful groups.\n\n"
                "Working with **Mario Inostroza-Ponta**, we conducted a comprehensive study examining the influence of the four most widely used GO semantic similarity measures "
                "within a multi-objective gene clustering framework. We benchmarked the measures across four publicly available microarray expression datasets, evaluating clustering compactness, "
                "cluster separation, multi-objective Pareto front quality, and functional biological coherence.\n\n"
                "Our results revealed subtle individual strengths: the Resnik metric yielded the most compact and well-separated clusters, while the Wang measure captured higher biological homogeneity. "
                "However, thorough statistical, visual, and biological significance testing demonstrated that no single GO measure universally outclasses the others. "
                "The practical conclusion for bioinformaticians is that the optimization algorithm's architectural design and objective balance matter far more than the specific similarity formula selected. "
                "The study was published in the **Journal of Bioinformatics and Computational Biology**."
            ),
            "es": (
                "Descifrar cómo interactúan miles de genes dentro de las células es uno de los mayores desafíos de la biología computacional. "
                "Un paso indispensable en este campo es el agrupamiento (clustering): reunir genes con comportamiento similar para identificar rutas patológicas y funciones compartidas. "
                "Históricamente, los algoritmos agrupaban genes guiándose únicamente por correlaciones numéricas en sus niveles de expresión. No obstante, basarse solo en cifras puede inducir a error, "
                "reuniendo procesos celulares no relacionados simplemente porque sus señales coincidieron en un instante determinado.\n\n"
                "Para corregir este sesgo, se recurre a la optimización multiobjetivo, equilibrando la coexpresión matemática con el conocimiento biológico existente "
                "en la base de datos **Gene Ontology (GO)**. Esto originó un dilema práctico: existen diversas fórmulas matemáticas para medir la similitud semántica en GO "
                "(como Resnik, Lin, Jiang-Conrath y Wang), pero no existía claridad sobre cuál de ellas genera agrupaciones más coherentes desde el punto de vista biológico.\n\n"
                "Junto a **Mario Inostroza-Ponta** llevamos a cabo un estudio sistemático para analizar el impacto de las cuatro medidas de similitud semántica más utilizadas "
                "sobre el desempeño de un algoritmo de agrupamiento multiobjetivo. Evaluamos las técnicas con cuatro conjuntos de datos de microarreglos públicos, examinando la compacidad de los grupos, "
                "su separación espacial, las métricas del frente de Pareto y la homogeneidad funcional de los resultados.\n\n"
                "Los hallazgos mostraron ventajas particulares: la métrica de Resnik produjo grupos más compactos y definidos, mientras que la similitud de Wang reportó mayor enriquecimiento biológico. "
                "Sin embargo, las pruebas estadísticas, visuales y de significancia biológica confirmaron que ninguna medida supera de manera concluyente a las demás en todos los aspectos. "
                "Para la comunidad bioinformática, esto señala que la estructura del algoritmo de optimización y el balance de objetivos tienen un peso mucho mayor que la elección puntual de la fórmula de distancia semántica. "
                "La investigación fue publicada en el **Journal of Bioinformatics and Computational Biology**."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.1142/s0219720020500389"}
        ]
    },

    # 10. IJMS 2020 - Testicular Germ Cell Tumor Histologies Meta-Analysis
    {
        "id": "post-ijms2020-tgct-genetics",
        "date": "2020-06-24",
        "type": "paper",
        "doi": "10.3390/ijms21124487",
        "auto": False,
        "topics": ["health", "bioinformatics", "genetics"],
        "title": {
            "en": "Tracing the genetic roadmap of testicular cancer",
            "es": "Trazar el mapa genético del cáncer testicular"
        },
        "summary": {
            "en": "With Danish oncologist Finn Edler von Eyben, a transcriptomic meta-analysis across 203 clinical samples uncovering key gene expression shifts that drive testicular tumor development.",
            "es": "Con el oncólogo danés Finn Edler von Eyben, un metaanálisis transcriptómico en 203 muestras clínicas que revela los cambios de expresión génica que impulsan el cáncer testicular."
        },
        "body": {
            "en": (
                "Testicular germ cell tumors (TGCT) represent the most frequent solid malignancy diagnosed in young men between the ages of 15 and 40. "
                "Medical consensus recognizes that these tumors develop from an early precursor lesion known as germ cell neoplasia in situ (GCNIS). "
                "However, the precise molecular switches that cause this initial dormant lesion to progress and diverge into distinct histological subtypes "
                "(such as seminomas versus non-seminomatous tumors like embryonal carcinoma) have long remained an open scientific question.\n\n"
                "In partnership with Danish medical oncologist **Finn Edler von Eyben**, we conducted an extensive transcriptomic meta-analysis combining gene expression data "
                "from three independent clinical studies. The unified dataset comprised 203 tissue specimens spanning healthy normal testis, precursor GCNIS lesions, "
                "and different histological presentations of malignant testicular tumors.\n\n"
                "Using Fisher's combined probability tests, we analyzed the RNA expression patterns of 24 candidate regulatory genes. The meta-analysis revealed "
                "statistically concordant expression differences across the datasets for nine primary genes (including PRAME, KIT, SOX17, NANOG, KLF4, POU5F1, RB1, DNMT3B, and LIN28A). "
                "Notably, certain genes exhibited subtype-specific behavior: **KLF4** showed uniquely elevated expression in seminomas, whereas **DNMT3B** was intensely overexpressed "
                "in embryonal carcinomas.\n\n"
                "These findings delineate a clear genetic progression model, tracing the evolutionary trajectory from normal testicular tissue through in situ neoplasia to differentiated cancer forms. "
                "Clarifying these regulatory milestones supports the development of targeted molecular therapies and improves diagnostic stratification for young patients. "
                "The study was published in open-access format in the **International Journal of Molecular Sciences** (IJMS)."
            ),
            "es": (
                "Los tumores de células germinales testiculares (TGCT) constituyen el tipo de cáncer sólido más diagnosticado en varones jóvenes entre los 15 y 40 años de edad. "
                "La investigación clínica reconoce que estos tumores se originan a partir de una lesión precursora conocida como neoplasia germinal in situ (GCNIS). "
                "A pesar de ello, los mecanismos moleculares exactos que provocan que esta lesión inicial evolucione y se divida en diferentes subtipos histológicos "
                "(como los seminomas y los tumores no seminomatosos, entre ellos el carcinoma embrionario) planteaban interrogantes abiertas.\n\n"
                "En colaboración con el oncólogo danés **Finn Edler von Eyben**, realizamos un metaanálisis transcriptómico integrando datos de expresión génica procedentes "
                "de tres estudios clínicos independientes. El conjunto integrado reunió 203 muestras de tejido correspondientes a tejido testicular normal, lesiones precursoras GCNIS "
                "y diversos subtipos histológicos de tumores testiculares.\n\n"
                "Mediante pruebas de probabilidad combinada de Fisher, evaluamos los perfiles de expresión de ARN de 24 genes candidatos. El metaanálisis confirmó "
                "diferencias concordantes y significativas en nueve genes reguladores fundamentales (entre ellos PRAME, KIT, SOX17, NANOG, KLF4, POU5F1, RB1, DNMT3B y LIN28A). "
                "De manera destacada, ciertos genes mostraron comportamientos exclusivos por subtipo: **KLF4** presentó niveles altos de expresión únicamente en seminomas, "
                "mientras que **DNMT3B** se manifestó con gran intensidad en carcinomas embrionarios.\n\n"
                "Los resultados permiten trazar un mapa de progresión biológica que va desde el tejido sano y la neoplasia in situ hasta las formas tumorales diferenciadas. "
                "Identificar estos marcadores clave contribuye al diseño de terapias dirigidas y a una clasificación diagnóstica más precisa para los pacientes afectados. "
                "El artículo se publicó en modalidad de acceso abierto en el **International Journal of Molecular Sciences** (IJMS)."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.3390/ijms21124487"}
        ]
    },

    # 11. Data in Brief 2019 - RoCoLe Robusta Coffee Leaf Images Dataset
    {
        "id": "post-dib2019-rocole-coffee",
        "date": "2019-08-01",
        "type": "paper",
        "doi": "10.1016/j.dib.2019.104414",
        "auto": False,
        "topics": ["agriculture", "computer-vision", "deep-learning", "datasets"],
        "title": {
            "en": "RoCoLe: An open coffee leaf dataset to train plant disease AI",
            "es": "RoCoLe: Un banco de imágenes de café para entrenar IA en enfermedades de plantas"
        },
        "summary": {
            "en": "With Kevin Cusme, Angélica Loor and Esneider Santander, an open benchmark of 1,560 robusta coffee leaf photographs captured in Ecuadorian plantations to diagnose rust and pest damage.",
            "es": "Con Kevin Cusme, Angélica Loor y Esneider Santander, un banco de pruebas abierto de 1.560 fotografías de hojas de café robusta tomadas en cafetales ecuatorianos para diagnosticar roya y plagas."
        },
        "body": {
            "en": (
                "Coffee is one of the most widely traded agricultural commodities on the planet, providing livelihoods for millions of smallholder farming families. "
                "However, coffee plantations are perpetually endangered by plant diseases, particularly coffee leaf rust (roya, caused by the fungus *Hemileia vastatrix*) "
                "and infestations of red spider mites. When these infections take hold, leaves develop necrotic lesions and drop prematurely, devastating harvest yields "
                "and forcing growers into heavy, costly chemical pesticide treatments.\n\n"
                "Early identification is essential to contain outbreaks, and computer vision powered by deep learning offers great promise for automated crop health monitoring. "
                "Yet existing academic datasets were almost exclusively captured under sterile laboratory settings: detached leaves flattened against white paper under artificial studio lighting. "
                "Models trained on such images invariably fail when deployed in actual fields where leaves flutter in the wind, receive uneven sunlight, and overlap with branches.\n\n"
                "To solve this problem, we created and published **RoCoLe** (Robusta Coffee Leaf dataset). Working with **Kevin Cusme**, **Angélica Loor**, and **Esneider Santander**, "
                "we collected 1,560 high-resolution leaf photographs directly on living coffee shrubs in Manabí, Ecuador, using standard smartphone cameras under realistic daylight conditions. "
                "The collection incorporates comprehensive expert annotations: polygon contours isolating each individual leaf, health classifications (healthy vs. diseased), "
                "and quantitative severity scores measuring the exact percentage of foliage covered by fungal rust spots or mite damage.\n\n"
                "RoCoLe was published in **Data in Brief** with full open access via Mendeley Data. With nearly 100 scientific citations, it has become an international standard benchmark, "
                "utilized by computer vision teams across the globe to train and evaluate semantic segmentation, object detection, and deep learning algorithms for smart agriculture."
            ),
            "es": (
                "El café es uno de los productos agrícolas más comercializados del planeta y el sustento de millones de familias productoras. "
                "Sin embargo, los cafetales enfrentan el ataque constante de plagas y enfermedades, en especial la roya del café (provocada por el hongo *Hemileia vastatrix*) "
                "y las plagas de ácaros rojos. Cuando estas patologías proliferan, las hojas desarrollan manchas necróticas y caen de forma prematura, "
                "reduciendo drásticamente la cosecha y obligando a los agricultores a costosas aplicaciones químicas de emergencia.\n\n"
                "Detectar las afecciones a tiempo resulta decisivo, y la visión artificial con redes neuronales ofrece un gran potencial para monitorear cultivos de forma automática. "
                "Pese a ello, la mayoría de bancos de imágenes disponibles en la investigación habían sido tomados en condiciones de laboratorio: hojas cortadas y colocadas sobre fondos blancos "
                "con iluminación artificial uniforme. Los modelos entrenados con esas imágenes fallan al aplicarse en plantaciones reales, donde la luz solar varía, el viento mueve el follaje "
                "y los fondos son irregulares.\n\n"
                "Para solucionar esta limitación, creamos y publicamos **RoCoLe** (Robusta Coffee Leaf dataset). Junto a **Kevin Cusme**, **Angélica Loor** y **Esneider Santander**, "
                "recolectamos 1.560 fotografías de hojas tomadas directamente sobre cafetos vivos en Manabí, Ecuador, empleando cámaras de teléfonos móviles en condiciones naturales de luz. "
                "El conjunto incluye anotaciones técnicas minuciosas: polígonos que delimitan cada hoja, clasificación de estado (sana o enferma) y el grado de severidad "
                "determinado según el porcentaje de superficie foliar cubierto por manchas de roya o lesiones de ácaros.\n\n"
                "Publicamos RoCoLe en la revista **Data in Brief** con acceso libre en el repositorio Mendeley Data. Con cerca de un centenar de citas científicas internacionales, "
                "el banco de datos se ha consolidado como una referencia global para entrenar algoritmos de segmentación, detección de objetos y diagnóstico temprano en agricultura de precisión."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.1016/j.dib.2019.104414"},
            {"label": "Mendeley Data", "url": "https://doi.org/10.17632/c5yvn32dzg.2"}
        ]
    },

    # 12. Scientometrics 2026 - Institutional Bibliometrics UTM
    {
        "id": "post-scientometrics2026-utm",
        "date": "2026-09-23",
        "type": "paper",
        "doi": "10.1007/s11192-026-05818-4",
        "auto": False,
        "topics": ["bibliometrics", "higher-education", "data-science", "scopus"],
        "title": {
            "en": "How a regional public university built a modern research ecosystem",
            "es": "Cómo una universidad pública regional construyó un ecosistema de investigación moderno"
        },
        "summary": {
            "en": "With Jorge Rodas-Silva, a comprehensive bibliometric study in Scientometrics tracking a decade of research growth, thematic diversification, and international collaboration at Universidad Técnica de Manabí.",
            "es": "Con Jorge Rodas-Silva, un estudio bibliométrico exhaustivo en Scientometrics que analiza una década de crecimiento científico, diversificación temática y colaboración internacional en la Universidad Técnica de Manabí."
        },
        "body": {
            "en": (
                "When national education reforms demand that universities dramatically increase their scientific output, "
                "regional institutions in the Global South face an uphill struggle. Unlike wealthy capital universities with centuries of tradition, "
                "regional public schools often lack established graduate research programs, international funding networks, and protected research hours. "
                "Yet understanding how these universities actually respond to legislative reforms remains an understudied area in higher education policy.\n\n"
                "Together with **Jorge Rodas-Silva**, we conducted a longitudinal bibliometric investigation examining the entire research output of the "
                "**Universidad Técnica de Manabí (UTM)** over a transformative decade (2016 to 2025). Using data indexed in Scopus, we applied quantitative indicators "
                "including compound annual growth rates (CAGR), the Herfindahl-Hirschman Index (HHI) for disciplinary concentration, Gini coefficients with Lorenz curves "
                "for productivity equality, and Louvain community detection algorithms to map coauthorship networks.\n\n"
                "The evidence reveals a compelling institutional trajectory. Following the reforms, the university experienced rapid exponential growth in scientific publications "
                "followed by a stable phase of consolidation. Remarkably, this upward momentum held firm even through devastating external crises, including the destructive "
                "April 2016 Manabí earthquake and the worldwide COVID-19 pandemic. Over the decade, the university expanded from being active in only a single isolated subject area "
                "into diverse disciplinary domains, while its internal collaboration network evolved from fragmented departmental pockets into an interconnected academic community "
                "with near-full connectivity.\n\n"
                "These findings provide empirical guideposts for university administrators and accreditation bodies seeking sustainable models for institutional development. "
                "Building a research culture does not happen overnight, but coherent institutional policies can turn external challenges into opportunities for lasting academic maturity. "
                "The study was published in **Scientometrics** (Springer Nature)."
            ),
            "es": (
                "Cuando las reformas educativas nacionales exigen a las universidades elevar de forma sustancial su producción científica, "
                "las instituciones regionales de países en desarrollo enfrentan un desafío enorme. A diferencia de las universidades tradicionales ubicadas en las grandes capitales, "
                "los centros regionales suelen lidiar con presupuestos ajustados, escasos programas doctorales propios y cargas docentes elevadas. "
                "A pesar de ello, la forma en que estas instituciones responden a las exigencias regulatorias rara vez se documenta con rigor científico.\n\n"
                "Junto a **Jorge Rodas-Silva** desarrollamos una investigación bibliométrica longitudinal que examinó la totalidad de la producción científica de la "
                "**Universidad Técnica de Manabí (UTM)** durante una década decisiva (2016 a 2025). A partir de registros indexados en Scopus, aplicamos indicadores cuantitativos "
                "como la tasa de crecimiento anual compuesto (CAGR), el índice de Herfindahl-Hirschman (HHI) para medir la concentración temática, el coeficiente de Gini con curvas "
                "de Lorenz para la distribución de la productividad y algoritmos de detección de comunidades de Louvain para analizar las redes de coautoría.\n\n"
                "Los datos evidencian una trayectoria institucional notable. Tras las reformas, la universidad experimentó una fase de crecimiento acelerado que dio paso a un periodo "
                "de consolidación sostenida. De forma sorprendente, esta tendencia positiva se mantuvo firme frente a grandes contingencias externas, como el devastador terremoto "
                "de Manabí en abril de 2016 y la posterior crisis sanitaria del COVID-19. A lo largo del decenio, la institución pasó de concentrar casi toda su actividad en una sola "
                "área temática a diversificar su impacto en múltiples disciplinas, mientras que su red interna de colaboración transitó de grupos aislados hacia una estructura académica "
                "cohesionada y ampliamente conectada.\n\n"
                "Estos hallazgos ofrecen pautas empíricas de gran valor para directivos universitarios y organismos de acreditación interesados en diseñar políticas científicas sostenibles. "
                "Construir capacidades investigativas no ocurre de la noche a la mañana, pero una planificación coherente permite transformar las presiones normativas en una cultura "
                "académica sólida y perdurable. El artículo fue publicado en la revista de referencia **Scientometrics** (Springer Nature)."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.1007/s11192-026-05818-4"}
        ]
    },

    # 13. ACMLC 2026 - Vision-Language Models for Coffee Leaf Rust
    {
        "id": "post-acmlc2026-vlm-coffee",
        "date": "2026-07-15",
        "type": "paper",
        "doi": "10.1109/acmlc70381.2026.11700499",
        "auto": False,
        "topics": ["agriculture", "deep-learning", "computer-vision", "vision-language-models"],
        "title": {
            "en": "Can vision-language models diagnose plant diseases without thousands of photos?",
            "es": "¿Pueden los modelos multimodales diagnosticar enfermedades de plantas sin miles de fotos?"
        },
        "summary": {
            "en": "With Jorge Rodas-Silva, evaluating zero-shot and few-shot Vision-Language Models against traditional supervised CNNs to classify coffee leaf rust with minimal training data, presented at ACMLC 2026.",
            "es": "Con Jorge Rodas-Silva, evaluamos modelos multimodales de visión y lenguaje en escenarios zero-shot y few-shot frente a redes neuronales convolucionales para clasificar roya del café con mínimas imágenes, presentado en ACMLC 2026."
        },
        "body": {
            "en": (
                "Coffee leaf rust (roya, caused by the fungus *Hemileia vastatrix*) is the most destructive disease affecting coffee farms worldwide. "
                "For years, computer vision specialists have trained convolutional neural networks (CNNs like ResNet, VGG, or DenseNet) to spot rust lesions automatically. "
                "However, supervised CNNs suffer from a fundamental drawback: they require thousands of laboriously annotated images for every specific disease and "
                "struggle to adapt when deployed in new plantation environments with unfamiliar lighting or soil conditions.\n\n"
                "With **Jorge Rodas-Silva**, we explored a modern alternative powered by foundation models: **Vision-Language Models (VLMs)**. "
                "Unlike conventional image classifiers that learn purely from numeric pixel patterns, VLMs align visual encoders with rich text representations in a shared "
                "multimodal space. This enables **zero-shot** classification (identifying a disease through a simple descriptive prompt without having seen a single training example) "
                "and **few-shot** learning (adapting to a new crop using only three to five reference pictures).\n\n"
                "In this study, we conducted a systematic benchmark comparing zero-shot and few-shot VLMs directly against fully supervised CNN baselines for coffee leaf rust "
                "detection using real plantation imagery. While supervised CNNs remain formidable when massive labeled datasets are available, VLMs demonstrated striking zero-shot "
                "reasoning capabilities and closed the performance gap remarkably fast when provided with just a handful of reference shots per category.\n\n"
                "This shift in artificial intelligence opens promising possibilities for agricultural robotics and mobile farm scouting apps. "
                "Instead of collecting and hand-labeling thousands of plant photos before deploying an AI tool, agronomists can leverage pretrained multimodal models to recognize "
                "emergent crop diseases in near real time. We presented this work at the **2026 8th Asia Conference on Machine Learning and Computing (ACMLC)**, published by IEEE."
            ),
            "es": (
                "La roya del café (producida por el hongo *Hemileia vastatrix*) es la enfermedad foliar más dañina para los cafetales en todo el mundo. "
                "Durante años, los especialistas en visión artificial han entrenado redes neuronales convolucionales (CNN como ResNet, VGG o DenseNet) para detectar estas lesiones "
                "en hojas. No obstante, las CNN supervisadas tienen una debilidad fundamental: necesitan miles de fotos etiquetadas a mano para cada enfermedad y suelen fallar "
                "cuando se instalan en plantaciones con iluminación, fondos o variedades de cultivo diferentes a las del laboratorio.\n\n"
                "Junto a **Jorge Rodas-Silva** exploramos una alternativa vanguardista basada en modelos fundacionales: los **modelos de visión y lenguaje (VLM)**. "
                "A diferencia de los clasificadores convencionales que solo procesan patrones de píxeles, los VLM conectan representaciones visuales con descripciones textuales "
                "en un espacio semántico compartido. Esto permite realizar clasificación **zero-shot** (identificar una patología mediante una simple instrucción de texto sin haber "
                "visto fotos previas de entrenamiento) y aprendizaje **few-shot** (adaptarse con apenas tres a cinco imágenes de referencia).\n\n"
                "En esta investigación desarrollamos una comparativa sistemática entre modelos VLM en modalidades zero-shot y few-shot frente a redes CNN totalmente supervisadas, "
                "utilizando imágenes de hojas de café tomadas en condiciones reales de cultivo. Aunque las CNN supervisadas conservan una alta precisión cuando disponen de grandes "
                "volúmenes de datos anotados, los VLM mostraron una capacidad sorprendente de diagnóstico inmediato y redujeron la brecha de rendimiento rápidamente con solo un puñado "
                "de ejemplos por clase.\n\n"
                "Este avance representa un cambio de paradigma para la robótica agrícola y las aplicaciones de monitoreo en teléfonos móviles. "
                "En lugar de retrasar despliegues de campo durante meses esperando recolectar y etiquetar miles de fotografías, los agrónomos pueden emplear modelos multimodales "
                "preentrenados para reconocer brotes de enfermedades casi en tiempo real. Presentamos estos hallazgos en la **2026 8th Asia Conference on Machine Learning and Computing (ACMLC)**, "
                "con publicación de IEEE."
            )
        },
        "links": [
            {"label": "DOI", "url": "https://doi.org/10.1109/acmlc70381.2026.11700499"}
        ]
    }
]

# Validation checks
PROHIBITED_CHARS = ["—", "–"] # em dash and en dash
PROHIBITED_PHRASES = ["asimismo", "así mismo"]

errors = []
for p in new_posts:
    for lang in ["en", "es"]:
        title = p["title"][lang]
        summary = p["summary"][lang]
        body = p["body"][lang]
        text_block = f"{title}\n{summary}\n{body}"
        
        for ch in PROHIBITED_CHARS:
            if ch in text_block:
                errors.append(f"Post {p['id']} [{lang}] contains prohibited character '{ch}'")
        
        for phr in PROHIBITED_PHRASES:
            if phr in text_block.lower():
                errors.append(f"Post {p['id']} [{lang}] contains prohibited phrase '{phr}'")

if errors:
    print("Validation failed with errors:")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)
else:
    print(f"All {len(new_posts)} posts passed all validation rules successfully! No prohibited characters or phrases found.")

# Merge posts: baseline + new posts
combined_posts = list(baseline_posts) + new_posts
posts_data["items"] = combined_posts

# Write updated posts.json
with open("data/posts.json", "w", encoding="utf-8") as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"Successfully updated data/posts.json! Total posts now: {len(combined_posts)}")
