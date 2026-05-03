import serial
import time

# Configurações da porta série
PORTA = '/dev/serial0'
BAUDRATE = 115200

def ler_valor(vp_address):
    """Envia um pedido de leitura (0x83) e aguarda a resposta do ecrã."""
    vp_h = (vp_address >> 8) & 0xFF
    vp_l = vp_address & 0xFF
    
    # Frame de pedido de leitura: 
    # [5A A5] [Tamanho: 04] [Comando Read: 83] [VP_H] [VP_L] [Qtd. Words para ler: 01]
    comando_leitura = bytearray([0x5A, 0xA5, 0x04, 0x83, vp_h, vp_l, 0x01])
    
    try:
        # Abre a porta
        with serial.Serial(PORTA, baudrate=BAUDRATE, timeout=0.5) as ser:
            ser.reset_input_buffer() # Limpa lixo antigo do buffer
            ser.write(comando_leitura) # Envia o pedido
            
            # Aguarda a resposta (o ecrã costuma responder em 2 a 10 milissegundos)
            tempo_inicio = time.time()
            while ser.in_waiting < 9: # Um frame de resposta completo tem 9 bytes
                if time.time() - tempo_inicio > 0.5:
                    return None # Passou meio segundo e não respondeu (Timeout)
                time.sleep(0.01)
            
            # Lê os 9 bytes de resposta
            resposta = ser.read(9)
            
            # Verifica a assinatura do DWIN (5A A5) e o comando de resposta (83)
            if resposta[0] == 0x5A and resposta[1] == 0xA5 and resposta[3] == 0x83:
                # O valor real está sempre nos dois últimos bytes do pacote
                valor_lido = (resposta[7] << 8) | resposta[8]
                return valor_lido
            
            return None
    except Exception as e:
        print(f"[!] Erro ao tentar ler a porta: {e}")
        return None

def enviar_valor(vp_address, valor):
    """Monta e envia o frame DGUS (0x82), abrindo e fechando a porta."""
    vp_h = (vp_address >> 8) & 0xFF
    vp_l = vp_address & 0xFF
    val_h = (valor >> 8) & 0xFF
    val_l = valor & 0xFF
    
    comando = bytearray([0x5A, 0xA5, 0x05, 0x82, vp_h, vp_l, val_h, val_l])
    
    try:
        with serial.Serial(PORTA, baudrate=BAUDRATE, timeout=1) as ser:
            ser.write(comando)
            print(f"-> Escrito com sucesso: {valor}")
    except Exception as e:
        print(f"\n[!] Erro ao escrever na porta: {e}")

# ==========================================
# LÓGICA PRINCIPAL
# ==========================================
print("=== Teste de Comunicação DWIN (Com Leitura Prévia) ===")

while True:
    try:
        # 1. TENTA LER O VALOR ATUAL ANTES DE QUALQUER COISA
        valor_atual = ler_valor(0x1000)
        
        if valor_atual is not None:
            # Traduz o número para a sua expressão facial para ficar mais visual
            expressao = "RAIVA (1)" if valor_atual == 1 else "NEUTRO (0)" if valor_atual == 0 else str(valor_atual)
            print(f"\n[STATUS DO ECRÃ] A memória 0x1000 contém agora: {expressao}")
        else:
            print("\n[!] Não foi possível ler o ecrã (verifique os cabos).")

        # 2. PEDE O NOVO VALOR
        entrada = input("Digite o novo valor a enviar (ou 'q' para sair): ")
        if entrada.lower() == 'q':
            break
            
        valor_int = int(entrada)
        
        if 0 <= valor_int <= 65535:
            # 3. ENVIA O NOVO VALOR
            enviar_valor(0x1000, valor_int)
        else:
            print("O valor deve estar entre 0 e 65535.")
            
    except ValueError:
        print("Erro: Por favor, digite apenas números inteiros.")
    except KeyboardInterrupt:
        break

print("Script encerrado.")