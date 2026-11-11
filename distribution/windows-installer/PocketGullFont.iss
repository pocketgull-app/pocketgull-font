; PocketGull Font Superfamily v4.0.0 — Official Windows & WinGet Installer
[Setup]
AppId={{8D692F2F-D44B-451D-A62F-E95528567C5F}
AppName=PocketGull Font
AppVersion=4.0.0
AppVerName=PocketGull Font 4.0.0
AppPublisher=The PocketGull Project Authors
AppPublisherURL=https://font.pocketgull.app
AppSupportURL=https://github.com/pocketgull-app/pocketgull-font/issues
AppUpdatesURL=https://github.com/pocketgull-app/pocketgull-font/releases
VersionInfoVersion=4.0.0.0
VersionInfoCompany=The PocketGull Project Authors
VersionInfoDescription=PocketGull Clinical & Scientific Typeface Installer
VersionInfoCopyright=Copyright (c) 2026 The PocketGull Project Authors (OFL-1.1)
DefaultDirName={autopf}\PocketGull Font
DisableDirPage=yes
DisableProgramGroupPage=yes
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog commandline
OutputDir=dist
OutputBaseFilename=PocketGull-Font-Setup-v4.0.0
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardImageFile=assets\wizard-banner.bmp
WizardSmallImageFile=assets\wizard-small.bmp
SetupIconFile=assets\pocketgull.ico
UninstallDisplayIcon={app}\pocketgull.ico
UninstallDisplayName=PocketGull Font
LicenseFile=..\..\OFL.txt
InfoBeforeFile=assets\specimen-info.rtf
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "assets\pocketgull.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\OFL.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "stage_ttf\PocketGull-ASL.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull ASL"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Algo.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Algo"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Black.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Black"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Bold.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Bold"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-BoldItalic.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Bold Italic"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Chem.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Chem"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Chiseltip.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Chiseltip"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-CondensedBold.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Condensed Bold"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Emoji.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Emoji"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Fineliner.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Fineliner"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Genome.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Genome"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Halftone.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Halftone"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Inline.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Inline"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Italic.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Italic"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Lab.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Lab"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Learn.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Learn"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-MarkerRaw.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Marker Raw"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Math.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Math"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Micro.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Micro"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Music.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Music"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Numerics.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Numerics"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Outline.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Outline"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Press.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Press"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Regular.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Serif-Bold.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Serif Bold"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Serif-Regular.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Serif"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Serif-VF.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Serif VF"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Sign.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Sign"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Slab-Bold.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Slab Bold"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Slab-Regular.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Slab"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Soft-Bold.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Soft Bold"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Soft-Regular.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Soft"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-VF.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull VF"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGullMono-Bold.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Mono Bold"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGullMono-Italic.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Mono Italic"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGullMono-Regular.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Mono"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Botanica.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Botanica"; Flags: ignoreversion restartreplace
Source: "stage_ttf\PocketGull-Kintsugi.ttf"; DestDir: "{autofonts}"; FontInstall: "PocketGull Kintsugi"; Flags: ignoreversion restartreplace
