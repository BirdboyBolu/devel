# ���������


## �� ����������

� Ubuntu ����� ������ ���������� ��� ����������� ����� ��������:

    sudo apt-get install python python-twisted python-pyasn1 python-openssl python-crypto python-wxgtk2.8 python-imaging

������������ Windows ����� ������������ ����������� ���� ������ ��� ��������� ����������� ������� ��������������:

* [python 2.6 ��� 2.7](http://python.org/download/releases), python3 �� ��������������
* [twisted 12.0](http://twistedmatrix.com) (��� ����� ������� ������)
* [pyasn1](http://pyasn1.sourceforge.net)
* [pyOpenSSL](https://launchpad.net/pyopenssl)
* [pycrypto](https://www.dlitz.net/software/pycrypto/)
* [PIL](http://www.pythonware.com/products/pil)
* [wxgtk2.8](http://wiki.wxpython.org/InstallingOnUbuntuOrDebian)

����� �������� [�����](http://bitpie.net/download/bitpie.tar.gz) � �������� ����� BitPie.NET. 
���������� ����� � ����� ������� ��� ��� �����.


## ������

��� ������� �� �� ���������� ������ ����������� ��������� ��������:

    cd bitpie
    python bitpie.py show
	
�� ������ ������ ������������� ���� ���� `identity`, ����� ����� ����������� �������� � �������
�������������� ���� - ��������� ��������� ������� ��� ��� ������ �������.

���� �� ���������� �� � ������� ��� ������������ ����������,
��� ����� ����� ������������������ �� ��������� ������ ��������������:

    python bitpie.py register <your_nickname>

� ���������� ��� ������� ��� ���� ����� ���������� ����� � �������� �����, 
����� ����� ����������� ������������ ���� ������ � �������.
�� ������ ������� ��� �� ������������ ���������� ��� ����� ���������� ������:

	python bitpie.py key copy <filename>

���� ��������� � ��������� ����� ����������� � ����� `~/.bitpie`.

����������� ��� �������� ��� �� �������� ������ ����������:

	python bitpie.py help

