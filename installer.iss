[Setup]
AppName=CS2 Mac Analizci
AppVersion=1.0
DefaultDirName={autopf}\CS2 Mac Analizci
DefaultGroupName=CS2 Mac Analizci
OutputDir=installer
OutputBaseFilename=CS2-Mac-Analizci-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\CS2-Mac-Analizci.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\CS2 Mac Analizci"; Filename: "{app}\CS2-Mac-Analizci.exe"
Name: "{commondesktop}\CS2 Mac Analizci"; Filename: "{app}\CS2-Mac-Analizci.exe"

[Run]
Filename: "{app}\CS2-Mac-Analizci.exe"; Description: "Uygulamayı Başlat"; Flags: nowait postinstall skipifsilent