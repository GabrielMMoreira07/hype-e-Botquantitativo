from flask import Flask, jsonify
from flask_cors import CORS
from agente import RoboNexus
import traceback

app = Flask(__name__)
CORS(app)

meu_robo = RoboNexus()

@app.route('/api/analise', methods=['GET'])
def analise_do_robo():
    try:
        # Tenta rodar o robô normalmente
        resposta_real = meu_robo.rodar_algoritmo()
        return jsonify(resposta_real)
        
    except Exception as e:
        # Se algo falhar, capturamos o erro e mostramos no terminal do Mac
        print("\n❌ ERRO DETECTADO NO MOTOR DO ROBÔ:")
        traceback.print_exc()
        
        # Enviamos o erro formatado para o site mostrar na tela
        return jsonify({
            "ticker": "ERRO API",
            "jogo": "Falha na Comunicação",
            "decisao": "VENDER",
            "lucro_prejuizo": "OFFLINE",
            "motivo": f"Erro interno do Python: {str(e)}"
        })

if __name__ == '__main__':
    print("🤖 Servidor HYPE-E Iniciado. Aguardando conexões na porta 5000...")
    app.run(port=5000)