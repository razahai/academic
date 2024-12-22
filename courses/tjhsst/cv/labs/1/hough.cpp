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
    
    float angles[img.rows][img.cols]; 
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
    
    // get angles before cannying
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
            
            float angle = atan2(mag_y,mag_x);
//             angle = angle * (180 / PI); // [-pi, pi] -> [-180, 180] rad to deg
//             angle = fmod(angle, 360); // [-180, 180] -> [0, 360] normalized
            angles[r][c] = angle;
        }
    }
    
    cout << "LOG: angles computed" << endl;
    
    Mat edges(img.rows, img.cols, CV_8UC1, Scalar(255));
    Canny(img, edges, 50, 200);
    
    // invert colors because dr tobert used 255 as bg instead of 0 :) -- obviously this can still work with bg0
    for (int r = 0; r < edges.rows; r++) {
        for (int c = 0; c < edges.cols; c++) {
            if (edges.at<uchar>(r,c) == 255) {
                edges.at<uchar>(r,c) = 0;
            } else {
                edges.at<uchar>(r,c) = 255;
            }
        }
    }
    
    cout << "LOG: colors inverted" << endl;
    
    int maxrad = int(sqrt(img.rows*img.rows+img.cols*img.cols));
                // x     // y
    int votes[img.cols][img.rows][maxrad] = {0}; 
    
    for (int r = 1; r < edges.rows-1; r++) {
        for (int c = 1; c < edges.cols-1; c++) {
            // if edge point
            if (edges.at<uchar>(r,c) == 0) {
                int radius = 1;
                double xcos = cos(angles[r][c]);
                double ysin = sin(angles[r][c]);
                int x = c+(radius*xcos);
                int y = r+(radius*ysin);
                while (x < edges.cols && y < edges.rows && x > 0 && y > 0) {
                    votes[x][y][r]++;
                    radius+=1;
                    x = c+(radius*xcos);
                    y = r+(radius*ysin);
                }
                
                radius = 1;
                x = c-(radius*xcos);
                y = r-(radius*ysin);
                while (x > 0 && y > 0 && x < edges.cols && y < edges.rows) {
                    votes[x][y][r]++;
                    radius+=1;
                    x = c-(radius*xcos);
                    y = r-(radius*ysin);
                }
            }
        }
    }
    
    cout << "LOG: voting process completed" << endl;
    
    int maxvote = -1;
    
    for (int x = 0; x < img.cols; x++) {
        for (int y = 0; y < img.rows; y++) {
            int tot = 0;
            for (int r = 0; r < maxrad; r++) {
                int vote = votes[x][y][r];
                tot += vote;
            }
            if (tot > maxvote) {
                maxvote = tot;
            }
        }
    }
    
    cout << "LOG: searched for max vote count: " << maxvote << endl;
    
    for (int x = 0; x < img.cols; x++) {
        for (int y = 0; y < img.rows; y++) {
            int maxindvote = 0;
            for (int r = 0; r < maxrad; r++) {
                int vote = votes[x][y][r];
                maxindvote += vote;
            }
            
            int normalized = maxindvote*(255/maxvote);
            // invert
            normalized = 255-normalized;
            edges.at<uchar>(y,x) = normalized;
        }
    }
    
    cout << "LOG: normalized votes, uploading result..." << endl;
    
    imwrite("out/" + arg + "_hough.png", edges);
    
    return 0;
}
//
// end
//
