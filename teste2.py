import serial
import time

# Configurações da porta serial
PORTA = '/dev/serial0'
BAUDRATE = 115200

def enviar_valor(vp_address, valor):
    """Monta e envia o frame DGUS, abrindo e fechando a porta a cada envio."""
    # Desmembrando o endereço e o valor em bytes (High e Low)
    vp_h = (vp_address >> 8) & 0xFF
    vp_l = vp_address & 0xFF
    val_h = (valor >> 8) & 0xFF
    val_l = valor & 0xFF
    
    # Frame: [5A A5] [Tamanho] [Write:82] [VP_H] [VP_L] [VAL_H] [VAL_L]
    comando = bytearray([0x5A, 0xA5, 0x05, 0x82, vp_h, vp_l, val_h, val_l])
    
    try:
        # O bloco 'with' ABRE a porta aqui e FECHA automaticamente ao sair do bloco
        with serial.Serial(PORTA, baudrate=BAUDRATE, timeout=1) as ser:
            ser.write(comando)
            # A porta é fechada instantaneamente após essa linha
            print(f"-> Enviado hex: {comando.hex(' ').upper()} (Porta aberta e fechada)")
    except Exception as e:
        print(f"\n[!] Erro ao tentar se comunicar com a porta serial: {e}")
        print("[!] Verifique se os cabos estão bem conectados.")

print("=== Teste de Comunicação DWIN (Abre e Fecha a cada envio) ===")
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

print("Script encerrado.")