��������:
������ network() ��� ������� ������, ������� ������ �� ��� ������ ������� ������� � ���������� �� BitPie.NET. ��� � ���������, ���������� ���������� ���� �������� �� ������ ������ ��������, ����� ������� ��� ������ � ���������� � ������� �������� � ��������� ��������� ������ �������������� � �����.

Description:
Service network() is a basic service that affects all other network services in the BitPie.NET software. When it is stopped, all currently active services will be also stopped, all sessions and connections to other machines will be closed, and the program should stop any interaction with the network.

��������� ����� �������:
services/service_network.py 
p2p/network_connector.py 
p2p/run_upnpc.py

���������� ��������: 
network_connector()
