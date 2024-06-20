//
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
//
#include <iostream>
//
using namespace std;
using namespace cv;
//
int main(int argc, char* argv[])
{
    RNG rng(100000);
    
    string fname;
    
    Mat img(480, 640, CV_8UC3, Scalar(0,0,0));
    Mat silhouette;
   
    fname = "seahorse";
    // fname = "seahorse"
    // fname = "teapot"
    // fname = "cat"    ;
   
    silhouette = imread("in/" + fname + ".pbm", IMREAD_UNCHANGED);
   
    //identical dots
    for (int r = 0; r < img.rows; r++) {
        for (int c = 0; c < img.cols; c++) {
            Vec3b px = img.at<Vec3b>(r,c);
            
            if (c > 160) {
                
                if (silhouette.at<uchar>(r,c-160) == 0) {
                    px = img.at<Vec3b>(r,(c-160)+5);
                } else {
                    px = img.at<Vec3b>(r,c-160);
                }
            } else {
                if (rng.next() * 1.0 / UINT_MAX <= 0.5) {
                    px = Vec3b(255, 255, 255);
                }
            }

             img.at<Vec3b>(r,c) = px;
         }
    }
    
    imwrite("out/" + fname + ".png", img);
   
    return 0;
}
//
// end
//
