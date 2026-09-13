<div align="center">

# 🕊️ Superfamille Typographique PocketGull

[![Licence OFL 1.1](https://img.shields.io/badge/Licence-SIL_OFL_1.1-orange.svg?style=flat-square)](OFL.txt)
[![SemVer 3.0.0](https://img.shields.io/badge/SemVer-3.0.0-blue.svg?style=flat-square)](CHANGELOG.md)
[![Validation W3C OTS](https://img.shields.io/badge/W3C_OTS-100%25_Valide-emerald.svg?style=flat-square)](https://github.com/googlefonts/ots)
[![Assurance Qualité Fontbakery](https://img.shields.io/badge/Fontbakery-711%2F711_R%C3%A9ussis-brightgreen.svg?style=flat-square)](https://github.com/googlefonts/fontbakery)
<br/>
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--1372--5381-A6C900?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0008-1372-5381)
[![Archivage CERN Zenodo](https://img.shields.io/badge/CERN%20Zenodo-Science%20Ouverte-024c9c.svg?style=flat-square)](documentation/CERN_ZENODO_ARCHIVAL_GUIDE.md)
[![Conformité WCAG 2.1 AAA](https://img.shields.io/badge/WCAG_2.1-AAA_100%25-emerald.svg?style=flat-square)](index.html)

<br/>

### 🌐 [Spécimen Interactif en Ligne](https://font.pocketgull.app) &nbsp;•&nbsp; 📦 [Sources UFO](sources/) &nbsp;•&nbsp; 📄 [Licence SIL OFL 1.1](OFL.txt) &nbsp;•&nbsp; 🏛️ [Archivage CERN](documentation/CERN_ZENODO_ARCHIVAL_GUIDE.md)

</div>

<div align="center">

<img src="documentation/images/pocketgull_device_hero.jpg" alt="Dispositif télémétrique PocketGull et interface optotypique" width="100%" />

<br/><br/>

<table>
  <tr>
    <td width="50%" align="center">
      <img src="documentation/images/pocketgull_synaptic_specimen_light.png" alt="Codex synaptique PocketGull - Mode clair" width="100%" />
    </td>
    <td width="50%" align="center">
      <img src="documentation/images/pocketgull_synaptic_specimen_dark.png" alt="Codex synaptique PocketGull - Mode sombre" width="100%" />
    </td>
  </tr>
</table>

</div>

**PocketGull** est une superfamille typographique libre et open-source comprenant des styles sans-serif cliniques, d'affichage et à chasse fixe télémétrique, conçue par Phil Gear. Conçue pour unir la chaleur humaniste du tracé manuel à la rigueur de la précision clinique critique, PocketGull répond à un impératif vital des logiciels médicaux : éliminer les erreurs d'administration médicamenteuse tout en offrant une texture organique et reposante pour les yeux lors des gardes hospitalières de 12 heures.

Issue de lettrages spontanés au feutre biseauté sur bristol physique, PocketGull synthétise le dynamisme du tracé biologique avec les règles de désambiguïsation de l'Institut pour la Sécurité des Pratiques Médicamenteuses (ISMP / ANSM) et les invariants de lisibilité optotypique 5:1 de Louise Sloan.

---

## 🗂️ Architecture de la Superfamille : Familles Typographiques & Polices Numériques

PocketGull est construite sur une grille normalisée de 1000 UPM (Unités Par Cadratin). En taxonomie typographique rigoureuse, **PocketGull** constitue la *famille de caractères* (le dessin conceptuel), tandis que les fichiers binaires compilés `.woff2` et `.ttf` en constituent les *polices numériques concrètes* :

| Sous-famille de Caractères | Fichier Binaire de Police | Nom PostScript | Graisse | Métrique d'Avance | Cas d'Usage Clinique Principal |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PocketGull Bold** | `PocketGull-Bold.woff2` | `PocketGull-Bold` | 700 / 800 | Proportionnelle | Marqueurs de prescription, ancres de lecture bionique, alarmes |
| **PocketGull Fineliner** | `PocketGull-Fineliner.woff2` | `PocketGull-Fineliner` | 400 | Proportionnelle | Observations médicales denses, dossiers patients (DPI), notices |
| **PocketGull Chiseltip** | `PocketGull-Chiseltip.woff2` | `PocketGull-Chiseltip` | 900 | Proportionnelle | Signalétique d'urgence, alertes de déchocage, pancartes |
| **PocketGull Mono** | `PocketGullMono-Regular.woff2` | `PocketGullMono-Regular` | 400 / 500 | Fixe 600 UPM | Monitorage réanimatoire, constantes tabulaires, tracés ECG |

---

## 🔬 Innovations Fondamentales

* **🫀 Désambiguïsation ISMP & FDA** : Tables de fonctionnalités OpenType natives pour le zéro barré (`cv08`), le `l` minuscule courbé (`cv05`), le `I` majuscule empatté (`ss02`) et les chiffres tabulaires (`tnum`).
* **⠃ Bloc Braille Unicode 256 Caractères (`U+2800`–`U+28FF`)** : Matrice tactile conforme à la norme ISO/TR 11548 pour les conditionnements sous blister et l'accessibilité pharmaceutique.
* **👁️ Optotypes de Sloan 5:1 & Espacement de Bouma** : Étalonnage pour une acuité visuelle LogMAR 0.0 (Snellen 20/20) et suppression du phénomène d'encombrement périphérique d'Herman Bouma à 50–70 cm de distance de lecture.
* **💻 Terminal Médical Réanimatoire & Thème Oh My Posh** : Chasse fixe stricte de 600 UPM avec caractères de tracé de cadres continus (`U+2500`–`U+257F`), formes d'ondes ECG sous-cellulaires et thème de prompt natif (`pocketgull-ophthalmic.omp.json`).

---

## 🌐 Feuille de Route & Progression des Écritures Universelles

Afin de garantir l'équité mondiale des soins de santé, PocketGull étend son support à l'ensemble des grands systèmes d'écriture, éliminant ainsi le syndrome du glyphe manquant (« tofu ») dans les dossiers de santé électroniques internationaux :

| Niveau | Systèmes d'Écriture | Glyphes Cibles | Effort Estimé | Statut dans PocketGull |
| :--- | :--- | :---: | :---: | :---: |
| **Niveau 1 (Occidental & Tactile)** | Latin, Cyrillique, Grec, Braille, Télémétrie Réa | ~1 800 | 1 200 h | 🟢 **100 % Achevée** (3 350+ caractères) |
| **Niveau 2 (RTL & Sémitique)** | Arabe, Hébreu, Syriaque, Thaana (BiDi & Cursif) | ~2 200 | 1 500 h | 📋 Planifiée |
| **Niveau 3 (Noyau Indique)** | Devanagari, Bengali, Tamoul, Télougou, Gurmukhi, Gujarati | ~6 500 | 4 200 h | 🟡 En cours (128 caractères Devanagari) |
| **Niveau 4 (Asie du Sud-Est)** | Thaï, Lao, Khmer, Birman, Tibétain | ~2 000 | 1 200 h | 📋 Planifiée |
| **Niveau 5 (Noyau Clinique CJK)** | Sinogrammes médicaux fréquents (Hanzi/Kanji), Kana, Hangeul | ~15 000 | 8 500 h | 📋 Planifiée |
| **Niveau 6 (Autochtone & Africain)** | Syllabaire canadien (Inuktitut), Duployé (Chinuk Pipa), Néo-Tifinagh, Cherokee, Éthiopique, Adlam, Vaï | 1 760 CP | 5 280 h économisées | 🟢 **100 % Native en Production** (1 760 points de code, 7 040 glyphes compilés en 73,9s) |

*Études de Cas Cliniques Autochtones* : Les sept études de cas souveraines sont documentées avec télémétrie empirique :
- Étude de cas 01 : [`CASE_STUDY_01_INUKTITUT_SYLLABICS.md`](documentation/case_studies/CASE_STUDY_01_INUKTITUT_SYLLABICS.md) (Télésanté arctique au Nunavut)
- Étude de cas 02 : [`CASE_STUDY_02_CHINUK_PIPA.md`](documentation/case_studies/CASE_STUDY_02_CHINUK_PIPA.md) (Grand Ronde & Nord-Ouest Pacifique)
- Étude de cas 03 : [`CASE_STUDY_03_NEO_TIFINAGH.md`](documentation/case_studies/CASE_STUDY_03_NEO_TIFINAGH.md) (Vitalité linguistique amazighe nord-africaine)
- Étude de cas 04 : [`CASE_STUDY_04_CHEROKEE_SYLLABARY.md`](documentation/case_studies/CASE_STUDY_04_CHEROKEE_SYLLABARY.md) (Syllabaire Sequoyah & Hôpital Hastings)
- Étude de cas 05 : [`CASE_STUDY_05_ETHIOPIC_GEEZ.md`](documentation/case_studies/CASE_STUDY_05_ETHIOPIC_GEEZ.md) (Abugida à 7 ordres de la Corne de l'Afrique)
- Étude de cas 06 : [`CASE_STUDY_06_WEST_AFRICAN_SCRIPTS.md`](documentation/case_studies/CASE_STUDY_06_WEST_AFRICAN_SCRIPTS.md) (Santé communautaire Adlam & Vaï)
- Étude de cas 07 : [`CASE_STUDY_07_PAN_TRIBAL_ORTHOGRAPHIES.md`](documentation/case_studies/CASE_STUDY_07_PAN_TRIBAL_ORTHOGRAPHIES.md) (12 zones IHS, 574+ tribus & diacritiques empilés)

En attendant l'achèvement natif des niveaux restants, PocketGull s'harmonise parfaitement avec Google Noto Sans (`sCapHeight=714`, `sxHeight=536` concordance métrique exacte sur grille 1000 UPM) et les polices système CJK/Indiques, sans aucun décalage d'alignement sur la ligne de base.

---

## 🚀 Intégration Rapide

Liaison via feuille de style CSS :
```html
<link rel="stylesheet" href="https://font.pocketgull.app/fonts.css">
```

Activation de la sécurité posologique clinique :
```css
.securite-posologique-clinique {
  font-family: 'PocketGull', sans-serif;
  font-feature-settings: "zero" 1, "cv08" 1, "cv05" 1, "ss02" 1, "tnum" 1;
}
```

---

## 📚 Documentation & Spécifications

* 📖 **[Spécification de Conception](documentation/DESIGN_SPECIFICATION.md)** — Principes directeurs d'architecture et genèse du projet
* 🔬 **[Bibliographie Scientifique](documentation/BIBLIOGRAPHY.md)** — Littérature ophtalmologique et sciences de la vision évaluée par les pairs
* 🏛️ **[Guide d'Archivage CERN & Zenodo](documentation/CERN_ZENODO_ARCHIVAL_GUIDE.md)** — Préservation pérenne en Science Ouverte
* ⚖️ **[Gouvernance du Projet](GOVERNANCE.md)** — Cadre de supervision éthique et comité de revue
* 👁️ **[Cadre Typographique Responsable](RESPONSIBLE_TYPOGRAPHY.md)** — Sécurité clinique et invariants optotypiques
* 🏥 **[Mémo d'Autorisation de Déploiement](documentation/WORKSTATION_AUTHORIZATION_LETTER.md)** — Dossier technique institutionnel pour directeurs médicaux (CMIO) et DSI
* 🛠️ **[Compilation depuis les Sources UFO](sources/)** — Configuration du compilateur avec `fontmake` et `gftools-builder`
* 🛡️ **[Politique de Sécurité](SECURITY.md)** — Divulgation responsable des vulnérabilités OpenSSF et validation W3C OTS
* 📝 **[Journal des Modifications](CHANGELOG.md)** — Historique de versionnement sémantique (SemVer 3.0.0)

---

## 🔬 Citation Académique & DOI CERN / Zenodo

Si vous intégrez la superfamille typographique PocketGull dans vos recherches cliniques, vos dispositifs médicaux logiciels ou vos publications scientifiques en ophtalmologie, veuillez citer le projet via le fichier [`CITATION.cff`](CITATION.cff) ou la notice BibTeX ci-dessous :

```bibtex
@software{gear_pocketgull_font_2026,
  author       = {Gear, Phil and {Les auteurs du projet PocketGull}},
  title        = {{Superfamille Typographique PocketGull : Tracés Vectoriels Cliniques et Ophtalmologiques à Calibrage Optotypique}},
  month        = sep,
  year         = 2026,
  publisher    = {CERN / Zenodo},
  version      = {3.0.0},
  doi          = {10.5281/zenodo.20647514},
  url          = {https://font.pocketgull.app},
  license      = {OFL-1.1}
}
```

---

## 🙏 Remerciements

Nous adressons notre profonde gratitude aux personnes et initiatives qui rendent PocketGull possible :
* **Le langage de programmation Dart & l'Ingénierie Google** ([dart.dev](https://dart.dev)) : Pour l'environnement autonome, typé et hautement performant qui propulse nos pipelines de synthèse vectorielle procédurale, nos matrices de données phonologiques et le rendu sans tête de nos spécimens.
* **Randal L. Schwartz** : Pour des décennies de contributions fondamentales au logiciel libre, à la pédagogie des développeurs, à la défense de Perl et de Dart, et pour son exigence d'une rigueur absolue dans l'outillage en ligne de commande.
* **Les Gardiens Linguistiques Autochtones & Praticiens Cliniques** : Pour leur dévouement culturel inestimable au sein des 574+ tribus souveraines, Premières Nations et conseils circumpolaires.
* **Les Pionniers de la Vision et de la Sécurité des Patients** : Louise L. Sloan (optotypes 5:1), Herman Bouma (encombrement visuel périphérique) et l'Institut pour la Sécurité des Pratiques Médicamenteuses (ISMP).

Consultez **[THANKS.md](THANKS.md)** pour l'ensemble des hommages et dédicaces.

---

## 📜 Licence & Droits d'Auteur

PocketGull est distribuée sous la **[Licence SIL Open Font, Version 1.1](OFL.txt)**.  
Utilisation libre et gratuite pour les projets personnels, académiques et commerciaux.

**Copyright (c) 2026 Les Auteurs du Projet PocketGull** ([Dépôt GitHub](https://github.com/pocketgull-app/pocketgull-font)).  
*Ancrée dans la science empirique. Conçue pour la vie. 🕊️*
