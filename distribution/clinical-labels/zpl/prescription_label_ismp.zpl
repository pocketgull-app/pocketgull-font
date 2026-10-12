^XA
^FX =============================================================
^FX PocketGull Clinical EHR Prescription Label Template (ZPL-II)
^FX Enforces Louise Sloan 5:1 Acuity & ISMP Tall Man Lettering
^FX =============================================================
^PW812
^LL1218
^LH0,0

^FX --- Header Banner ---
^FO40,40^GB732,80,4,B,0^FS
^FO60,65^A0N,45,45^FDMEMORIAL HOSPITAL PHARMACY^FS

^FX --- Patient Identification ---
^FO40,140^A0N,30,30^FDPATIENT: DOE, JANE M.^FS
^FO500,140^A0N,30,30^FDMRN: 902-814-11^FS
^FO40,180^A0N,25,25^FDDOB: 1968-04-12   LOC: ICU BED 04^FS

^FX --- Divider ---
^FO40,220^GB732,2,2^FS

^FX --- Critical Medication & Dosage (ISMP Tall Man Lettering) ---
^FO40,240^A0N,45,45^FDhydrOXYzine HCl^FS
^FO40,295^A0N,35,35^FDDOSE: 25 mg ORAL CAPSULE^FS
^FO40,345^A0N,30,30^FDFREQ: Q6H PRN SEVERE ANXIETY^FS

^FX --- Warnings & Lookalike Disambiguation Banner ---
^FO40,400^GB732,100,0,B^FS
^FO60,420^FR^A0N,28,28^FDWARNING: NOT hydrALAzine (Blood Pressure)^FS
^FO60,455^FR^A0N,26,26^FDVERIFY DOSAGE & INDICATION PRIOR TO ADMIN^FS

^FX --- Barcode (GS1-128 / Medication Barcode Verification) ---
^FO150,530^BY3,3,100^BCN,100,Y,N,N^FD(01)00300450250123(21)987654321^FS

^FX --- Dispensing Metadata ---
^FO40,680^A0N,22,22^FDRX: 4892019   QTY: 30   DATE: 2026-10-12^FS
^FO40,710^A0N,22,22^FDRPh: P. GEAR, PharmD   EXP: 2027-10-12^FS

^XZ
