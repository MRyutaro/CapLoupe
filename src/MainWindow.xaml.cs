using System;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Input;
using NHotkey;
using NHotkey.Wpf;

namespace src;

public partial class MainWindow : Window
{
    // Windows API の GetCursorPos を呼び出す
    [DllImport("user32.dll")]
    private static extern bool GetCursorPos(out System.Drawing.Point lpPoint);

    public MainWindow()
    {
        InitializeComponent();

        // ショートカットキー（Ctrl + Alt + Z）を登録
        HotkeyManager.Current.AddOrReplace("Zoom", Key.Z, ModifierKeys.Control | ModifierKeys.Alt, OnZoomShortcut);
    }

    private void OnZoomShortcut(object sender, HotkeyEventArgs e)
    {
        System.Drawing.Point cursorPos;
        GetCursorPos(out cursorPos);

        MessageBox.Show($"マウスの位置: X={cursorPos.X}, Y={cursorPos.Y}",
            "マウス座標",
            MessageBoxButton.OK,
            MessageBoxImage.Information);
    }
}
