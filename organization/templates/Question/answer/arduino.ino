/* upstairs_robot - 版本1.0 */
// 采用模块化设计

// ================= 硬件引脚定义 =================
// 前腿抬升机构（双步进电机）
#define FRONTLEG_STEP_L 22    // 前左抬升步进脉冲
#define FRONTLEG_DIR_L 23     // 前左抬升方向
#define FRONTLEG_STEP_R 24    // 前右抬进脉冲
#define FRONTLEG_DIR_R 25     // 前右方向
const int FRONTLEG_MAX_STEP = 2000;  // 最大抬升步数

// 后腿支撑机构（双步进电机）
#define HINDLEG_STEP_L 26     // 后左步进脉冲
#define HINDLEG_DIR_L 27      // 后左方向
#define HINDLEG_STEP_R 28     // 后右脉冲
#define HINDLEG_DIR_R 29      // 后右方向
const int HINDLEG_MIN_PRESSURE = 15; // 支撑腿最小压力值(Kg)

// 身体轮组（4个直流电机）
#define BODY_FL_PWM 3    // 身体前左轮PWM
#define BODY_FL_DIR 4    // 身体前左方向
#define BODY_FR_PWM 5    // 前右PWM
#define BODY_FR_DIR 6    // 前右方向
#define BODY_RL_PWM 7    // 后左PWM
#define BODY_RL_DIR 8    // 后左方向
#define BODY_RR_PWM 9    // 后右PWM
#define BODY_RR_DIR 10   // 后右方向

// ================= 核心控制函数 =================
void setup() {
  // 初始化步进电机控制引脚
  pinMode(FRONTLEG_STEP_L, OUTPUT);
  pinMode(FRONTLEG_DIR_L, OUTPUT);
 

  // 设置直流电机引脚
  pinMode(BODY_FL_PWM, OUTPUT);
  pinMode(BODY_FL_DIR, OUTPUT);
  // 初始化其他直流电机引脚

  Serial.begin(115200); // 启动调试串口
}

// 前腿抬升函数
void liftFrontLeg(int steps, bool isUp) {
  digitalWrite(FRONTLEG_DIR_L, isUp ? HIGH : LOW);
  digitalWrite(FRONTLEG_DIR_R, isUp ? HIGH : LOW);
  
  for(int i=0; i<steps; i++){
    // 同步驱动双步进电机
    digitalWrite(FRONTLEG_STEP_L, HIGH);
    digitalWrite(FRONTLEG_STEP_R, HIGH);
    delayMicroseconds(800); // 控制抬升速度
    digitalWrite(FRONTLEG_STEP_L, LOW);
    digitalWrite(FRONTLEG_STEP_R, LOW);
    delayMicroseconds(800);
    
  }
}

// 身体轮组运动控制（四轮独立驱动）
void driveBodyWheels(int fl_speed, int fr_speed, 
                    int rl_speed, int rr_speed) {
  // 限制速度范围（-255~255）
  fl_speed = constrain(fl_speed, -255, 255);
  fr_speed = constrain(fr_speed, -255, 255);
  
  // 前左轮驱动
  digitalWrite(BODY_FL_DIR, fl_speed >0 ? HIGH:LOW);
  analogWrite(BODY_FL_PWM, abs(fl_speed));
  
}

// ================= 主控制循环 =================
void loop() {
  
  static int stepCounter = 0;
  
  // 阶段1：前腿抬升
  if(stepCounter < FRONTLEG_MAX_STEP){
    liftFrontLeg(50, true); // 每次抬升50步
    stepCounter +=50;
    return;
  }
  
  // 阶段2：身体轮组推进
  driveBodyWheels(200, 200, 200, 200); // 全速前进
  delay(2000);  // 持续2秒
  
  // 阶段3：后腿跟进
  adjustHindLegPosition(); // 后腿位置调整函数
  
  stepCounter =0; // 重置计数器
}