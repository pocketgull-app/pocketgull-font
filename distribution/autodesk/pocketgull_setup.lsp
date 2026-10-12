; PocketGull CAD Dimension & Annotation Style Setup for AutoCAD
; ==============================================================
; Configures Louise Sloan 5:1 optotypic acuity and ISMP clinical
; character disambiguation for architectural & mechanical blueprints.
;
; How to load in AutoCAD:
;   Command: (load "pocketgull_setup.lsp")
;   Or add to your acaddoc.lsp startup suite.

(defun c:PocketGullSetup ()
  (vl-load-com)
  
  (princ "\nConfiguring PocketGull CAD Annotation Environment...")

  ; 1. Define Text Style POCKETGULL-STANDARD (PocketGull-Fineliner.ttf)
  (if (null (tblsearch "STYLE" "POCKETGULL-STANDARD"))
    (command "-STYLE" "POCKETGULL-STANDARD" "PocketGull-Fineliner.ttf" "0.0" "1.0" "0.0" "N" "N")
    (princ "\nStyle POCKETGULL-STANDARD already defined.")
  )

  ; 2. Define Text Style POCKETGULL-MONO (PocketGullMono-Regular.ttf)
  (if (null (tblsearch "STYLE" "POCKETGULL-MONO"))
    (command "-STYLE" "POCKETGULL-MONO" "PocketGullMono-Regular.ttf" "0.0" "1.0" "0.0" "N" "N")
    (princ "\nStyle POCKETGULL-MONO already defined.")
  )

  ; 3. Define Text Style POCKETGULL-BOLD (PocketGull-Bold.ttf for Titling/Placards)
  (if (null (tblsearch "STYLE" "POCKETGULL-BOLD"))
    (command "-STYLE" "POCKETGULL-BOLD" "PocketGull-Bold.ttf" "0.0" "1.0" "0.0" "N" "N")
    (princ "\nStyle POCKETGULL-BOLD already defined.")
  )

  ; 4. Configure Dimension Text Style
  (setvar "DIMTXSTY" "POCKETGULL-STANDARD")
  (setvar "DIMTXT" 2.5)     ; 2.5 mm standard optometric annotation height
  (setvar "DIMASZ" 2.5)     ; Arrow size matches Sloan stroke contrast
  (setvar "DIMEXE" 1.25)    ; Extension line extension
  (setvar "DIMEXO" 0.625)   ; Extension line offset
  (setvar "DIMTAD" 1)       ; Place text above dimension line

  (princ "\n[SUCCESS] PocketGull CAD typography loaded: DIMTXSTY set to POCKETGULL-STANDARD.")
  (princ)
)

; Auto-execute upon loading
(c:PocketGullSetup)
