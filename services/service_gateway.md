# ������ gateway()


## ��������
������� ������ `gateway()` �������� ������� ������ ��� �������� � ������ ��������� ������� ������ � �������������� � ������� ������ � ���� BitPie.NET. ��� ������ ���� "������" ����� ������� �������� ���� �������� ������ ��� ����������� ��. 

�������� ��� ������ `inbox()` � `outbox()` ������������ �������� � ��������� ������, ����������� ����������� �������� ��������� ������. 
���� ������ ��� �� ����� ���� ����������� ������ ��������� ������, ����� ��� ��� ����� �������� � ����� `outbox()`. 

����������� ������� ����� �������� ������ � ������ �������� ����������� �� � ������ ������ � �������� ������� ����� "������". 
������ `gateway()` ��� �� ����� ������� ��������� ������� � ������� ������� �� � ������ ���������� �� ���� � ��������� `.bitpie/bandin` � `.bitpie/bandout`.

���������� �������� `packet_in()` � `packet_out()` ��������� � ������ ������ � �������� ���������� ������ ��������������. ��� ��������� ��������� ������ ������, ��������� ��������� ��� ������ ��������� � ��������� ���������� ���������� �������� � ���.


## ������� ��
* [network()](services/service_network.md)


## ������ ��
* [private_messages()](services/service_private_messages.md)
* [p2p_hookups()](services/service_p2p_hookups.md)
* [supplier()](services/service_supplier.md)
* [udp_transport()](services/service_udp_transport.md)
* [tcp_transport()](services/service_tcp_transport.md)
* [identity_propagate()](services/service_identity_propagate.md)


## ��������� �������
* services/gateway/enabled - ���������/���������� ������� `gateway()`


## ��������� ����� �������
* [services/service_gateway.py](services/service_gateway.py)
* [transport/gateway.py](transport/gateway.py)
* [transport/packet_in.py](transport/packet_in.py)
* [transport/packet_out.py](transport/packet_out.py)
* [transport/bandwidth.py](transport/bandwidth.py)
* [transport/callback.py](transport/callback.py)
* [transport/stats.py](transport/stats.py)


## ������ ���������
* [packet_in()](transport/packet_in.md)
* [packet_out()](transport/packet_out.md)
