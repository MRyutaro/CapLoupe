using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using NHotkey;
using NHotkey.Wpf;

namespace src;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        // ショートカットキー（Ctrl + Alt + Z）を登録
        HotkeyManager.Current.AddOrReplace("Zoom", Key.Z, ModifierKeys.Control | ModifierKeys.Alt, OnZoomShortcut);
    }

    private void OnZoomShortcut(object sender, HotkeyEventArgs e)
    {
        MessageBox.Show("ショートカットキーが押されました！", "通知", MessageBoxButton.OK, MessageBoxImage.Information);
    }
}
