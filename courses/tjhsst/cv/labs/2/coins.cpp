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
    string fname;
    string arg;
    
    arg = argv[1];
    fname = "in/coins/" + arg + ".png";
    
    Mat img = imread(fname);
    Mat modf = img.clone();//imread(fname);
    
    if (img.channels() > 3) {
        // remove alpha channel
        cvtColor(img, img, COLOR_BGRA2BGR);
        cvtColor(modf, modf, COLOR_BGRA2BGR);
    }
        
    float thresh = 0.5f;
    float maxThresh = 8.0f;
    int amtPennies = 0;
    int amtNickels = 0;
    int amtDimes = 0;
    int amtQuarters = 0;
    vector<Point> pts;

    for (int i = 1; i < 3; i++) {
        Mat penny = imread(string("in/coins/templates/penny") + to_string(i) + ".png", IMREAD_UNCHANGED);
        Mat nickel = imread(string("in/coins/templates/nickel") + to_string(i) + ".png", IMREAD_UNCHANGED);
        Mat dime = imread(string("in/coins/templates/dime") + to_string(i) + ".png", IMREAD_UNCHANGED);
        
        Mat quarter = imread(string("in/coins/templates/quarter") + to_string(i) + ".png", IMREAD_UNCHANGED);
        Mat qmsk = imread(string("in/coins/templates/quarter") + to_string(i) + "_mask.png", IMREAD_UNCHANGED);
        
        Mat pmsk(penny.rows, penny.cols, CV_8UC3);
        for (int r = 0; r < penny.rows; r++) {
            for (int c = 0; c < penny.cols; c++) {
                if (penny.at<Vec4b>(r,c)[3] == 0) {
                    pmsk.at<Vec3b>(r,c) = Vec3b(0, 0, 0);
                } else {
                    pmsk.at<Vec3b>(r,c) = Vec3b(255, 255, 255);
                }
            }
        }
        
        Mat presult;
        
        cvtColor(penny, penny, COLOR_BGRA2BGR);
        
        matchTemplate(img, penny, presult, TM_SQDIFF, pmsk); // TM_SQDIFF_NORMED 
        double pMinVal;
        minMaxLoc(presult, &pMinVal, NULL, NULL, NULL, Mat());
        for (int y = 0; y < presult.rows; y++) {
            for (int x = 0; x < presult.cols; x++) {
                double score = presult.at<float>(y, x);
                
                if (score <= pMinVal+thresh && score < maxThresh) {
                    bool invalidPt = false;
                    for (Point pt : pts) {
                        int x2 = pt.x;
                        int y2 = pt.y;
                        
                        if ((x < x2+30 && x > x2-30) && (y < y2+30 && y > y2-30)) {
                            invalidPt = true;
                        } 
                    }
                    if (invalidPt) {
                        rectangle(modf, Point(x, y), Point(x + penny.cols, y + penny.rows), Scalar(0, 0, 0), 1);
                        amtPennies++;
                        pts.push_back(Point(x,y));
                    }
                }
            }
        }
            
        Mat nmsk = Mat(nickel.rows, nickel.cols, CV_8UC3);
        for (int r = 0; r < nickel.rows; r++) {
            for (int c = 0; c < nickel.cols; c++) {
                if (nickel.at<Vec4b>(r,c)[3] == 0) {
                    nmsk.at<Vec3b>(r,c) = Vec3b(0, 0, 0);
                } else {
                    nmsk.at<Vec3b>(r,c) = Vec3b(255, 255, 255);
                }
            }
        }
        
        Mat nresult;
        
        cvtColor(nickel, nickel, COLOR_BGRA2BGR);
        
        matchTemplate(img, nickel, nresult, TM_SQDIFF, nmsk);
        double nMinVal;
        minMaxLoc(nresult, &nMinVal, NULL, NULL, NULL, Mat());
        for (int y = 0; y < nresult.rows; y++) {
            for (int x = 0; x < nresult.cols; x++) {
                double score = nresult.at<float>(y, x);

                if (score <= nMinVal+thresh && score <= maxThresh) {
                    bool invalidPt = false;
                    for (Point pt : pts) {
                        int x2 = pt.x;
                        int y2 = pt.y;
                        
                        if ((x < x2+30 && x > x2-30) && (y < y2+30 && y > y2-30)) {
                            invalidPt = true;
                        } 
                    }
                    if (invalidPt) {
                        rectangle(modf, Point(x, y), Point(x + nickel.cols, y + nickel.rows), Scalar(0, 0, 0), 1);
                        amtNickels++;
                        pts.push_back(Point(x,y));
                    }
                }
            }
        }
            
        
        Mat dmsk = Mat(dime.rows, dime.cols, CV_8UC3);
        for (int r = 0; r < dime.rows; r++) {
            for (int c = 0; c < dime.cols; c++) {
                if (dime.at<Vec4b>(r,c)[3] == 0) {
                    dmsk.at<Vec3b>(r,c) = Vec3b(0, 0, 0);
                } else {
                    dmsk.at<Vec3b>(r,c) = Vec3b(255, 255, 255);
                }
            }
        }
        
        Mat dresult;
        
        cvtColor(dime, dime, COLOR_BGRA2BGR);
        
        matchTemplate(img, dime, dresult, TM_SQDIFF, dmsk);
        double dMinVal;
        minMaxLoc(dresult, &dMinVal, NULL, NULL, NULL, Mat());
        for (int y = 0; y < dresult.rows; y++) {
            for (int x = 0; x < dresult.cols; x++) {
                double score = dresult.at<float>(y, x);
                
                if (score <= dMinVal+thresh && score <= maxThresh) {
                    bool invalidPt = false;
                    for (Point pt : pts) {
                        int x2 = pt.x;
                        int y2 = pt.y;
                        
                        if ((x < x2+30 && x > x2-30) && (y < y2+30 && y > y2-30)) {
                            invalidPt = true;
                        } 
                    }
                    if (invalidPt) {
                        rectangle(modf, Point(x, y), Point(x + dime.cols, y + dime.rows), Scalar(0, 0, 0), 1);
                        amtDimes++;
                        pts.push_back(Point(x,y));
                    }
                }
            }
        }
        
        Mat qresult;
        
        cvtColor(quarter, quarter, COLOR_BGRA2BGR);
        cvtColor(qmsk, qmsk, COLOR_BGRA2BGR);
        
        matchTemplate(img, quarter, qresult, TM_SQDIFF, qmsk);
        double qMinVal;
        minMaxLoc(qresult, &qMinVal, NULL, NULL, NULL, Mat());
        for (int y = 0; y < qresult.rows; y++) {
            for (int x = 0; x < qresult.cols; x++) {
                double score = qresult.at<float>(y, x);
                
                if (score <= qMinVal+thresh && score <= maxThresh) {
                    bool invalidPt = false;
                    for (Point pt : pts) {
                        int x2 = pt.x;
                        int y2 = pt.y;
                        
                        if ((x < x2+30 && x > x2-30) && (y < y2+30 && y > y2-30)) {
                           invalidPt = true;
                        } 
                    }
                    if (invalidPt) {
                        rectangle(modf, Point(x, y), Point(x + quarter.cols, y + quarter.rows), Scalar(0, 0, 0), 1);
                        amtQuarters++;
                        pts.push_back(Point(x,y));
                    }
                }
            }
        }
            
    }
    
    // debug
//     cout << "Pennies: " << amtPennies << endl;
//     cout << "Nickels: " << amtNickels << endl;
//     cout << "Dimes: " << amtDimes << endl;
//     cout << "Quarters: " << amtQuarters << endl;
    // prod
    cout << amtPennies+(amtNickels*5)+(amtDimes*10)+(amtQuarters*25) << " " << arg << ".png" << endl;
    
    imwrite("out/coins/" + arg + ".png", modf);
    
    return 0;
}

//
// end
//
