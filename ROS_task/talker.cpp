#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/String.h"
#include <queue>
#include <string>

using namespace std;
int key = 2;

string encrypt_data(string &s){
    int len = s.size();
    char ch;
    for(int i = 0; s[i] != '\0'; ++i){
        ch = s[i];
        if (ch >= 'a' && ch <= 'z'){
            ch = ch + key;
            if (ch > 'z') {
               ch = ch - 'z' + 'a' - 1;
            }  
            s[i] = ch;
        }
        else if (ch >= 'A' && ch <= 'Z'){
            ch = ch + key;
            if (ch > 'Z'){
               ch = ch - 'Z' + 'A' - 1;
            }
            s[i] = ch;
         }
    }
    return s;
}

int main(int argc, char **argv){
    ros::init(argc, argv, "talker");
    ros::NodeHandle n;
    ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
    ros::Publisher key_pub = n.advertise<std_msgs::String>("key", 10);
    ros::Rate loop_rate(10);
    int count = 0;
    queue<string> msg_q;
  while (ros::ok())
  {
    std_msgs::String msg;
    std::stringstream ss;
    std_msgs::String msg2;
    std::stringstream ss2;
    std::string s2 = to_string(key);
    ss2 << s2;
    msg2.data = ss2.str();
    key_pub.publish(msg2);
    if(msg_q.size() < 10){
        std::string s = "This is message #" + std::to_string(count) + "|"; 
        std::string enc_s = encrypt_data(s);
        msg_q.push(enc_s);
    }
    if(msg_q.size() == 10){
        std::string s = "";
        while(!msg_q.empty()) {
            s = s + msg_q.front();
            msg_q.pop();
            //cout << msg_q.front();
            //cout << "\n";
        }
        ss << s;
        msg.data = ss.str();
        ROS_INFO("%s", msg.data.c_str());
        chatter_pub.publish(msg);
    }
    //ss << "hello world " << count;
    //msg.data = ss.str();
    //ROS_INFO("%s", msg.data.c_str());
    //chatter_pub.publish(msg);std::string s = "";
    ros::spinOnce();
    loop_rate.sleep();
    ++count;
  }
  return 0;
}