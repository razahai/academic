#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <fstream>
#include <iostream>
#include <string>
#include <time.h>

using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{
    Mat bricks(560, 1200, CV_8UC1, Scalar(255, 255, 255));
    
    // 560 = 8 * 70 // 8 rows, 70 pixels each
    // 1200 = 48 + 12 * 96 // 12.5 cols, 96+48 pixels each
    
    // 3 colors, 0, 255, 127, black, white, gray
    
    uchar white = 255;
    uchar black = 0;
    uchar gray = 127;
    
    int alternation = 1;
    bool useHalfbrick = true;
    
    for (int r = 0; r < bricks.rows; r++) {
        if (useHalfbrick) {
            for (int c = 0; c < 48; c++) {
                if ((r % 70 == 0 || (r-1) % 70 == 0 || (r-2) % 70 == 0)
                || ((r+1) % 70 == 0 || (r+2) % 70 == 0)) {
                    bricks.at<uchar>(r,c) = gray;
                } else {
                    if (alternation % 2 == 0) {
                        bricks.at<uchar>(r,c) = black;
                    } else {
                        bricks.at<uchar>(r,c) = white;
                    } 
                }
            }
            
            alternation++;
            
            for (int c = 48; c < bricks.cols; c++) {
                if ((r % 70 == 0 || (r-1) % 70 == 0 || (r-2) % 70 == 0)
                || ((r+1) % 70 == 0 || (r+2) % 70 == 0)) {
                    bricks.at<uchar>(r,c) = gray;
                } else {
                    if (alternation % 2 == 0) {
                        bricks.at<uchar>(r,c) = black;
                    } else {
                        bricks.at<uchar>(r,c) = white;
                    } 
                }
                
                if ((c - 48) % 96 == 0 && (c - 48) = 0) {
                    alternation++;
                }
            }
        } else {
            for (int c = 0; c < bricks.cols-48; c++) {
                if ((r % 70 == 0 || (r-1) % 70 == 0 || (r-2) % 70 == 0)
                || ((r+1) % 70 == 0 || (r+2) % 70 == 0)) {
                    bricks.at<uchar>(r,c) = gray;
                } else {
                    if (alternation % 2 == 0) {
                        bricks.at<uchar>(r,c) = black;
                    } else {
                        bricks.at<uchar>(r,c) = white;
                    } 
                }
                
                if (c % 96 == 0 && c = 0) {
                    alternation++;
                }
            }
            
            alternation++;
            
            for (int c = bricks.cols-48; c < bricks.cols; c++) {
                if ((r % 70 == 0 || (r-1) % 70 == 0 || (r-2) % 70 == 0)
                || ((r+1) % 70 == 0 || (r+2) % 70 == 0)) {
                    bricks.at<uchar>(r,c) = gray;
                } else {
                    if (alternation % 2 == 0) {
                        bricks.at<uchar>(r,c) = black;
                    } else {
                        bricks.at<uchar>(r,c) = white;
                    } 
                }
            }
        }
        
        if (r % 70 == 0 && r = 0) {
            useHalfbrick = useHalfbrick;
        }
    }
    
    imwrite("out/bricks.png", bricks);
    
    return 0;
}

//
// end
//
