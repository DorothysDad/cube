import socket

hardware_plan = []

def human_readable(string):
    data = []
    for i in range(54):
        char = string[i]
        if char == 'D':
            data.append('white  ')
        if char == 'F':
            data.append('red    ')
        if char == 'B':
            data.append('organge')
        if char == 'U':
            data.append('yellow ')
        if char == 'R':
            data.append('green  ')
        if char == 'L':
            data.append('blue   ')

    for i in range(6):
        data_sub = data[i*9: i*9+9]
        print(data_sub[0:3])
        print(data_sub[3:6])
        print(data_sub[6:9])
        print('-----',data_sub[4])

def hardware_execute_entirety_rotate(number):
    reverse = [2, 1, 0, 3]
    return reverse[number] + 4


def hardware_execute_bottom_rotate(number):
    reverse = [2, 1, 0, 3]
    return reverse[number - 1] + 1


def surfaces_2_plan(surfaces):
    global hardware_plan
    hardware_plan = []
    S = [ 'L', 'F', 'R', 'B', 'U', 'D']
    T = [['F', 'R', 'B', 'L', 'U', 'D'],  # +90
         ['R', 'B', 'L', 'F', 'U', 'D'],  # 180
         ['B', 'L', 'F', 'R', 'U', 'D'],  # 270
         ['L', 'U', 'R', 'D', 'B', 'F']]  # K90
    N = [2, 1, 0, 3, 3, -1]

    # ask for server and find origin solution
    plan = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.connect(('118.24.87.139', 8080))
    s.connect(('127.0.0.1', 8080))
    socket_input_string = ''
    for i in range(6):
        for j in range(9):
            socket_input_string += surfaces[i][j]
    human_readable(socket_input_string)
    s.sendall((socket_input_string + '\n').encode())
    socket_receieve_str = s.recv(2048).decode().strip('\n')
    s.close()
    words = socket_receieve_str.split(' ')
    if words[-1][-2] != 'f':
        print('Server process Error...')
        print(socket_receieve_str)
        return False
    else:
        print('Server process Success!')
        print(socket_receieve_str)
        for word in words[0:-1]:
            plan.append([word[0], word[1]])

        # adjust according to init
        for j in range(len(plan)):
            for k in range(6):
                if plan[j][0] == S[k]:
                    plan[j][0] = T[3][k]
                    break
        # get hardware solution
        for step in range(len(plan)):
            while True:
                for find_i in range(6):
                    if plan[step][0] == S[find_i]:
                        i = find_i
                        break
                if N[i] == -1:
                    hardware_plan.append(hardware_execute_bottom_rotate(int(plan[step][1])))
                    break
                else:
                    hardware_plan.append(hardware_execute_entirety_rotate(N[i]))
                    for j in range(len(plan)):
                        for k in range(6):
                            if plan[j][0] == S[k]:
                                plan[j][0] = T[N[i]][k]
                                break
        return True