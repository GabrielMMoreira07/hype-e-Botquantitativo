import datetime
import json
import os
from google import genai

class RoboNexus:
    def __init__(self):
        self.empresas = ["CD Projekt (CDR.WA)", "Electronic Arts (EA)", "Ubisoft (UBI.PA)", "Take-Two (TTWO)"]
        # Inicializa o cliente com o novo SDK oficial
        api_key = os.environ.get("GENAI_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def _limpar_texto_ia(self, texto):
        """Limpa a resposta da IA para o Python conseguir ler o JSON perfeitamente"""
        return texto.replace("```json", "").replace("```", "").strip()

    # ==========================================
    # IA 1: PESQUISADOR DE LANÇAMENTOS
    # ==========================================
    def pesquisar_proximos_jogos(self):
        prompt = f"""
        Pesquise e liste os 5 próximos lançamentos de jogos para cada uma destas empresas: {self.empresas}.
        Responda APENAS com um array JSON neste formato exato, sem textos adicionais:
        [
            {{"ticker": "EA", "jogo": "Battlefield 6", "data_lancamento": "2026-10-15"}}
        ]
        """
        resposta = self.client.models.generate_content(
           model='gemini-2.5-flash',
            contents=prompt
        )
        return json.loads(self._limpar_texto_ia(resposta.text))

    # ==========================================
    # IA 2: ANALISTA DE HYPE (Usado no D-60)
    # ==========================================
    def analisar_hype(self, jogo):
        prompt = f"""
        Analise a expectativa (hype) da internet para o jogo '{jogo}'.
        A expectativa está BOA ou RUIM? Responda APENAS com um JSON: {{"hype": "BOA"}} ou {{"hype": "RUIM"}}.
        """
        resposta = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return json.loads(self._limpar_texto_ia(resposta.text))

    # ==========================================
    # IA 3: ANALISTA DE CRÍTICAS (Usado no D-5)
    # ==========================================
    def analisar_criticas(self, jogo):
        prompt = f"""
        Analise as críticas, previews e vazamentos recentes do jogo '{jogo}'.
        Elas estão POSITIVAS ou NEGATIVAS (com bugs e reclamações)?
        Responda APENAS com um JSON: {{"criticas": "POSITIVAS"}} ou {{"criticas": "NEGATIVAS"}}.
        """
        resposta = self.client.models.generate_content(
            model=='gemini-2.5-flash',
            contents=prompt
        )
        return json.loads(self._limpar_texto_ia(resposta.text))

    # ==========================================
    # O MOTOR DE EXECUÇÃO
    # ==========================================
    def rodar_algoritmo(self):
        print("🤖 Iniciando rastreio de mercado...")
        hoje = datetime.date.today()
        
        # 1. A IA pesquisa o calendário
        agenda = self.pesquisar_proximos_jogos()
        
        relatorio_final = []

        # 2. O algoritmo passa por cada jogo analisando a data
        for evento in agenda:
            try:
                data_lanc = datetime.datetime.strptime(evento['data_lancamento'], '%Y-%m-%d').date()
            except:
                continue 
            
            jogo = evento['jogo']
            ticker = evento['ticker']

            faltam_60_dias = data_lanc - datetime.timedelta(days=60)
            faltam_5_dias = data_lanc - datetime.timedelta(days=5)
            passou_1_mes = data_lanc + datetime.timedelta(days=30)

            if hoje == faltam_60_dias:
                resultado = self.analisar_hype(jogo)
                if resultado.get('hype') == 'BOA':
                    relatorio_final.append({
                        "ticker": ticker,
                        "jogo": jogo,
                        "decisao": "COMPRAR",
                        "motivo": f"Faltam 2 meses. Hype verificado como BOM. Iniciando operação de compra."
                    })

            elif hoje == faltam_5_dias:
                resultado = self.analisar_criticas(jogo)
                if resultado.get('criticas') == 'NEGATIVAS':
                    relatorio_final.append({
                        "ticker": ticker,
                        "jogo": jogo,
                        "decisao": "VENDER",
                        "motivo": f"Faltam 5 dias. Críticas NEGATIVAS (Bugs/Problemas). Encerrando posição ou entrando Short."
                    })
                elif resultado.get('criticas') == 'POSITIVAS':
                    relatorio_final.append({
                        "ticker": ticker,
                        "jogo": jogo,
                        "decisao": "MANTER",
                        "motivo": f"Faltam 5 dias. Críticas POSITIVAS. Ação segura, mantendo na carteira."
                    })

            elif hoje == passou_1_mes:
                relatorio_final.append({
                    "ticker": ticker,
                    "jogo": jogo,
                    "decisao": "VENDER",
                    "motivo": f"Passou 1 mês do lançamento bem sucedido. Realizando lucros e saindo da operação."
                })

        if len(relatorio_final) == 0:
            return {
                "ticker": "GLOBAL",
                "jogo": "Mercado Geral",
                "decisao": "ESPERAR",
                "lucro_prejuizo": "0.00%",
                "motivo": "Nenhum jogo no calendário atingiu a janela de 2 meses, 5 dias ou +1 mês hoje."
            }
        
        alerta = relatorio_final[0]
        alerta["lucro_prejuizo"] = "Análise Ativa"
        return alerta