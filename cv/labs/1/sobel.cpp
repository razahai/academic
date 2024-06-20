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
    int gs[img.rows][img.cols]; 
    int gmag[img.rows][img.cols][2];
    
    /*
    *     [ 1, 1, 1 ]
    * 1/9 [ 1, 1, 1 ]
    *     [ 1, 1, 1 ]
    */
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
            
            gs[r][c] = mag;
            gmag[r][c][0] = mag_y;
            gmag[r][c][1] = mag_x;
        }
    }
    
    // possibly a better way to do this, but to check the diag option, all Gs have to be computed so we
    // have to go through the entire image once more
    
    for (int r = 1; r < img.rows-1; r++) {
        for (int c = 1; c < img.cols-1; c++) {
            int mag_y = gmag[r][c][0];
            int mag_x = gmag[r][c][1];
            int mag = gs[r][c];
            
            float angle = atan2(mag_y,mag_x);
            float angle_r2d = angle * (180 / PI); // [-pi, pi] -> [-180, 180] rad to deg
            float angle_nz = fmod(angle_r2d, 360); // [-180, 180] -> [0, 360] normalized
            
            if (mag > 110) {
                if (angle_nz > 22.5 || angle_nz < 67.5) {
                    // 1. closest to 45deg
                    if (mag < gs[r-1][c+1] || mag < gs[r+1][c-1]) {
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle_nz > 67.5 || angle_nz < 112.5) {
                    // 2. closest to 90deg
                    if (mag < gs[r-1][c] || mag < gs[r+1][c]) {
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle_nz > 112.5 || angle_nz < 157.5) {
                    // 3. closest to 135deg
                    if (mag < gs[r-1][c-1] || mag < gs[r+1][c+1]) {
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle_nz > 157.5 || angle_nz < 202.5) {
                    // closest to 180deg
                    if (mag < gs[r][c-1] || mag < gs[r][c+1]) {
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle_nz > 202.5 || angle_nz < 247.5) {
                    // closest to 225deg
                    if (mag < gs[r+1][c-1] || mag < gs[r-1][c+1]) {
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle_nz > 247.5 || angle_nz < 292.5) {
                    // closest to 270deg
                    if (mag < gs[r][c-1] || mag < gs[r][c+1]) {
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle_nz > 292.5 || angle_nz < 337.5) {
                    // closest to 315deg
                    if (mag < gs[r+1][c+1] || mag < gs[r-1][c-1]) {
                        edges.at<uchar>(r,c) = 255;
                    } else {
                        edges.at<uchar>(r,c) = 0;
                    }
                } else if (angle_nz > 337.5 || angle_nz < 22.5) {
                    // closest to 0deg or 360deg
                    if (mag < gs[r][c-1] || mag < gs[r][c+1]) {
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
    
    imwrite("out/" + arg + "_sobel_edges_wa.png", edges);
    
    return 0;
}
//
// end
//
