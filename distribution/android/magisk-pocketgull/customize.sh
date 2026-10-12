SKIPMOUNT=false
PROPFILE=false
POSTFSDATA=true
LATESTARTSERVICE=false

ui_print "****************************************"
ui_print "*    PocketGull Font for Google Pixel  *"
ui_print "*   ISMP Disambiguation & OLED Energy  *"
ui_print "*           Version 3.1.0              *"
ui_print "****************************************"

set_permissions() {
  set_perm_recursive $MODPATH 0 0 0755 0644
  set_perm_recursive $MODPATH/system/fonts 0 0 0755 0644
}
