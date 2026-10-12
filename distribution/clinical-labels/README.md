# PocketGull Typography for Clinical Pharmacy & EHR Labels (ZPL / FHIR)

Brings **ISMP Character Disambiguation**, **Tall Man Lettering**, and **Louise Sloan 5:1 optotypes** to Zebra and Brother thermal prescription printers in hospital pharmacies.

## Why PocketGull for Pharmacy Labels?
* **Eliminates Lookalike Collisions**: Confusing *hydrOXYzine* (antihistamine) with *hydrALAzine* (antihypertensive) can be fatal. PocketGull's stroke clarity makes Tall Man capital letters stand out instantly.
* **Slashed Zero Protection**: Dosage `50 mg` vs `500 mg` can never be confused because every zero is cleanly slashed (`0̸`) with optical junction thinning.

## Zebra Thermal Printer Setup (ZPL-II)

Send the font to printer memory (flash `E:` or DRAM `R:`):

```bash
# Upload TrueType font to Zebra printer memory
! CISDFCRC16
~DUE:POCKETGULL.TTF,bytes,data...
```

Use the included template [prescription_label_ismp.zpl](prescription_label_ismp.zpl) to print GS1-128 compliant bedside unit-dose labels.
