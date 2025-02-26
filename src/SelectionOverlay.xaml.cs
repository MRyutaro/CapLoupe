using System;
using System.Drawing;
using System.IO;
using System.Windows;
using System.Windows.Input;
using System.Windows.Shapes;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Controls;

namespace src;

public partial class SelectionOverlay : Window
{
    private System.Windows.Point startPoint;
    private bool isSelecting = false;

    public SelectionOverlay()
    {
        InitializeComponent();
    }

    private void Canvas_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        startPoint = e.GetPosition(this);
        SelectionRectangle.Width = 0;
        SelectionRectangle.Height = 0;
        SelectionRectangle.Visibility = Visibility.Visible;
        isSelecting = true;
    }

    private void Canvas_MouseMove(object sender, MouseEventArgs e)
    {
        if (!isSelecting) return;

        var currentPoint = e.GetPosition(this);
        double x = Math.Min(startPoint.X, currentPoint.X);
        double y = Math.Min(startPoint.Y, currentPoint.Y);
        double width = Math.Abs(startPoint.X - currentPoint.X);
        double height = Math.Abs(startPoint.Y - currentPoint.Y);

        Canvas.SetLeft(SelectionRectangle, x);
        Canvas.SetTop(SelectionRectangle, y);
        SelectionRectangle.Width = width;
        SelectionRectangle.Height = height;
    }

    private void Canvas_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
    {
        isSelecting = false;
        var endPoint = e.GetPosition(this);
        this.Hide();

        // **ウィンドウ内座標をスクリーン座標に変換**
        var screenStart = this.PointToScreen(startPoint);
        var screenEnd = this.PointToScreen(endPoint);

        int x = (int)Math.Min(screenStart.X, screenEnd.X);
        int y = (int)Math.Min(screenStart.Y, screenEnd.Y);
        int width = (int)Math.Max(10, Math.Abs(screenStart.X - screenEnd.X));
        int height = (int)Math.Max(10, Math.Abs(screenStart.Y - screenEnd.Y));

        CaptureSelectedArea(x, y, width, height);
        this.Close();
    }

    private void CaptureSelectedArea(int x, int y, int width, int height)
    {
        using (Bitmap bitmap = new Bitmap(width, height))
        {
            using (Graphics g = Graphics.FromImage(bitmap))
            {
                g.CopyFromScreen(x, y, 0, 0, new System.Drawing.Size(width, height));
            }

            string filePath = System.IO.Path.Combine(System.IO.Directory.GetCurrentDirectory(), "selected_screenshot.png");
            bitmap.Save(filePath, ImageFormat.Png);
            MessageBox.Show($"選択範囲のスクリーンショットを保存しました:\n{filePath}",
                "キャプチャ完了",
                MessageBoxButton.OK,
                MessageBoxImage.Information);
        }
    }
}
