import socket

from common_ports import ports_and_services

def is_ip(address):
  return not address.split(".")[-1].isalpha()

def to_verbose_results(ip, domain, open_ports):
  verbose_results = []

  verbose_results_header = 'Open ports for '

  # This is to get the IP from the domain if target is domain 

  if not domain: 
    try:
      domain = socket.gethostbyaddr(ip)[0]

    except socket.error:
      domain = None

  if domain:
    verbose_results_header += '%s (%s)' % (domain,ip)
  else:
    verbose_results_header += ip

  verbose_results_header += '\nPORT     SERVICE'
  verbose_results.append(verbose_results_header)

#Here we use the dictionary 'ports_and_services' to get the service name for each port.

  for port in open_ports:
    if port in ports_and_services:
      service = ports_and_services[port]

    else:
      service = ''

#Here we convert the port from int to str and right pad the str with spaces to make it's lenght 4 

    port_str = str(port).ljust(4, ' ')
    verbose_results.append('%s     %s' % (port_str, service))

  return verbose_results


def get_open_ports(target, port_range, verbose=False):
  ip = None 
  domain = None

  # Ensure IP address is valid by using the socket.inte_aton() method that changes the IP address from a doted string to a 32bit packed format as a 4 charcter string 

  if is_ip(target):
    try:
      socket.inet_aton(target)
      ip = target 
    except:
      return "Error: Invalid IP address"

  #Ensure domain name is valid 
  else:
    try:
      ip = socket.gethostbyname(target)
      domain = target
    except socket.error:
      return "Error: Invalid hostname"
  
  first_port = port_range[0]
  last_port = port_range[1]
  open_ports = []

  #Here we get all the open ports in tje given range 

  for port in range(first_port, last_port +1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    if not s.connect_ex((ip,port)):
      open_ports.append(port)
    s.close()

  if not verbose:
    return open_ports

  verbose_results = to_verbose_results(ip, domain, open_ports)

  return '\n'.join(verbose_results)

