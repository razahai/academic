#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>

using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{
    RNG rng(100000);
    
    Mat img(480, 640, CV_8UC3, Scalar(0,0,0));
    
    for (int r = 0; r < img.rows; r++) {
        for (int c = 0; c < img.cols; c++) {
            Vec3b px = img.at<Vec3b>(r,c);
            
            if (rng.next() * 1.0 / UINT_MAX <= 0.5) {
                px[0] = 255;
                px[1] = 255;
                px[2] = 255;
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
   
    imwrite("out/random_dots.jpg", img);
   
    return 0 ;
}
//
// end
//
