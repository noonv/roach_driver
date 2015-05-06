/*
 * CraftDuino firmware
 * for Roach Follower Robot
 *
 * http://robocraft.ru
 */

// store motor pins
typedef struct MOTOR
{
    int in1;      // INPUT1
    int in2;      // INPUT2
    int enable; // ENABLE (pwm)
} MOTOR;

#define BAUDRATE 57600
#define MOTORS_COUNT 2
#define SPEED 220

MOTOR motors[MOTORS_COUNT] = {
    { 12, 11, 10 },
    { 7,  8,  9 }
};

static const int FORWARD = HIGH;
static const int BACKWARD = LOW;

void motor_drive(int motor_id, int dir, int pwm);

void motor_drive(int motor_id, int pwm) 
{
    if(pwm >= 0) {
        motor_drive(motor_id, FORWARD, pwm);
    }
    else {
        motor_drive(motor_id, BACKWARD, (-1)*pwm);
    }
}

void motor_drive(int motor_id, int dir, int pwm)
{
    if(motor_id < 0 || motor_id >= MOTORS_COUNT)
        return;

    if(dir == FORWARD) {
        digitalWrite(motors[motor_id].in1, HIGH);
        digitalWrite(motors[motor_id].in2, LOW);
    }
    else {
        digitalWrite(motors[motor_id].in1, LOW);
        digitalWrite(motors[motor_id].in2, HIGH);
    }
    analogWrite(motors[motor_id].enable, pwm);

}

void setup() 
{                
    Serial.begin(BAUDRATE);

    int i;
    for(i=0; i<MOTORS_COUNT; i++) {
        pinMode(motors[i].in1, OUTPUT);
        pinMode(motors[i].in2, OUTPUT);
    }

    for(i=0; i<MOTORS_COUNT; i++) {
        motor_drive(i, FORWARD, 0);
    }
}

void loop() 
{
//    motor_drive(0, SPEED);
//    motor_drive(1, SPEED);
//    delay(1000);
//    motor_drive(0, -SPEED);
//    motor_drive(1, -SPEED);
//    delay(1000);

    // read message from serial
    int c = 0;
    if(Serial.available()) {
        c = Serial.read();
        if(c == 'w') {
            motor_drive(0, SPEED);
            motor_drive(1, SPEED);
        }
        else if(c == 's') {
            motor_drive(0, -SPEED);
            motor_drive(1, -SPEED);
        }
        else if(c == 'a') {
            motor_drive(0, SPEED);
            motor_drive(1, -SPEED);
        }
        else if(c == 'd') {
            motor_drive(0, -SPEED);
            motor_drive(1, SPEED);
        }
        else if(c == ' ') {
            motor_drive(0, 0);
            motor_drive(1, 0);
        }
    }
}
