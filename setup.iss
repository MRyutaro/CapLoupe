[Setup]
AppName=CapLoupe
AppVersion=1.2.0
AppPublisher=MRyutaro
AppPublisherURL=https://github.com/MRyutaro/CapLoupe
DefaultDirName={commonpf}\CapLoupe
DefaultGroupName=CapLoupe
OutputDir=.\output
OutputBaseFilename=installer
Compression=lzma
SolidCompression=yes
SetupIconFile=.\docs\cap_loupe.ico
DisableProgramGroupPage=yes
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Files]
Source: "dist\CapLoupe.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\CapLoupe"; Filename: "{app}\CapLoupe.exe"
Name: "{commondesktop}\CapLoupe"; Filename: "{app}\CapLoupe.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CapLoupe.exe"; Description: "Launch CapLoupe"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "CapLoupe"; ValueData: """{app}\CapLoupe.exe"""; Flags: uninsdeletevalue

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked
