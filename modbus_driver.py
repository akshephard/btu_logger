# coding: utf-8

# In[61]:


#!/usr/bin/env python
'''
Pymodbus Synchrnonous Client Test with Dynasonic DXN Energy Meter
--------------------------------------------------------------------------

The following is an example of how to use the synchronous modbus client
implementation from pymodbus. This has been adapted from a sample script
at https://pythonhosted.org/pymodbus/examples/synchronous-client.html

_Additional Note from sample script:
It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::

    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result


***Created 2018-07-22 by Chris Weyandt
        ('string', decoder.decode_string(8)),
        ('bits', decoder.decode_bits()),
        ('8int', decoder.decode_8bit_int()),
        ('8uint', decoder.decode_8bit_uint()),
        ('16int', decoder.decode_16bit_int()),
        ('16uint', decoder.decode_16bit_uint()),
        ('32int', decoder.decode_32bit_int()),
        ('32uint', decoder.decode_32bit_uint()),
        ('32float', decoder.decode_32bit_float()),
        ('32float2', decoder.decode_32bit_float()),
        ('64int', decoder.decode_64bit_int()),
        ('64uint', decoder.decode_64bit_uint()),
        ('ignore', decoder.skip_bytes(8)),
        ('64float', decoder.decode_64bit_float()),
        ('64float2', decoder.decode_64bit_float())




'''

#---------------------------------------------------------------------------#
# import the required server implementation
#---------------------------------------------------------------------------#
from pymodbus.client.sync import ModbusTcpClient
#from pymodbus.client.sync import ModbusUdpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient

#additional imports for conversions
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import configparser
import yaml
#---------------------------------------------------------------------------#
# configure the client logging
#---------------------------------------------------------------------------#
import logging

#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)


