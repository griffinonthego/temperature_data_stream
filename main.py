import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import paramiko

# specify the file to read from and write to
remote_file_in = "examples/dht_outputs2.txt"
file_out = "output.txt"
file_in = "unfiltered_data.txt"

# Create an SSH client
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.WarningPolicy)

# Connect to the remote host
client.connect('10.0.0.48', username='pi', password='griffgriff_')
sftp = client.open_sftp()
sftp.get(remote_file_in, file_in)
sftp.close()
client.close()

# regular expression pattern to match the format
pattern = r"Temp: (\d+\.\d+) F / (\d+\.\d+) C\s+Humidity: (\d+)%"

with open(file_in, "r") as f_in, open(file_out, "w") as f_out:
    for line in f_in:
        match = re.match(pattern, line)
        if match:
            first_num, _, third_num = match.groups()
            f_out.write(f"{first_num},{third_num}\n")


# arrays to store the data from each column
temp_f = []
humidity_data = []

# create a figure and axes for the plot
fig, ax = plt.subplots()
ax.set_xlim(0, 7000)
ax.set_ylim(0, 200)
line1, = ax.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2)
# function to be called repeatedly to update the plot
def update(num):
    client.connect('10.0.0.48', username='pi', password='griffgriff_')
    sftp = client.open_sftp()
    sftp.get(remote_file_in, file_in)
    sftp.close()
    client.close()

    # regular expression pattern to match the format
    pattern = r"Temp: (\d+\.\d+) F / (\d+\.\d+) C\s+Humidity: (\d+)%"

    with open(file_in, "r") as f_in, open(file_out, "w") as f_out:
        for line in f_in:
            match = re.match(pattern, line)
            if match:
                first_num, _, third_num = match.groups()
                f_out.write(f"{first_num},{third_num}\n")

    data = open(file_out,'r').readlines()
    x = list(range(len(data)))
    y = [i.strip().split(",") for i in data]
    temp_f = [float(i[0]) for i in y]
    humidity_data = [float(i[1]) for i in y]
    line1.set_data(x, temp_f)
    line2.set_data(x, humidity_data)

    return line1, line2


# create the animation object
ani = animation.FuncAnimation(fig, update, frames=100, repeat=True)
plt.show()
