#include "ros/ros.h"
#include "geometry_msgs/Twist.h" // Motor Commands
#include "sensor_msgs/LaserScan.h" // Laser Data
#include "tf/transform_listener.h" // tf Tree
#include "std_msgs/String.h"
#include <iostream>
#include <cmath>
#include <algorithm>
#include <stack>
#include <utility>
#include <string>



sensor_msgs::LaserScan laser_msg;

float d_right;
float d_left;


ros::NodeHandle n;
ros::Subscriber laser_subscriber;
ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);


void laser_call(const sensor_msgs::LaserScan::ConstPtr& scan_msg){
    laser_msg = *scan_msg;
    std::vector<float> laser_ranges;
    laser_ranges = laser_msg.ranges;
    size_t range_size = laser_ranges.size();
    float range_min = laser_msg.range_max, range_max = laser_msg.range_min;
    int inf_count = 0;
    std_msgs::String msg;
    std::stringstream ss;
    std::string s = "This is messaAge #" + std::to_string(laser_msg.angle_increment) + "|";
    ss << s;
    msg.data = ss.str();
    //chatter_pub.publish(msg);
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "nodesex");
    // Subscribe to the /scan topic and call the laser_callback function
    laser_subscriber = n.subscribe("/laserscan", 1000, laser_call);

    // Enter an infinite loop where the laser_callback function will be called when new laser messages arrive
    ros::Duration time_between_ros_wakeups(0.001);
    while (ros::ok()) {
        ros::spinOnce();
        time_between_ros_wakeups.sleep();
    }

    return 0;
}