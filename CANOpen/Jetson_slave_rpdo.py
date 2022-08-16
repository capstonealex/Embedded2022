import canopen
import time

# construct a CAN network
network = canopen.Network()

# connect to the CAN network
network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)
#network.connect(bustype='socketcan', channel='can0', bitrate=1000000)

# create a slaver node with id 2(need to match with master.py) and Object Dictionary "Slaver.eds"
Jetson_66 = network.create_node(66, 'Jetson_exo_66_v11.eds')

# Node send the boot-up message to the CAN network COB-ID:0x700+node-ID detail: "0"
Jetson_66.nmt.send_command(0)

# With the heartbeat configuration in object Dictionary, use the function by following command every 1s(1000ms)
Jetson_66.nmt.start_heartbeat(1000)  

# send pdo message
Jetson_66.rpdo.read()
Jetson_66.tpdo.read()

print("Test reading PDO to read input of Exo")
try:
    while True:
        timestamp_1 = Jetson_66.rpdo[1].wait_for_reception(timeout=0.1)
        timestamp_2 = Jetson_66.rpdo[2].wait_for_reception(timeout=0.1)
        timestamp_3 = Jetson_66.rpdo[3].wait_for_reception(timeout=0.1)
        timestamp_4 = Jetson_66.rpdo[4].wait_for_reception(timeout=0.1)
        timestamp_5 = Jetson_66.rpdo[5].wait_for_reception(timeout=0.1)
        timestamp_6 = Jetson_66.rpdo[6].wait_for_reception(timeout=0.1)
        timestamp_7 = Jetson_66.rpdo[7].wait_for_reception(timeout=0.1)
        timestamp_8 = Jetson_66.rpdo[8].wait_for_reception(timeout=0.1)

        timestamp_9 = Jetson_66.rpdo[9].wait_for_reception(timeout=0.1)
        timestamp_10 = Jetson_66.rpdo[10].wait_for_reception(timeout=0.1)
        timestamp_11 = Jetson_66.rpdo[11].wait_for_reception(timeout=0.1)
        timestamp_12 = Jetson_66.rpdo[12].wait_for_reception(timeout=0.1)

        timestamp_13 = Jetson_66.rpdo[13].wait_for_reception(timeout=0.1)
        timestamp_14 = Jetson_66.rpdo[14].wait_for_reception(timeout=0.1)

        timestamp_15 = Jetson_66.rpdo[15].wait_for_reception(timeout=0.1)
        timestamp_16 = Jetson_66.rpdo[16].wait_for_reception(timeout=0.1)

        timestamp_17 = Jetson_66.rpdo[17].wait_for_reception(timeout=0.1)
        timestamp_18 = Jetson_66.rpdo[18].wait_for_reception(timeout=0.1)

        
        # LH_position[] = [Jetson_node_66.rpdo[1][0x200F].phys,Jetson_node_66.rpdo[1][0x2010].phys,Jetson_node_66.rpdo[1][0x2011].phys,Jetson_node_66.rpdo[1][0x2012].phys]
        # 'LH_Position_1'= 0x200F
        LH_position = [Jetson_66.rpdo[1]['LH_Position_1'].phys, Jetson_66.rpdo[1][0x2010].phys, Jetson_66.rpdo[1][0x2011].phys, Jetson_66.rpdo[1][0x2012].phys]
        LH_velocity = [Jetson_66.rpdo[1][0x2013].phys, Jetson_66.rpdo[1][0x2014].phys, Jetson_66.rpdo[1][0x2015].phys, Jetson_66.rpdo[1][0x2016].phys]
        LH_torque = [Jetson_66.rpdo[2][0x2017].phys, Jetson_66.rpdo[2][0x2018].phys]

        LK_position = [Jetson_66.rpdo[3][0x2019].phys, Jetson_66.rpdo[3][0x201A].phys, Jetson_66.rpdo[3][0x201B].phys, Jetson_66.rpdo[3][0x201C].phys]
        LK_velocity = [Jetson_66.rpdo[3][0x201D].phys, Jetson_66.rpdo[3][0x201E].phys, Jetson_66.rpdo[3][0x201F].phys, Jetson_66.rpdo[3][0x2020].phys]
        LK_torque = [Jetson_66.rpdo[4][0x2021].phys, Jetson_66.rpdo[4][0x2022].phys]
        
        RH_position = [Jetson_66.rpdo[5][0x2023].phys, Jetson_66.rpdo[5][0x2024].phys, Jetson_66.rpdo[5][0x2025].phys, Jetson_66.rpdo[5][0x2026].phys]
        RH_velocity = [Jetson_66.rpdo[5][0x2027].phys, Jetson_66.rpdo[5][0x2028].phys, Jetson_66.rpdo[5][0x2029].phys, Jetson_66.rpdo[5][0x202A].phys]
        RH_torque = [Jetson_66.rpdo[6][0x202B].phys, Jetson_66.rpdo[6][0x202C].phys]

        RK_position = [Jetson_66.rpdo[7][0x202D].phys, Jetson_66.rpdo[7][0x202E].phys, Jetson_66.rpdo[7][0x202F].phys, Jetson_66.rpdo[7][0x2030].phys]
        RK_velocity = [Jetson_66.rpdo[7][0x2031].phys, Jetson_66.rpdo[7][0x2032].phys, Jetson_66.rpdo[7][0x2033].phys, Jetson_66.rpdo[7][0x2034].phys]
        RK_torque = [Jetson_66.rpdo[8][0x2035].phys, Jetson_66.rpdo[8][0x2036].phys]

        Left_crutch_force_sesnor_1 = [Jetson_66.rpdo[9][0x2037].phys, Jetson_66.rpdo[9][0x2038].phys, Jetson_66.rpdo[9][0x2039].phys, Jetson_66.rpdo[9][0x203A].phys, Jetson_66.rpdo[9][0x203B].phys, Jetson_66.rpdo[9][0x203C].phys, Jetson_66.rpdo[9][0x203D].phys, Jetson_66.rpdo[9][0x203E].phys]
        Left_crutch_force_sesnor_2 = [Jetson_66.rpdo[10][0x203F].phys, Jetson_66.rpdo[10][0x2040].phys, Jetson_66.rpdo[10][0x2041].phys, Jetson_66.rpdo[10][0x2042].phys, Jetson_66.rpdo[10][0x2043].phys, Jetson_66.rpdo[10][0x2044].phys, Jetson_66.rpdo[10][0x2045].phys, Jetson_66.rpdo[10][0x2046].phys]
        Right_crutch_force_sesnor_1 = [Jetson_66.rpdo[11][0x2047].phys, Jetson_66.rpdo[11][0x2048].phys, Jetson_66.rpdo[11][0x2049].phys, Jetson_66.rpdo[11][0x204A].phys, Jetson_66.rpdo[11][0x204B].phys, Jetson_66.rpdo[11][0x204C].phys, Jetson_66.rpdo[11][0x204D].phys, Jetson_66.rpdo[11][0x204E].phys]
        Right_crutch_force_sesnor_2 = [Jetson_66.rpdo[12][0x204F].phys, Jetson_66.rpdo[12][0x2050].phys, Jetson_66.rpdo[12][0x2051].phys, Jetson_66.rpdo[12][0x2052].phys, Jetson_66.rpdo[12][0x2053].phys, Jetson_66.rpdo[12][0x2054].phys, Jetson_66.rpdo[12][0x2055].phys, Jetson_66.rpdo[12][0x2056].phys]

        Left_crutch_force_sesnor_command = [Jetson_66.rpdo[13][0x2057].phys]
        Right_crutch_force_sesnor_command = [Jetson_66.rpdo[14][0x205F].phys]

        Current_state = [Jetson_66.rpdo[15][0x2067].phys]
        Current_movement = [Jetson_66.rpdo[16][0x206F].phys]

        Next_movement = [Jetson_66.rpdo[17][0x2077].phys]
        Go_button = [Jetson_66.rpdo[18][0x207F].phys]

        
        print("LH Actual Position = {} {} {} {} t={}".format(LH_position[0],LH_position[1], LH_position[2], LH_position[3], timestamp_1))
        print("LK Actual Position = {} {} {} {} t={}".format(LK_position[0],LK_position[1], LK_position[2], LK_position[3], timestamp_4))
        print("RH Actual Position = {} {} {} {} t={}".format(RH_position[0],RH_position[1], RH_position[2], RH_position[3], timestamp_7))
        print("RH Actual Position = {} {} {} {} t={}".format(RH_position[0],RH_position[1], RH_position[2], RH_position[3], timestamp_10))

        print("LH Actual Velocity = {} {} {} {} t={}".format(LH_velocity[0],LH_velocity[1], LH_velocity[2], LH_velocity[3], timestamp_2))
        print("LK Actual Velocity = {} {} {} {} t={}".format(LK_velocity[0],LK_velocity[1], LK_velocity[2], LK_velocity[3], timestamp_5))
        print("RH Actual Velocity = {} {} {} {} t={}".format(RH_velocity[0],RH_velocity[1], RH_velocity[2], RH_velocity[3], timestamp_8))
        print("RH Actual Velocity = {} {} {} {} t={}".format(RH_velocity[0],RH_velocity[1], RH_velocity[2], RH_velocity[3], timestamp_11))

        print("LH Actual Torque = {} {} t={}".format(LH_torque[0],LH_torque[1], timestamp_3))
        print("LK Actual Torque = {} {} t={}".format(LK_torque[0],LK_torque[1], timestamp_6))
        print("RH Actual Torque = {} {} t={}".format(RH_torque[0],RH_torque[1], timestamp_9))
        print("RH Actual Torque = {} {} t={}".format(RH_torque[0],RH_torque[1], timestamp_12))

        print("Left crutch force sesnor 1 = {} {} {} {} {} {} {} {} t={}".format(LH_velocity[0],LH_velocity[1], LH_velocity[2], LH_velocity[3], timestamp_2))
        print("Left crutch force sesnor 2 = {} {} {} {} {} {} {} {} t={}".format(LK_velocity[0],LK_velocity[1], LK_velocity[2], LK_velocity[3], timestamp_5))
        print("RH Actual Velocity = {} {} {} {} {} {} {} {} t={}".format(RH_velocity[0],RH_velocity[1], RH_velocity[2], RH_velocity[3], timestamp_8))
        print("RH Actual Velocity = {} {} {} {} {} {} {} {} t={}".format(RH_velocity[0],RH_velocity[1], RH_velocity[2], RH_velocity[3], timestamp_11))

    
except KeyboardInterrupt:
    print("Exit from reading PDO to Jetson")