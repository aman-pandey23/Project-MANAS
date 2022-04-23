#include "ros/ros.h"
#include "std_msgs/String.h"
#include <queue>
#include <string>
#include <cstring>  

using namespace std;
int key;

string decrypt_data(string &s){
  char ch;
  for(int i = 0; s[i] != '\0'; ++i) {
    ch = s[i];
    //decrypt for lowercase letter
    if(ch >= 'a' && ch <= 'z') {
      ch = ch - key;
      if(ch < 'a'){
        ch = ch + 'z' - 'a' + 1;
      }
      s[i] = ch;
    }
    //decrypt for uppercase letter
    else if(ch >= 'A' && ch <= 'Z') {
      ch = ch - key;
      if(ch < 'A') {
        ch = ch + 'Z' - 'A' + 1;
      }
      s[i] = ch;
    }
  }
  return s;
}

void printData(string &s){
  string delim = "|"; // delimiter  
  size_t pos = 0;  
  string token1; // define a string variable  
  while (( pos = s.find (delim)) != std::string::npos){  
    token1 = s.substr(0, pos); // store the substring    
    ROS_INFO("%s",token1.c_str());
    s.erase(0, pos + delim.length());  /* erase() function store the current positon and move to next token. */   
  }  
  ROS_INFO("%s",s.c_str());
}  

void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
  std::string rec = msg->data.c_str();
  std::string dec_s = decrypt_data(rec);
  printData(dec_s);
}
void keyCallback(const std_msgs::String::ConstPtr& msg)
{
  std::string dec_key = msg->data.c_str();
  key = stoi(dec_key);
}


int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");


  ros::NodeHandle n;
  ros::Subscriber sub_k = n.subscribe("key", 10, keyCallback);
  ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallback);

  ros::spin();

  return 0;
}