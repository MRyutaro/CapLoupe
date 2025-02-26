using System;
using System.IO;
using System.Windows;
using System.Windows.Media.Imaging;

namespace src;

public partial class PreviewWindow : Window
{
    public PreviewWindow(string imagePath)
    {
        InitializeComponent();
        DisplayImage(imagePath);
    }

    private void DisplayImage(string imagePath)
    {
        if (File.Exists(imagePath))
        {
            BitmapImage bitmap = new BitmapImage();
            bitmap.BeginInit();
            bitmap.UriSource = new Uri(imagePath);
            bitmap.CacheOption = BitmapCacheOption.OnLoad;
            bitmap.EndInit();

            PreviewImage.Source = bitmap;
        }
        else
        {
            MessageBox.Show("画像が見つかりません", "エラー", MessageBoxButton.OK, MessageBoxImage.Error);
            this.Close();
        }
    }

    // **ESCキーでウィンドウを閉じる**
    private void Window_KeyDown(object sender, System.Windows.Input.KeyEventArgs e)
    {
        if (e.Key == System.Windows.Input.Key.Escape)
        {
            this.Close();
        }
    }
}
