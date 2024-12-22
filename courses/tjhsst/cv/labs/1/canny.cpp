#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <cmath>

using namespace std;
using namespace cv;

#define PI 3.14159265358979323846

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
    } if (img.channels() == 3) {
        cvtColor(img, img, COLOR_BGR2GRAY);
    }
    Mat edges(img.rows, img.cols, CV_8UC1, Scalar(255));
    int gMagnitude[img.rows][img.cols][2];
    int gStrength[img.rows][img.cols]; 
    
    int highThreshold = 110;
    int lowThreshold = 80;
    
    // gaussian blur
    double blur[3][3] = {
        {0.111, 0.111, 0.111},
        {0.111, 0.111, 0.111},
        {0.111, 0.111, 0.111}
    };
    
    for (int r = 1; r < img.rows-1; r++) {
        for (int c = 1; c < img.cols-1; c++) {
            double b0 = ((int)img.at<uchar>(r-1, c-1))*blur[0][0];
            double b1 = ((int)img.at<uchar>(r-1, c))*blur[0][1];
            double b2 = ((int)img.at<uchar>(r-1, c+1))*blur[0][2];
            double b3 = ((int)img.at<uchar>(r, c-1))*blur[1][0];
            double b4 = ((int)img.at<uchar>(r, c))*blur[1][1];
            double b5 = ((int)img.at<uchar>(r, c+1))*blur[1][2];
            double b6 = ((int)img.at<uchar>(r+1, c-1))*blur[2][0];
            double b7 = ((int)img.at<uchar>(r+1, c))*blur[2][1];
            double b8 = ((int)img.at<uchar>(r+1, c+1))*blur[2][2];

            double mag = b0+b1+b2+b3+b4+b5+b6+b7+b8;
            uchar m = mag;

            edges.at<uchar>(r, c) = m;
        }
     }

    // ------- canny -------
    
    int gx[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };
    int gy[3][3] = {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };
    
    for (int r = 1; r < img.rows-1; r++) {
        for (int c = 1; c < img.cols-1; c++) {
            int gx0 = ((int)img.at<uchar>(r-1, c-1))*gx[0][0];
            int gx1 = ((int)img.at<uchar>(r-1, c))*gx[0][1];
            int gx2 = ((int)img.at<uchar>(r-1, c+1))*gx[0][2];
            int gx3 = ((int)img.at<uchar>(r, c-1))*gx[1][0];
            int gx4 = ((int)img.at<uchar>(r, c))*gx[1][1];
            int gx5 = ((int)img.at<uchar>(r, c+1))*gx[1][2];
            int gx6 = ((int)img.at<uchar>(r+1, c-1))*gx[2][0];
            int gx7 = ((int)img.at<uchar>(r+1, c))*gx[2][1];
            int gx8 = ((int)img.at<uchar>(r+1, c+1))*gx[2][2];
            
            int gy0 = ((int)img.at<uchar>(r-1, c-1))*gy[0][0];
            int gy1 = ((int)img.at<uchar>(r-1, c))*gy[0][1];
            int gy2 = ((int)img.at<uchar>(r-1, c+1))*gy[0][2];
            int gy3 = ((int)img.at<uchar>(r, c-1))*gy[1][0];
            int gy4 = ((int)img.at<uchar>(r, c))*gy[1][1];
            int gy5 = ((int)img.at<uchar>(r, c+1))*gy[1][2];
            int gy6 = ((int)img.at<uchar>(r+1, c-1))*gy[2][0];
            int gy7 = ((int)img.at<uchar>(r+1, c))*gy[2][1];
            int gy8 = ((int)img.at<uchar>(r+1, c+1))*gy[2][2];
            
            int mag_x = gx0+gx1+gx2+gx3+gx4+gx5+gx6+gx7+gx8;
            int mag_y = gy0+gy1+gy2+gy3+gy4+gy5+gy6+gy7+gy8;
            int mag = abs(mag_x)+abs(mag_y);
            
            gStrength[r][c] = mag; 
            gMagnitude[r][c][0] = mag_y;
            gMagnitude[r][c][1] = mag_x;
        }
    }
      
    // non maximal suppression
    for (int r = 1; r < img.rows-1; r++) {
        for (int c = 1; c < img.cols-1; c++) {       
            int mag_y = gMagnitude[r][c][0];
            int mag_x = gMagnitude[r][c][1];
            int mag = gStrength[r][c];
            
            float angle = atan2(mag_y,mag_x);
            angle = angle * (180 / PI); // [-pi, pi] -> [-180, 180] rad to deg
            angle = fmod(angle, 360); // [-180, 180] -> [0, 360] normalized
            
            if (mag > highThreshold) {
                if (angle > 22.5 || angle < 67.5) {
                    // 1. closest to 45deg
                    if (mag < gStrength[r-1][c+1] || mag < gStrength[r+1][c-1]) {
                        gStrength[r][c] = 0;
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle > 67.5 || angle < 112.5) {
                    // 2. closest to 90deg
                    if (mag < gStrength[r-1][c] || mag < gStrength[r+1][c]) {
                        gStrength[r][c] = 0;
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle > 112.5 || angle < 157.5) {
                    // 3. closest to 135deg
                    if (mag < gStrength[r-1][c-1] || mag < gStrength[r+1][c+1]) {
                        gStrength[r][c] = 0;
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle > 157.5 || angle < 202.5) {
                    // closest to 180deg
                    if (mag < gStrength[r][c-1] || mag < gStrength[r][c+1]) {
                        gStrength[r][c] = 0;
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle > 202.5 || angle < 247.5) {
                    // closest to 225deg
                    if (mag < gStrength[r+1][c-1] || mag < gStrength[r-1][c+1]) {
                        gStrength[r][c] = 0;
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle > 247.5 || angle < 292.5) {
                    // closest to 270deg
                    if (mag < gStrength[r+1][c] || mag < gStrength[r-1][c]) {
                        gStrength[r][c] = 0;
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle > 292.5 || angle < 337.5) {
                    // closest to 315deg
                    if (mag < gStrength[r+1][c+1] || mag < gStrength[r-1][c-1]) {
                        gStrength[r][c] = 0;
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle > 337.5 || angle < 22.5) {
                    // closest to 0deg or 360deg
                    if (mag < gStrength[r][c-1] || mag < gStrength[r][c+1]) {
                        gStrength[r][c] = 0;
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                }
            } else {
                edges.at<uchar>(r,c) = 255;
            }
        }
    }
    
    // very bad hysteresis

    for (int r = 1; r < img.rows-1; r++) {
        for (int c = 1; c < img.cols-1; c++) {
            int mag = gStrength[r][c];
            
            if (mag >= highThreshold) {
                edges.at<uchar>(r,c) = 0;
            } else if (mag >= lowThreshold && mag < highThreshold) {
                if (gStrength[r-1][c-1] >= highThreshold ||
                    gStrength[r-1][c] >= highThreshold ||
                    gStrength[r-1][c+1] >= highThreshold ||
                    gStrength[r][c-1] >= highThreshold ||
                    gStrength[r][c+1] >= highThreshold ||
                    gStrength[r+1][c-1] >= highThreshold ||
                    gStrength[r+1][c] >= highThreshold ||
                    gStrength[r+1][c+1] >= highThreshold
                ) {
                    edges.at<uchar>(r,c) = 0;
                    gStrength[r][c] = highThreshold + 1;
                } else {
                    edges.at<uchar>(r,c) = 255;
                }
                
            } else {
                edges.at<uchar>(r,c) = 255;
            }
        }
    }
    
    imwrite("out/" + arg + "_canny.png", edges);
    
    return 0;
}
//
// end
//
