using System.Windows;
using System.Windows.Input;
using NHotkey;
using NHotkey.Wpf;

namespace src;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        // **メインウィンドウを表示せずにアプリを起動**
        RegisterHotkey();
    }

    private void RegisterHotkey()
    {
        HotkeyManager.Current.AddOrReplace("SelectCapture", Key.Z, ModifierKeys.Control | ModifierKeys.Alt, (sender, args) =>
        {
            SelectionOverlay overlay = new SelectionOverlay();
            overlay.ShowDialog();
        });
    }
}
