#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <fstream>

using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{
    RNG rng(100000);
    
    Mat img(480, 640, CV_8UC3, Scalar(0,0,0));
    
    int black = 0;
    int white = 0;
    
    for (int r = 0; r < img.rows; r++) {
        for (int c = 0; c < img.cols; c++) {
            Vec3b px = img.at<Vec3b>(r,c);
            
            if (c > 160) {
                rng.next();
                px = img.at<Vec3b>(r,c%160);
            } else {
                if (rng.next() * 1.0 / UINT_MAX <= 0.5) {
                    px = Vec3b(255, 255, 255);
                    white++;
                } else {
                    black++;
                }
            }

            img.at<Vec3b>(r,c) = px;
        }
    }
    
    Point2d p1(160, 0), p2(160, 480);
    
    line(img, p1, p2, Scalar(0, 0, 255), 2, LINE_AA); 
    p1.x += 160;
    p2.x += 160;
    line(img, p1, p2, Scalar(0, 0, 255), 2, LINE_AA);
    p1.x += 160;
    p2.x += 160;
    line(img, p1, p2, Scalar(0, 0, 255), 2, LINE_AA);
   
    imwrite("out/identical_dots.jpg", img);
    
    //
    white *= 4;
    black *= 4;
    
    double wrat = 1.0*white / (black + white);
    double brat = 1.0*black / (black + white);
    
    ofstream ratios("out/ratios_identical_dots.txt");
    
    ratios << "White: " << wrat << "\n";
    ratios << "Black: " << brat;
    
    ratios.close();
   
    return 0 ;
}
//
// end
//
