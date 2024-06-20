#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <fstream>
#include <iostream>

using namespace std;
using namespace cv;

class Circle {
    private:
        int x;
        int y;
        int r;
        Vec3b exclude;
    public:
        Circle(int xc, int yc, int ca) {
            x = xc;
            y = yc;
            r = 40;
            
            if (ca == 1) {
                exclude = Vec3b(0, 0, 255); // red
            } else if (ca == 2) {
                exclude = Vec3b(0, 255, 0); // green
            } else if (ca == 3) {
                exclude = Vec3b(255, 0, 0); // blue
            }
        }
    
        bool contains(int xp, int yp) {
            int dx = xp - x;
            int dy = yp - y;
            return dx*dx + dy*dy <= r*r;
        }
    
        Vec3b getExcludedColor() {
            return exclude;
        }
};

int main(int argc, char* argv[])
{
    Mat img(480, 640, CV_8UC3, Scalar(255, 255, 255));
    int alternation = 1;
    Vec3b color(255, 0, 0);

    ifstream infile("in/xy.txt"); // coords
    const int n = 12;
    Circle* circles[n];
    Vec3b circleColor(165, 176, 200); // c8b0a5
    int circleAlternation = 0;
    
    for (int k = 0; k < n; k++) {
        if (k % 4 == 0) {
            circleAlternation++;
        }
        int x, y;
        infile >> x >> y;        
        circles[k] = new Circle(x, y, circleAlternation);
    }
    
    // offset of 3 at top
    for (int r = 3; r < img.rows; r++) {        
        if ((r - 3) % 6 == 0) {
            if (alternation % 3 == 0) {
                color = Vec3b(255, 0, 0);
            } else if (alternation % 3 == 1) {
                color = Vec3b(0, 0, 255);
            } else if (alternation % 3 == 2) {
                color = Vec3b(0, 255, 0);
            }
            alternation++;
        }
        for (int c = 0; c < img.cols; c++) {
            img.at<Vec3b>(r,c) = color;
        }
    }
    
    for (int r = 0; r < img.rows; r++) {
        for (int c = 0; c < img.cols; c++) {
            bool flag = false;
            for (int k = 0; k < n; k++) {
                if (circles[k]->contains(c, r)) {
                    if (img.at<Vec3b>(r,c) = circles[k]->getExcludedColor()) {
                        flag = true;
                        break;
                    }
                }
            }
            if (flag) {
                img.at<Vec3b>(r,c) = circleColor; 
            }
        }
    }
    
    imwrite("out/alternate.png", img);
    
    // gif
    for (int i = 0; i < 18; i++) {
        
        for (int r = 3; r < img.rows; r++) {        
            if ((r - 3) % 6 == 0) {
                if (alternation % 3 == 0) {
                    color = Vec3b(255, 0, 0);
                } else if (alternation % 3 == 1) {
                    color = Vec3b(0, 0, 255);
                } else if (alternation % 3 == 2) {
                    color = Vec3b(0, 255, 0);
                }
                alternation++;
            }
            for (int c = 0; c < img.cols; c++) {
                int modfr = r+i;
                if (modfr >= img.rows) {
                    modfr = (r+i)-img.rows+3;
                }
                img.at<Vec3b>(modfr,c) = color;
            }
        }

        for (int r = 0; r < img.rows; r++) {
            for (int c = 0; c < img.cols; c++) {
                bool flag = false;
                for (int k = 0; k < n; k++) {
                    if (circles[k]->contains(c, r)) {
                        if (img.at<Vec3b>(r,c) = circles[k]->getExcludedColor()) {
                            flag = true;
                            break;
                        }
                    }
                }
                if (flag) {
                    img.at<Vec3b>(r,c) = circleColor; 
                }
            }
        }
        
        imwrite("out/alternate_gif/" + to_string(i) + ".png", img);
    }
    
    return 0;
}

//
// end
//
