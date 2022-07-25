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
#include <stdlib.h>

sensor_msgs::LaserScan laser_msg;
geometry_msgs::Twist vel_msg;

float d_right;
float d_left;
float xvel = 0.0;
float setvel = 0.7;

class PID {
  public:
    /// @param  kp  Proportional gain   @f$ K_p @f$
    /// @param  ki  Integral gain       @f$ K_i @f$
    /// @param  kd  Derivative gain     @f$ K_d @f$
    /// @param  fc  Cutoff frequency    @f$ f_c @f$ of derivative filter in Hz
    /// @param  Ts  Controller sampling time    @f$ T_s @f$ in seconds
    /// The derivative filter can be disabled by setting `fc` to zero.
    PID(float kp, float ki, float kd, float Ts)
        : kp(kp), ki(ki), kd(kd), Ts(Ts) {}

    /// Update the controller with the given position measurement `meas_y` and 
    /// return the new control signal.
    float update(float reference, float meas_y) {
        // e[k] = r[k] - y[k], error between setpoint and true position
        float er = meas_y - reference;
        // e_d[k] = (e_f[k] - e_f[k-1]) / Tₛ, filtered derivative
        float derivative = (er - old_er) / Ts;

        
        std::cout << " | integral: ";
        std::cout << integral;
        std::cout << " | ";
        

        // e_i[k+1] = e_i[k] + Tₛ e[k], integral
        float new_integral = integral + (er * Ts);                                       // |Quarantined code
         
        // PID formula:
        // u[k] = Kp e[k] + Ki e_i[k] + Kd e_d[k], control signal

        float control_u = (kp * er) + (ki * integral) + (kd * derivative);

        // store the state for the next iteration
        integral = new_integral;                                                           //|Quarantined code
        old_er = er;
        // return the control signal
        //std::cout << control_u;

        if(isnan(control_u)){
          control_u = 0;
        }
        if (xvel < setvel)
        {
          xvel = xvel + 0.05;
        }

        if (control_u > maxOutput)
          control_u = maxOutput;
        else if (control_u < -maxOutput)
          control_u = -maxOutput;
        else
          integral = new_integral;

        return control_u;
    }
  private:
    float kp, ki, kd, Ts;
    float maxOutput = 2;
    float integral = 0;
    float old_er = 0;
};

PID headingPID(1.5,0,0.1,1);

// PID turnPID(1,0,0,1);

// PID linvelPID(0.01,0,0,1);

class SubscribeAndPublish
{
public:
  SubscribeAndPublish()
  {
    //publish
    chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
    vel_pub = n.advertise<geometry_msgs::Twist>("/cmd_vel", 1000);
    //subscribe
    laser_subscriber = n.subscribe("/m2wr/laser/scan", 1000, &SubscribeAndPublish::laser_call, this);
  }
  void laser_call(const sensor_msgs::LaserScan::ConstPtr& scan_msg){
    std_msgs::String msg;
    // Read and process laser scan values
    laser_msg = *scan_msg;
    std::vector<float> laser_ranges;
    laser_ranges = laser_msg.ranges;
    size_t range_size = laser_ranges.size();
    float left_side = laser_msg.range_max, right_side = laser_msg.range_max, front_dist = laser_msg.range_max;
    for (int i = 0; i < 180; i++){
      if(laser_ranges[i] < right_side){
        right_side = laser_ranges[i];
      }
    }
    front_dist = laser_ranges[357]; 
    for (int k = 360; k < 720; k++){
      if (laser_ranges[k] < left_side)
      {
        left_side = laser_ranges[k];
      }
    }

    float diff = right_side - left_side;
    float sp_centering = 0;
    float z = 0.0;
    float centering = headingPID.update(sp_centering, diff);
    z = z + centering;

    // Turn through PID
    /*
    float sp_turning = 2;
    float front_dist_adj;
    if(front_dist < sp_turning){
      front_dist_adj = front_dist;
    }
    else{
      front_dist_adj = sp_turning;
    }
    float turning = turnPID.update(sp_turning, front_dist_adj);
    if(right_side > left_side){
      turning = turning * -1;
    }
    z = z + centering + turning; 
    */

    // Turn through PID on linear vel
    /*
    float sp_velred = 5;
    float front_dist_adj;
    if(front_dist < sp_velred){
      front_dist_adj = front_dist;
    }
    else{
      front_dist_adj = sp_velred;
    }
    float vel_red = linvelPID.update(sp_velred, front_dist_adj);
    xvel = xvel- abs(vel_red);
    */

    // Turn through velocity vector
    //size of ugv "0.5 0.3 0.07";
    //r = root( (0.5/2)^2 +(0.3/2)^2 ) add headspace to prevent edges touching
    float r = sqrt(pow(0.28,2)+pow(0.18,2));
    

    vel_msg.linear.x = xvel;
    vel_msg.linear.y = 0;
    vel_msg.linear.z = 0;
    vel_msg.angular.x = 0;
    vel_msg.angular.y = 0;

    vel_msg.angular.z = z;
    vel_pub.publish(vel_msg);
    std::stringstream ss;
    //std::string s = "l: " + std::to_string(left_side) + " r: " + std::to_string(right_side) + " control m: " + std::to_string(centering) + " control t: " + std::to_string(turning) + "|";
    std::string s = "control_t : " + std::to_string(z) + "|";
    ss << s;
    msg.data = ss.str(); 
    chatter_pub.publish(msg);
    }

private:
  ros::NodeHandle n;
  ros::Subscriber laser_subscriber;
  ros::Publisher chatter_pub;
  ros::Publisher vel_pub;

};//End of class SubscribeAndPublish

int main(int argc, char **argv)
{
  //Initiate ROS
  ros::init(argc, argv, "botControl");
  //Create an object of class SubscribeAndPublish 
  SubscribeAndPublish SAPObject;
  ros::Duration time_between_ros_wakeups(0.001);
  while (ros::ok()) {
        ros::spinOnce();
        time_between_ros_wakeups.sleep();
    }
  return 0;
}