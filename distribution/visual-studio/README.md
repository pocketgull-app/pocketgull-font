# PocketGull Typeface for Visual Studio & .NET

Open-source clinical sans-serif, display, and telemetry monospace font superfamily for Visual Studio IDE, WPF, WinUI 3, .NET MAUI, and C++ desktop applications.

## Installation in Visual Studio

### Option 1: NuGet Package Manager Console
```powershell
Install-Package PocketGull.Typeface
```

### Option 2: .NET CLI
```bash
dotnet add package PocketGull.Typeface
```

## Usage in WPF (XAML)
```xml
<Window ...
        FontFamily="pack://application:,,,/PocketGull.Typeface;component/fonts/#PocketGull">
    <TextBlock Text="Amoxicillin 500 mg • Sinus Rhythm 72 bpm" 
               FontFamily="pack://application:,,,/PocketGull.Typeface;component/fonts/#PocketGull Mono"
               FontSize="16" />
</Window>
```

## Usage in .NET MAUI (`MauiProgram.cs`)
```csharp
builder
    .UseMauiApp<App>()
    .ConfigureFonts(fonts =>
    {
        fonts.AddFont("PocketGullMono-Regular.ttf", "PocketGullMono");
        fonts.AddFont("PocketGull-Fineliner.ttf", "PocketGullFineliner");
    });
```

## Configuring Visual Studio Editor Font
To use PocketGull Mono as your primary code editor font in Visual Studio:
1. Open **Tools** -> **Options** -> **Environment** -> **Fonts and Colors**.
2. Under **Show settings for**, select **Text Editor**.
3. Under **Font**, select **PocketGull Mono**.
4. Set Size to **11** or **12**.
