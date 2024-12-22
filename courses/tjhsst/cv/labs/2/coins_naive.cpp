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
    int step = 1;
    bool in_grid = false;
    
    if (argc > 1) {
        step = atoi(argv[1]);
        if (argc > 2) {
            // disregard whatever the second arg is
            in_grid = true;
        }
    }
    
    if (step == 1) {
        // generating random coins assortment
        
        RNG rng(time(NULL));
    
        Mat original = imread("in/coins.jpg");
        Mat img = imread("in/coins.jpg");    
        cvtColor(img, img, COLOR_BGR2GRAY);
        Mat modf(img.rows, img.cols, CV_8UC3, Scalar(255, 255, 255)); 

        for (int j = 0; j < 25; j++) {
            GaussianBlur(img, img, Size(3,3), 0);
        }

        vector<Vec3f> circles;
        HoughCircles(img, circles, HOUGH_GRADIENT, 2, 100);

        for (int j = 1; j < circles.size(); j++) {
            int s = int((rng.next() * 1.0 / UINT_MAX) * (circles.size()-j) + j);
            int jradius = cvRound(circles[j][2])+50;
            int sradius = cvRound(circles[s][2])+50;

            for (int r = 0; r < jradius*2; r++) {
                for (int c = 0; c < jradius*2; c++) {
                    int x = int(circles[s][0]-jradius+c)%img.cols;
                    int y = int(circles[s][1]-jradius+r)%img.rows;
                    int ox = int(circles[j][0]-jradius+c)%img.cols;
                    int oy = int(circles[j][1]-jradius+r)%img.rows;
                    modf.at<Vec3b>(y,x) = original.at<Vec3b>(oy, ox);
               }
            }

            for (int r = 0; r < sradius*2; r++) {
                for (int c = 0; c < sradius*2; c++) {
                    int x = int(circles[j][0]-sradius+c)%img.cols;
                    int y = int(circles[j][1]-sradius+r)%img.rows;
                    int ox = int(circles[s][0]-sradius+c)%img.cols;
                    int oy = int(circles[s][1]-sradius+r)%img.rows;
                    modf.at<Vec3b>(y,x) = original.at<Vec3b>(oy, ox);
               }
            }  
        }

        imwrite("out/coins.png", modf);
    } else if (step == 2) {
        // counting coins
        int amt_of_nickels = 0;
        int amt_of_dimes = 0;
        int amt_of_pennies = 0;
        int amt_of_quarters = 0;
        
        if (in_grid) {
            // todo: add impl for non-gridded coins
        } else {
           int num_right = 0;
           int num_amt = 0;
           int num_errors = 0;
           // really ugly; from coins_in_grid.txt; i cba to read a txt file in c++
           int answers[] = {81 , 77 , 52 , 90 , 80 , 91 , 52 , 121, 48 , 115, 49 , 76 , 110, 101, 56 , 14 , 95 , 93 , 78 , 32 , 110, 125, 86 , 91 , 91 , 82 , 96 , 125, 76 , 108, 26 , 62 , 81 , 52 , 67 , 75 , 33 , 41 , 59 , 67 , 116, 67 , 101, 105, 19 , 105, 37 , 49 , 44 , 86 , 68 , 56 , 97 , 117, 115, 53 , 97 , 97 , 105, 58 , 116, 36 , 82 , 101, 28 , 28 , 63 , 81 ,72 , 89 , 38 ,43, 76 ,42 ,137,77 ,93 ,100,110,141,71 ,21 ,71 ,120,72 ,100,82 ,57 , 57 ,107,54 ,57 ,69 , 65 , 97 , 28 , 19 , 97 , 101, 72};
            
           for (int i = 0; i < 100; i++) {
                string test_case;
                if (i < 10) {
                    test_case = string("in/coins/grid/case000") + to_string(i) + ".png";
                } else {
                    test_case = string("in/coins/grid/case00") + to_string(i) + ".png";
                }
                Mat colored = imread(test_case);
                Mat grayscale = imread(test_case);
                cvtColor(grayscale, grayscale, COLOR_BGR2GRAY);
                
                for (int r = 0; r < grayscale.rows; r++) {
                    for (int c = 0; c < grayscale.cols; c++) {
                        int px = (int)grayscale.at<uchar>(r,c);
                        
                        if (px < 245) {
                            grayscale.at<uchar>(r,c) = 0;
                        } else {
                            grayscale.at<uchar>(r,c) = 255;
                        }
                    }
                }
                
                for (int j = 0; j < 25; j++) {
                    GaussianBlur(grayscale, grayscale, Size(3,3), 0);
                } 
                
                vector<Vec3f> circles;
                HoughCircles(grayscale, circles, HOUGH_GRADIENT, 2, 100);
                
                int radii[circles.size()];
                
                for (int i = 0; i < circles.size(); i++) {
                    int radius = cvRound(circles[i][2]);
                    radii[i] = radius;
                }
                
                int min_radius = 10000;
                int max_radius = 0;
                for (int i = 0; i < circles.size(); i++) {
                    if (radii[i] < min_radius) {
                        min_radius = radii[i];
                    }
                    if (radii[i] > max_radius) {
                        max_radius = radii[i];
                    }
                }
               
               for (int i = 0; i < circles.size(); i++) {
                   if (radii[i] == min_radius || (radii[i] > min_radius-5 && radii[i] < min_radius+5)) {
                       // dime
                       amt_of_dimes += 1;
                   } else if (radii[i] == max_radius || (radii[i] > max_radius-5 && radii[i] < max_radius+5)) {
                       // quarter
                       amt_of_quarters += 1;
                   } else if (abs(radii[i]-max_radius) < abs(radii[i]-min_radius)) {
                       // nickel
                       amt_of_nickels += 1;
                   } else if (abs(radii[i]-max_radius) > abs(radii[i]-min_radius)) {
                       // penny
                       amt_of_pennies += 1;
                   } else {
                        // this should probably never happen, but i don't know a better way to do this
                        // so i shall just increment the amount that provides the lowest possible error
                        // which is pennies (1)
                       amt_of_pennies += 1;
                   }
               }
               
               int answer = (amt_of_quarters*25 + amt_of_dimes*10 + amt_of_nickels*5 + amt_of_pennies);
               cout << "AMT: " << answer << endl; 
               cout << "\tQUARTERS:" << amt_of_quarters << endl;
               cout << "\tDIMES:" << amt_of_dimes << endl;
               cout << "\tNICKELS:" << amt_of_nickels << endl;
               cout << "\tPENNIES:" << amt_of_pennies << endl;
               if (answers[i] == answer) {
                   cout << "CHECKING WITH ANSWERS... " << "AC" << endl;
                   num_right++;
               } else {
                   cout << "CHECKING WITH ANSWERS... " << "WA: ERROR OF " << abs(answers[i]-answer) << endl; 
                   num_errors += abs(answers[i]-answer);
               }
               num_amt += answers[i];
               cout << "<-->" << endl;
               
               amt_of_quarters = 0;
               amt_of_dimes = 0;
               amt_of_nickels = 0;
               amt_of_pennies = 0;
            }
            
            cout << "RIGHT/ALL: " << num_right << "/" << "100" << endl;
            cout << "ERRORS/ALL: " << num_errors << "/" << num_amt << endl;
        }
    }
    
    return 0;
}

//
// end
//
