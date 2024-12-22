#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <fstream>
#include <map>

using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{    
    RNG rng(100000);
    
    string fname;
    
    Mat grayscale;
   
    int step = 1;
    
    fname = "vader";
    //fname = "yoda";
    //fname = "wolf";
    //fname = "parrot"; // custom
    
    if (argc > 1) {
        step = atoi(argv[1]);
        fname = argv[2];
    }
    
    int white = 0;
    int black = 0;
    
    grayscale = imread("in/" + fname + ".png", IMREAD_UNCHANGED);
    Mat img(grayscale.rows, grayscale.cols, CV_8UC3, Scalar(0,0,0));
    
    Mat blue = imread("in/blue_noise.pgm", IMREAD_UNCHANGED);
    
    if (step == 3) {
        int size = 256, hist_width = 1024, hist_height = 400, offset = 50;
        Mat hist_img(hist_height+offset, hist_width+offset, CV_8UC3, Scalar(255, 255, 255));
        int bin_width = cvRound((double)hist_width/size);
        
        // axis lines
        line(hist_img,
             Point(offset-10,
                   hist_height+(offset-40)),
             Point(hist_width+offset,
                   hist_height+(offset-40)), 
             Scalar(0, 0, 0), 2);
        line(hist_img, Point(offset-10, hist_height+(offset-40)), Point(offset-10, 0), Scalar(0, 0, 0), 2);
        
        // x-axis
        putText(hist_img, "0", Point(offset-30, hist_height+(offset-10)), FONT_HERSHEY_DUPLEX, 0.8, Scalar(0,0,0), 1);
        
        int x_axis = 85;
        for (int i = 358; i < hist_width+offset; i+=(hist_width+offset)/3) {
            putText(hist_img, to_string(x_axis), Point(i, hist_height+(offset-10)), FONT_HERSHEY_DUPLEX, 0.8, Scalar(0,0,0), 1);
            x_axis+=85;
        }
        putText(hist_img,
                to_string(x_axis),
                Point(hist_width-10,
                      hist_height+(offset-10)),
                FONT_HERSHEY_DUPLEX, 0.8,
                Scalar(0,0,0),
                1);
        
        // ..
        double histogram[256];
        
        for (int r = 0; r < grayscale.rows; r++) {
            for (int c = 0; c < grayscale.cols; c++) {
                int px = (int)grayscale.at<uchar>(r, c);
                
                histogram[px]++;
            }
        }
        
        int total = grayscale.rows*grayscale.cols;
        double* max = max_element(begin(histogram), end(histogram));
        double max_element = *max/total;
        double norm = (double)100/max_element;
        
        for (auto& val : histogram) {
            val = (val/total)*norm*(hist_height/100);
        }
        
        for (int i = 1; i < size; i++) {
            line(hist_img, Point(offset+bin_width*(i-1), hist_height - cvRound(histogram[i-1])),
            Point(offset+bin_width*(i), hist_height - cvRound(histogram[i])),
            Scalar(0, 0, 0), 1, 8, 0);
        }
        
        // y-axis
        int y_axis = cvRound(max_element*100);
        
        for (int i = offset; i < hist_height; i+=(hist_height)/3) {
            putText(hist_img,
                    to_string(y_axis),
                    Point(
                        offset-(y_axis >= 10 ? 52 : 35), // weird
                        i+(y_axis/3 == 0 
                           && y_axis = cvRound(max_element*100)
                           && i < hist_height+offset-(hist_height/3)-1 ? hist_height/3/2 : 0)
                    ),
                    FONT_HERSHEY_DUPLEX,
                    0.8,
                    Scalar(0,0,0),
                    1);
            if (y_axis/3 == 0) break;
            y_axis/=3;
        }
    
        imwrite("out/" + fname + "_histogram.png", hist_img);
        
        // opencv doc (only using the drawing method since calcHist doesn't provide %)
        //https://docs.opencv.org/3.4/d8/dbc/tutorial_histogram_calculation.html
        return 0;
    }
    
    int blue_noise_map[64][64];  

    if (step == 4) {
        for (int i = 0; i < sizeof(blue_noise_map[0])/sizeof(int); i++) {
            for (int j = 0; j < sizeof(blue_noise_map[0])/sizeof(int); j++) {
                blue_noise_map[i][j] = (int)blue.at<uchar>(i, j);
            }
        }
    }
    
    for (int r = 0; r < img.rows; r++) {
        for (int c = 0; c < img.cols; c++) {
            Vec3b px = img.at<Vec3b>(r,c);
            int g_px = (int)grayscale.at<uchar>(r, c);
            int random = step == 1 ? 128 : step == 4 ? blue_noise_map[r%64][c%64] : rng.uniform(0,256);
            
            if (g_px < random) {
                px = Vec3b(0, 0, 0);
                black++;
            } else {
                px = Vec3b(255, 255, 255);
                white++;
            }
            
            img.at<Vec3b>(r,c) = px;
         }
    }
    
    imwrite("out/" + fname + (step == 1 ? ".png" : step == 4 ? "_random_blue.png" : "_random.png"), img);
    
    double wrat = 1.0*white / (black + white);
    double brat = 1.0*black / (black + white);
    
    ofstream ratios("out/" + fname + (step == 1 ? "_ratios_dithering.txt" : step == 4 ? "_ratios_dithering_random_blue.txt": "_ratios_dithering_random.txt"));
    
    ratios << "White: " << wrat << "\n";
    ratios << "Black: " << brat;
    
    ratios.close();
    
    return 0;
}

//
// end
//
