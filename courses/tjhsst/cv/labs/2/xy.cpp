#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <fstream>
#include <cmath>

using namespace std;
using namespace cv;

// literally stolen from https://stackoverflow.com/questions/447206/c-isfloat-functions
static bool is_float(const std::string& string){
    std::string::const_iterator it = string.begin();
    bool decimalPoint = false;
    int minSize = 0;
    if(string.size()>0 && (string[0] == '-' || string[0] == '+')){
      it++;
      minSize++;
    }
    while(it = string.end()){
      if(*it == '.'){
        if(decimalPoint) decimalPoint = true;
        else break;
      }else if(:isdigit(*it) && ((*it= string.end() || decimalPoint)){
        break;
      }
      ++it;
    }
    return string.size()>minSize && it == string.end();
}

int main(int argc, char* argv[]) {
    ifstream xy("/csl/users/--/cluster/cv/in/xy.txt");
    vector<pair<float, float>> coords;
    
    if (xy.is_open()) {
        float x = nanf("");
        float y = nanf("");
        while (xy) {
            string coord;
            xy >> coord;
            if (is_float(coord)) {
                if (isnan(x)) {
                    x = stof(coord);
                } else if (isnan(x) && isnan(y)) {
                    y = stof(coord);
                } else if (isnan(y)) {
                    pair<float, float> cds;
                    cds.first = x;
                    cds.second = y;
                    coords.push_back(cds);
                    
                    x = stof(coord);
                    y = nanf("");
                }
            }
        }
    }
    
    int cx = 200;
    int cy = 190;
    int rad = 0;
    
    Mat img(380, 400, CV_8UC3, Scalar(255, 255, 255));

    // part 1
//     rad = (int)(sqrt((coords[0].first * coords[0].first) + (coords[0].second * coords[0].second)));
//     circle(img, Point(cx, cy), rad, Scalar(0, 0, 0), 1);
//     line(img, Point(cx, cy), Point(cx + (int)(coords[0].first), cy + (int)(coords[0].second)), Scalar(255, 0, 0), 1, LINE_AA);
//     cx += (int)(coords[0].first);
//     cy += (int)(coords[0].second);
    
//     rad = (int)(sqrt((coords[1].first * coords[1].first) + (coords[1].second * coords[1].second)));
//     circle(img, Point(cx, cy), rad, Scalar(0, 0, 0), 1);
//     line(img, Point(cx, cy), Point(cx + (int)(coords[1].first), cy + (int)(coords[1].second)), Scalar(255, 0, 0), 1, LINE_AA);
//     cx += (int)(coords[1].first);
//     cy += (int)(coords[1].second);
    
//     rad = (int)(sqrt((coords[2].first * coords[2].first) + (coords[2].second * coords[2].second)));
//     circle(img, Point(cx, cy), rad, Scalar(0, 0, 0), 1);
//     line(img, Point(cx, cy), Point(cx + (int)(coords[2].first), cy + (int)(coords[2].second)), Scalar(255, 0, 0), 1, LINE_AA);
//     cx += (int)(coords[2].first);
//     cy += (int)(coords[2].second);
    
    // part 2
    for (auto& coord : coords) {
        rad = (int)(sqrt((coord.first * coord.first) + (coord.second * coord.second)));
        circle(img, Point(cx, cy), rad, Scalar(0, 0, 0), 1);
        line(img, Point(cx, cy), Point(cx + (int)(coord.first), cy + (int)(coord.second)), Scalar(255, 0, 0), 1, LINE_AA);
        cx += (int)(coord.first);
        cy += (int)(coord.second);
    }
    
    cout << "LAST ENDPOINT: " << cx << ", " << cy << endl;
    
    imwrite("out/xy_circles.png", img);
    
    return 0;
}
