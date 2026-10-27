import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class DuvarKacan(Node):
    def __init__(self):
        super().__init__('duvar_kacan')

        # Bonus: hiz ve sinir degerleri parametre
        self.declare_parameter('hiz', 1.5)
        self.declare_parameter('donus_hizi', 2.0)
        self.declare_parameter('alt_sinir', 1.0)
        self.declare_parameter('ust_sinir', 10.0)

        # Yayinci: kaplumbagayi surmek icin
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # Abone: konumu dinlemek icin
        self.sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10)

        self.x = 0.0
        self.y = 0.0
        self.pose_alindi = False

        # 0.1 sn'de bir karar ver, 1 sn'de bir logla
        self.kontrol_timer = self.create_timer(0.1, self.kontrol)
        self.log_timer = self.create_timer(1.0, self.logla)

    def pose_callback(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.pose_alindi = True

    def kontrol(self):
        if not self.pose_alindi:
            return

        hiz = self.get_parameter('hiz').value
        donus = self.get_parameter('donus_hizi').value
        alt = self.get_parameter('alt_sinir').value
        ust = self.get_parameter('ust_sinir').value

        msg = Twist()
        if (self.x < alt or self.x > ust or
                self.y < alt or self.y > ust):
            # Duvara yakin: yavasla ve don
            msg.linear.x = hiz * 0.5
            msg.angular.z = donus
        else:
            # Guvenli bolge: duz ilerle
            msg.linear.x = hiz
            msg.angular.z = 0.0
        self.pub.publish(msg)

    def logla(self):
        if self.pose_alindi:
            self.get_logger().info(
                f'Konum -> x: {self.x:.2f}, y: {self.y:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = DuvarKacan()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
