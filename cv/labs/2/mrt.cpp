#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <fstream>
#include <cmath>

using namespace std;
using namespace cv;

// literally stolen from https://stackoverflow.com/questions/447206/c-isfloat-function
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
                    
                    cout << x << " " << y << endl;
                    coords.push_back(cds);
                    
                    x = stof(coord);
                    y = nanf("");
                }
            }
        }
    }
    
    float cx = 200;
    float cy = 190;
    float rad = 0;
    
    Mat img(380, 400, CV_8UC3, Scalar(255, 255, 255));
    
    for (auto& coord : coords) {
        rad = sqrt((coord.first * coord.first) + (coord.second * coord.second));
        cx += coord.first;
        cy += coord.second;
    }
    
    cout << 1 << ": (" << cx << ", " << cy << ")" << endl; 
    
    pair<float, float> first_point = make_pair(cx, cy);
    pair<float, float> prev_point = make_pair(cx, cy);
    int m = 0;
    int n = 1; // for indexing
    
    // rest of the points
    for (int i = 1; i < 1541; i++) {
        cx = 200;
        cy = 190;
        
        // point i
        for (auto& coord : coords) {
            rad = sqrt((coord.first * coord.first) + (coord.second * coord.second));
            float t = atan2(coord.second, coord.first); // atan2(dy,dx)
            t += i*m*((2*M_PI)/1541);
            
            float c_dx = rad * cos(t); // dx = rcos(theta)
            float c_dy = rad * sin(t); // dy = rsin(theta)
            
            cx += c_dx;
            cy += c_dy;
            
            if (n % 2 == 0) {
                m *= -1;
            } else {
                m += (2*abs(m))+1;
            }
            n += 1;
        }
        
        m = 0;
        n = 1;
        
//         cout << i+1 << ": (" << cx << ", " << cy << ")" << endl;
        
        // make line between point_i-1 and point_i
        line(img, Point(prev_point.first, prev_point.second), Point(cx, cy), Scalar(255, 0, 0), 1, LINE_AA);
        prev_point = make_pair(cx, cy);
    }
    
    // 1541 to 1
    line(img, Point(prev_point.first, prev_point.second), Point(first_point.first, first_point.second), Scalar(255, 0, 0), 1, LINE_AA);
    
    imwrite("out/mrt.png", img);
    
    return 0;
}
