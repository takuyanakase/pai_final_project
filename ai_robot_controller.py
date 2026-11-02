#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class AIVisionController(Node):
    def __init__(self):
        super().__init__('ai_vision_controller')
        
        # 速度指令を /cmd_vel にパブリッシュするパブリッシャー
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 0.5秒ごとに動作を計算するタイマー
        self.timer = self.create_timer(0.5, self.control_loop)
        
        self.get_logger().info('=== AI Vision / Autonomous Controller Started ===')
        self.get_logger().info('Simulating visual tracking & autonomous behavior...')
        
        self.state = 0
        self.start_time = time.time()

    def control_loop(self):
        msg = Twist()
        current_time = time.time() - self.start_time

        # 【AIビジョン・自律制御ロジックのシミュレーション】
        # 映像の解析結果（ターゲットの有無や位置）に応じた行動決定を模しています
        
        if current_time < 5.0:
            # 状態1: 探索フェーズ（周囲をスキャンするようにゆっくり旋回）
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.get_logger().info('[AI Vision Inference] Target searching: Rotating to scan environment...')
            
        elif current_time < 12.0:
            # 状態2: ターゲット発見・アプローチフェーズ（直進してターゲットに近づく）
            msg.linear.x = 0.4
            msg.angular.z = 0.0
            self.get_logger().info('[AI Vision Inference] Target detected! Approaching target (Visual Tracking Active)...')
            
        elif current_time < 15.0:
            # 状態3: 回避・調整フェーズ（障害物やターゲットの前で一旦停止・方向微調整）
            msg.linear.x = 0.0
            msg.angular.z = -0.5
            self.get_logger().info('[AI Vision Inference] Obstacle/Target alignment: Adjusting orientation...')
            
        else:
            # 状態4: 任務完了、ループして再探索
            self.start_time = time.time()

        # 速度指令を送信
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    controller = AIVisionController()
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()