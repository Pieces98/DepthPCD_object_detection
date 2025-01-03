import sys, os

import cv2
from cv_bridge import CvBridge

import numpy as np
import ros2_numpy as rnp

import rclpy as rp
from rclpy.node import Node
from message_filters import ApproximateTimeSynchronizer, Subscriber
from laser_geometry import LaserProjection
from sensor_msgs.msg import Image, LaserScan, PointCloud2

class DataSubscriber(Node):
    def __init__(self):
        super().__init__('data_extractor')

        self.count = 0
        self.bridge = CvBridge()
        self.laser_proj = LaserProjection()

        self.save_dir_root = './data'
        self.subscribers = [
            Subscriber(self, LaserScan, '/scan'), 
            Subscriber(self, PointCloud2, '/camera/depth/points'),
            Subscriber(self, Image, '/camera/depth/image_raw'), 
            Subscriber(self, Image, '/camera/color/image_raw')
        ]

        

        self.synchronizer = ApproximateTimeSynchronizer(
            self.subscribers, 
            queue_size=10, 
            slop=0.02
        )
        self.synchronizer.registerCallback(self.save_data)

    def save_data(self, lidar_scan_msg, depth_pcd_msg, depth_img_msg, rgb_img_msg):
        # LiDAR LaserScan to PointCloud2 and PointCloud2 to np.array
        lidar_pcd_msg = self.laser_proj.projectLaser(lidar_scan_msg)
        lidar_pcd = rnp.numpify(lidar_pcd_msg)['xyz']

        # Depth camera PointCloud2 to np.array
        depth_pcd = rnp.numpify(depth_pcd_msg)['xyz']

        # Depth camera depth image
        depth_img = self.bridge.imgmsg_to_cv2(depth_img_msg, '16UC1')
        depth_img = cv2.convertScaleAbs(depth_img, alpha=0.05)

        # Depth camera rgb image
        rgb_img = self.bridge.imgmsg_to_cv2(rgb_img_msg, 'bgr8')
        

        # Save data
        np.save(os.path.join(self.save_dir_root, 'lidar_pcd', f'lidar_pcd_{self.count:05d}.npy'), lidar_pcd)
        np.save(os.path.join(self.save_dir_root, 'depth_pcd', f'depth_pcd_{self.count:05d}.npy'), depth_pcd)
        cv2.imwrite(os.path.join(self.save_dir_root, 'depth_img', f'depth_img_{self.count:05d}.jpg'), depth_img)
        cv2.imwrite(os.path.join(self.save_dir_root, 'rgb_img', f'rgb_img_{self.count:05d}.jpg'), rgb_img)
        print(f'data {self.count:05d} saved')
        self.count += 1

    
def main(args=None):
    rp.init(args=args)
    
    subscriber_node = DataSubscriber()

    print('Data extractor activated.')
    rp.spin(subscriber_node)
    subscriber_node.destroy_node()
    rp.shutdown()

if __name__ == '__main__':
    main()