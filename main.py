import serial

try:
    # Lembre-se: em alguns Raspberry Pi, a porta pode ser /dev/ttyAMA0 ou /dev/ttyS0
    ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)
    print("Porta serial aberta com sucesso.")
except Exception as e:
    print(f"Erro ao abrir a porta serial: {e}")
    exit()

def enviar_valor(vp_address, valor):
    """Monta e envia o frame DGUS para escrever um inteiro de 16 bits."""
    # Desmembrando o endereço e o valor em bytes (High e Low)
    vp_h = (vp_address >> 8) & 0xFF
    vp_l = vp_address & 0xFF
    val_h = (valor >> 8) & 0xFF
    val_l = valor & 0xFF
    
    # Frame: [5A A5] [Tamanho] [Write:82] [VP_H] [VP_L] [VAL_H] [VAL_L]
    comando = bytearray([0x5A, 0xA5, 0x05, 0x82, vp_h, vp_l, val_h, val_l])
    
    ser.write(comando)
    print(f"-> Enviado hex: {comando.hex(' ').upper()}")

print("=== Teste de Comunicação DWIN ===")
while True:
    try:
        entrada = input("\nDigite um número para enviar (ou 'q' para sair): ")
        if entrada.lower() == 'q':
            break
            
        valor_int = int(entrada)
        
        # O valor máximo para 2 bytes é 65535.
        if 0 <= valor_int <= 65535:
            enviar_valor(0x1000, valor_int)
        else:
            print("O valor deve estar entre 0 e 65535.")
            
    except ValueError:
        print("Erro: Por favor, digite apenas números inteiros.")
    except KeyboardInterrupt:
        break

ser.close()
print("Conexão encerrada.")