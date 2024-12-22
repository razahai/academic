#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>

using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{
    string fname;
    string arg;
    
    arg = argv[1];
    fname = "in/" + arg + ".png";
    
    Mat img = imread(fname, IMREAD_UNCHANGED);
    
    if (img.channels() > 3) {
        // remove alpha channel
        cvtColor(img, img, COLOR_BGRA2BGR);
    }
    
    if (img.channels() == 3) {
        cvtColor(img, img, COLOR_BGR2GRAY);
    }
    Mat blur(img.rows, img.cols, CV_8UC1, Scalar(0));
    
    double kernel[3][3] = {
        {0.0625, 0.125, 0.0625},
        {0.125, 0.25, 0.125},
        {0.0625, 0.125, 0.0625}
    };
     
    for (int r = 1; r < img.rows-1; r++) {
        for (int c = 1; c < img.cols-1; c++) {
            double k0 = ((int)img.at<uchar>(r-1, c-1))*kernel[0][0];
            double k1 = ((int)img.at<uchar>(r-1, c))*kernel[0][1];
            double k2 = ((int)img.at<uchar>(r-1, c+1))*kernel[0][2];
            double k3 = ((int)img.at<uchar>(r, c-1))*kernel[1][0];
            double k4 = ((int)img.at<uchar>(r, c))*kernel[1][1];
            double k5 = ((int)img.at<uchar>(r, c+1))*kernel[1][2];
            double k6 = ((int)img.at<uchar>(r+1, c-1))*kernel[2][0];
            double k7 = ((int)img.at<uchar>(r+1, c))*kernel[2][1];
            double k8 = ((int)img.at<uchar>(r+1, c+1))*kernel[2][2];
            
            double mag = k0+k1+k2+k3+k4+k5+k6+k7+k8;
            uchar m = mag;
             
            blur.at<uchar>(r, c) = m;
        }
     }
    
    imwrite("out/" + arg + "_gaussian_blur.png", blur);
    
    return 0;
}
//
// end
//
