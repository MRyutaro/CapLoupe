using System.Windows;
using System.Windows.Input;
using NHotkey;
using NHotkey.Wpf;

namespace src;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        HotkeyManager.Current.AddOrReplace("SelectCapture", Key.Z, ModifierKeys.Control | ModifierKeys.Alt, OnCaptureShortcut);
    }

    private void OnCaptureShortcut(object? sender, HotkeyEventArgs e)
    {
        SelectionOverlay overlay = new SelectionOverlay();
        overlay.ShowDialog();  // ウィンドウをモーダルで開く
    }
}
