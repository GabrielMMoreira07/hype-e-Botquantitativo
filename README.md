# 🎮📈 HYPE-E — Bot Quantitativo de Ações de Games

Robô em Python que sugere decisões de compra/venda de ações de quatro grandes empresas de jogos, com base no hype e nas críticas dos próximos lançamentos. A análise é feita por IA (Google Gemini), exposta por uma API em Flask e consumida por um frontend simples em HTML.

## Empresas acompanhadas
- CD Projekt (CDR.WA)
- - Electronic Arts (EA)
  - - Ubisoft (UBI.PA)
    - - Take-Two (TTWO)
     
      - ## Como funciona
      - O robô (agente.py) usa três etapas de IA:
     
      - 1. Pesquisador de lançamentos — busca os próximos jogos de cada empresa e suas datas.
        2. 2. Analista de hype (~60 dias antes) — avalia se a expectativa do público está BOA ou RUIM.
           3. 3. Analista de críticas (~5 dias antes) — avalia previews e reviews recentes.
             
              4. Com base na janela de tempo até o lançamento, o algoritmo gera uma decisão: COMPRAR, MANTER, VENDER ou ESPERAR.
             
              5. A API (api.py) expõe o endpoint GET /api/analise, que roda o algoritmo e devolve a recomendação em JSON. O index.html consome essa API e mostra o resultado.
             
              6. ## Tecnologias
              7. - Python (Flask, flask-cors)
                 - - Google Gemini (google-genai)
                   - - HTML e JavaScript no frontend
                    
                     - ## Como rodar
                     - ```bash
                       # 1. Instale as dependências
                       pip install flask flask-cors google-genai

                       # 2. Configure sua chave da API Gemini
                       export GENAI_API_KEY="sua-chave-aqui"

                       # 3. Inicie o servidor
                       python api.py
                       ```

                       O servidor sobe em http://localhost:5000 . Abra o index.html no navegador para ver as recomendações.

                       ## ⚠️ Aviso
                       Projeto de estudo. As recomendações são geradas por IA e não constituem recomendação de investimento.
                       