class Modbus_Driver(object):
    def __init__(self, config_file, config_section=None):
        if (config_section==None):
            modbus_section = 'modbus'
        with open(config_file) as f:
            # use safe_load instead load
            modbusConfig = yaml.safe_load(f)

        self.MODBUS_TYPE = modbusConfig[modbus_section]['modbus_type']
        if self.MODBUS_TYPE == 'serial':
            print('serial')
            self.METHOD = modbusConfig[modbus_section]['method']
            self.SERIAL_PORT = modbusConfig[modbus_section]['port']
            self.STOPBITS = modbusConfig[modbus_section]['stopbits']
            self.BYTESIZE = modbusConfig[modbus_section]['bytesize']
            self.PARITY = modbusConfig[modbus_section]['parity']
            self.BAUDRATE = modbusConfig[modbus_section]['baudrate']
        elif self.MODBUS_TYPE == 'tcp':
            self.IP_ADDRESS = modbusConfig[modbus_section]['ip']
        else:
            print("Invalid modbus type")
            exit()

        self.UNIT_ID = modbusConfig[modbus_section]['UNIT_ID']
        self.OFFSET_REGISTERS = modbusConfig[modbus_section]['OFFSET_REGISTERS']

        if modbusConfig[modbus_section]['byte_order'] == 'big':
            self.BYTE_ORDER = Endian.Big
        elif modbusConfig[modbus_section]['byte_order'] == 'little':
            self.BYTE_ORDER = Endian.Little
        else:
            print("invalid byte order") # change to except later
            exit()
        if modbusConfig[modbus_section]['word_order'] == 'big':
            print("big")
            self.WORD_ORDER = Endian.Big
        elif modbusConfig[modbus_section]['word_order'] == 'little':
            self.WORD_ORDER = Endian.Little
        else:
            print("invalid byte order") # change to except later
            exit()



        self.register_dict = modbusConfig[modbus_section]['registers']
        for key in self.register_dict:
            self.register_dict[key][0] -= self.OFFSET_REGISTERS


    def initialize_modbus(self):
        if self.MODBUS_TYPE == 'serial':
            self.client= ModbusSerialClient(method = self.METHOD, port=self.SERIAL_PORT,stopbits = self.STOPBITS, bytesize = self.BYTESIZE, parity = self.PARITY, baudrate= self.BAUDRATE)
            connection = self.client.connect()

        if self.MODBUS_TYPE == 'tcp':
            self.client = ModbusTcpClient(self.IP_ADDRESS)



    def write_data(self,register,value):
        response = self.client.write_register(register,value,unit= self.UNIT_ID)
        return response

    def read_register_raw(self,register,length):
        #print(register)
        #print(length)
        response = self.client.read_holding_registers(register,length,unit= self.UNIT_ID)
        return response

    def decode_register(self,register,type):
        #omitting string for now since it requires a specified length

        if type == '8int':
            rr = self.read_register_raw(register,1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                    rr.registers,
                    byteorder=self.BYTE_ORDER,
                    wordorder=self.WORD_ORDER)
            output = decoder.decode_8bit_int()

        elif type == '8uint':
            rr = self.read_register_raw(register,1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                    rr.registers,
                    byteorder=self.BYTE_ORDER,
                    wordorder=self.WORD_ORDER)
            output = decoder.decode_8bit_uint()
        elif type == '16int':
            rr = self.read_register_raw(register,1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                    rr.registers,
                    byteorder=self.BYTE_ORDER,
                    wordorder=self.WORD_ORDER)
            output = decoder.decode_16bit_int()
        elif type == '16uint':
            rr = self.read_register_raw(register,1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                    rr.registers,
                    byteorder=self.BYTE_ORDER,
                    wordorder=self.WORD_ORDER)
            output = decoder.decode_16bit_uint()
        elif type == '32int':
            rr = self.read_register_raw(register,2)
            decoder = BinaryPayloadDecoder.fromRegisters(
                    rr.registers,
                    byteorder=self.BYTE_ORDER,
                    wordorder=self.WORD_ORDER)
            output = decoder.decode_32bit_int()
        elif type == '32uint':
            rr = self.read_register_raw(register,2)
            decoder = BinaryPayloadDecoder.fromRegisters(
                    rr.registers,
                    byteorder=self.BYTE_ORDER,
                    wordorder=self.WORD_ORDER)
            output = decoder.decode_32bit_uint()
        elif type == '32float':
            rr = self.read_register_raw(register,2)
            decoder = BinaryPayloadDecoder.fromRegisters(
                    rr.registers,
                    byteorder=self.BYTE_ORDER,
                    wordorder=self.WORD_ORDER)
            output = decoder.decode_32bit_float()
        elif type == '64int':
            rr = self.read_register_raw(register,4)
            decoder = BinaryPayloadDecoder.fromRegisters(
                    rr.registers,
                    byteorder=self.BYTE_ORDER,
                    wordorder=self.WORD_ORDER)
            output = decoder.decode_64bit_int()
        elif type == '64uint':
            rr = self.read_register_raw(register,4)
            decoder = BinaryPayloadDecoder.fromRegisters(
                    rr.registers,
                    byteorder=self.BYTE_ORDER,
                    wordorder=self.WORD_ORDER)
            output = decoder.decode_64bit_uint()
        elif type == 'ignore':
            rr = self.read_register_raw(register,1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                    rr.registers,
                    byteorder=self.BYTE_ORDER,
                    wordorder=self.WORD_ORDER)
            output = decoder.skip_bytes(8)
        elif type == '64float':
            rr = self.read_register_raw(register,4)
            decoder = BinaryPayloadDecoder.fromRegisters(
                    rr.registers,
                    byteorder=self.BYTE_ORDER,
                    wordorder=self.WORD_ORDER)
            output = decoder.decode_64bit_float()

        return output

    def get_data(self):

        output = {}

        for key in self.register_dict:
            #print(self.register_dict[key][0])
            output[key] = self.decode_register(self.register_dict[key][0],self.register_dict[key][1])

        return output

    def kill_modbus(self):
        self.client.close()
