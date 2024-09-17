import javax.swing.JFrame;
import java.awt.Canvas;
import java.awt.Graphics;
import java.util.ArrayList;

public class Drawing extends Canvas {
    public static class Point {
        int x; int y; int z;

        public Point(int x, int y, int z) {
            this.x = x; this.y = y; this.z = z;
        }

        public int[] getPoint(){
            int[] out = new int[3];
            out[0] = x;
            out[1] = y;
            out[2] = z;
            return out;
        }
    }

    static Point projectedPoint = new Point(100, 100, 100);
    static Point prevProjected = projectedPoint;
    static Point[] wantArray = new Point[8];
    static ArrayList<Point> lineArray = new ArrayList<>();
    Point camera = new Point(0, 0, -100);
    Point origin = new Point(640, 360, 0);
    int[] originArray = origin.getPoint();

    public static int[] project(Point cam, Point wish) {
        int[] camArray = cam.getPoint();
        int[] wishArray = wish.getPoint();
        int camz = camArray[2];
        int wishx = wishArray[0];
        int wishy = wishArray[1];
        int wishz = wishArray[2];
        int focalLength = Math.abs(camz);
        int xProjected = (focalLength * wishx) / (focalLength + wishz);
        int yProjected = (focalLength * wishy) / (focalLength + wishz);
        int[] outArray = new int[2];
        outArray[0] = xProjected; outArray[1] = yProjected;
        return outArray;
    }

    public void paint(Graphics g) {
        //Point myPoint = new Point(0, 0, 100);
        for (int i = 0; i < 8; i++) {
            int[] projected = project(camera, wantArray[i]);
            prevProjected = projectedPoint;
            projectedPoint.x = originArray[0]+projected[0]; 
            projectedPoint.y = originArray[1]+projected[1]; 
            projectedPoint.z = 0;
            g.fillOval(projectedPoint.x, projectedPoint.y, 10, 10);
        } 
    }

    public static void main(String[] a) {
        wantArray[0] = new Point(100, 100, 100);
        wantArray[1] = new Point(-100, 100, 100);
        wantArray[2] = new Point(100, -100, 100);
        wantArray[3] = new Point(-100, -100, 100);
        wantArray[4] = new Point(100, 100, 200);
        wantArray[5] = new Point(-100, 100, 200);
        wantArray[6] = new Point(100, -100, 200);
        wantArray[7] = new Point(-100, -100, 200);
        JFrame frame = new JFrame("3D Renderer");
        Canvas canvas = new Drawing();
        canvas.setSize(1280, 720);
        frame.add(canvas);
        frame.pack();
        frame.setVisible(true);
    }
}
