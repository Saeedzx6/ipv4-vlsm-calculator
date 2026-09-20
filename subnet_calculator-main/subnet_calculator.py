import ipaddress
import pandas as pd

# this library is used to make the finale result better looking by putting it in a table
import tabulate

# this function checks if a number is a power of two
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

# here we ask the user for an ip address and a subnet mask to make our network:
ip = input("Enter the network ip address(example: 192.168.1.0): ")
subnet_mask = input("Enter a network subnet mask(Example: 255.255.255.0 or 24): ")

# we assemble the ip address and subnet mask to make a network
network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)

# we determine the max size for the network so we can divide it among the subnets
max_size = network.num_addresses

# this is the amount of ips that we used up
used_size = 0

# this counter simply tells the user the subnet number that he is choosing the size for
counter = 1

# we make an empty data frame to store the results at the end
df = pd.DataFrame([], columns=["Network", "Start", "End", "Hosts", "Broadcast", "Subnet Mask"])

# this list will contain the subnet sizes that the user inputs
sizes = []

# this while statment asks the user for the sizes of the subnets
# it also makes sure that the size is a power of two and that its less than the max size
while(max_size > 0):
    # this line asks the user for a subnet size while telling the of the max size
    subnet_size = int(input(f'Enter the Minimum size of subnet {counter}(Max size = {max_size}):'))
    
    # this while statment makes sure that the size is a power of two, if not it increases it until it is
    while(not is_power_of_two(subnet_size)):
        subnet_size+=1
        
    # this while statment makes sure the user doesnt input a size bigger than the max size
    while(subnet_size > max_size):
        print('-Invalid input: the subnet size can not be bigger than the max size.')
        subnet_size = int(input(f'Enter the Minimum size of subnet {counter}(Max size = {max_size}):'))
        
    # then we print the size of the subnet to inform the user if we increased the size to make it a power of two
    print(f'subnet {counter} = {subnet_size}')
    
    # then we add the size to the sizes list
    sizes.append(subnet_size)
    
    # then we decrease the max size to inform the user of how much ips are left in the network
    max_size-=subnet_size
    
    # then we increase the counter to inform the user of wich subnet to choose a size for
    counter+=1
    
# we make sure that the list of sizes is ordred from biggest to smallest 
sizes = reversed(sorted(sizes))

# this for statment is where the data frame is constructed, it makes the subnets one by one using the sizes list
for subnet_size in sizes:
    # the host bits is the number of bits we need to construct the subnet
    host_bits = len(format(subnet_size, "b")) - 1
    
    # this line constructs the subnet with the host bits that it needs to have a certin number of ips
    subnets = list(network.subnets(new_prefix=32 - host_bits))
    
    # I am not even gonna try to explain those 2 lines in a single comment, ill explain it in person
    # just know it took me hours to come up with those two lines of code
    subnet = subnets[int(used_size / subnet_size)]
    used_size+=subnet_size
    
    # the rest of the for statment simply constucts the data frame from the following variables: 
    start = list(subnet.hosts())[0]
    end = list(subnet.hosts())[-1]
    broadcast = subnet.broadcast_address
    number_of_hosts = len(list(subnet.hosts()))
    net_mask = subnet.netmask
    data = [str(subnet), str(start), str(end), str(number_of_hosts), str(broadcast), str(net_mask)]
    df.loc[len(df)] = data

# now we increase the index so the table does not start from zero
df.index+=1

# finaly we print the data frame using the "tabulate" library to make it look good
print(tabulate.tabulate(df, headers='keys', tablefmt='pretty', showindex=True))