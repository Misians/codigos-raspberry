import serial
import time

# Configura a porta serial (altere para /dev/ttyUSB0 se estiver usando um adaptador USB-Serial)
# A taxa de baudrate padrão da DWIN é 115200.
ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

def mudar_expressao(valor):
    """
    Envia o valor inteiro para o endereço 0x1000 do display.
    valor = 0 (Neutro)
    valor = 1 (Raiva)
    """
    # Montando o frame hexadecimal: [5A A5] [05] [82] [10 00] [00 Valor]
    comando = bytearray([0x5A, 0xA5, 0x05, 0x82, 0x10, 0x00, 0x00, valor])
    
    ser.write(comando)
    print(f"Comando enviado. Expressão atual: {valor}")

# --- Lógica de Exemplo ---
try:
    print("Iniciando display em estado Neutro...")
    mudar_expressao(0)
    time.sleep(3)
    
    print("Mudando para Raiva!")
    mudar_expressao(1)
    time.sleep(3)
    
    print("Voltando ao normal...")
    mudar_expressao(0)
    
except KeyboardInterrupt:
    ser.close()