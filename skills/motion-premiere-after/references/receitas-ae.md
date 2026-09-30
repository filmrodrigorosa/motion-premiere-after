# Receitas de tela (After Effects, via ae_do batch.run)

Medidas para 3840×2160. Em 1080p, divida por 2. Cores e fontes vêm da ficha de identidade: TÍTULO, ANOTAÇÃO, LEGENDA, ACENTO, CLARO, ESCURO.
Tempos relativos à comp. A comp começa um pouco antes da primeira palavra. Entrada = `layer.set_props {inPoint}` no quadro da palavra.
Trim End: `["ADBE Root Vectors Group","ADBE Vector Group","ADBE Vectors Group","ADBE Vector Filter - Trim","ADBE Vector Trim End"]`.
Shape layer: `transform.set position [0,0], anchorPoint [0,0]`, vértices em coordenadas da comp.

## Palavra-chave + logo
Anotação pequena (150) acima → palavra 1 em TÍTULO 400 → palavra 2 → sublinhado ACENTO 34 px (trim 0→55→100 em 3 quadros) → logo com escala 8→28→24% e giro lento posterizado. Tudo alinhado na margem (x≈280).

## Palavra circulada
Anotação (260) + palavra TÍTULO 320 + elipse à mão (path aberto de 6 pontos, stroke 22). Trim 0→100 em ~8 quadros. Escale a camada até a elipse envolver a palavra inteira.

## Lower third
Barra ACENTO vertical (trim 0→100 em 6 quadros) → nome TÍTULO 200 deslizando uns 50 px com overshoot → segunda linha LEGENDA 64, tracking 120. Saída: opacidade + Trim Start na barra.

## Lista / contraste
Item 1 TÍTULO 220 + check ACENTO à direita da palavra (não em cima) → item 2 → risco ACENTO atravessando a palavra toda no momento da fala negativa → anotação abaixo.

## Ideia / ferramenta citada
Seta curva ACENTO da cabeça até o logo (2 paths: curva + ponta, trim 0→100) → logo pop → anotação em 2 linhas perto do logo.

## CTA (descrição / link)
Null `CARD_RIG` pai de: card CLARO (retângulo 1320×400, arredondamento 14, rotação −1,5°) + TÍTULO 210 ESCURO + LEGENDA 54 ESCURO. O card sobe de fora do quadro com overshoot. Seta ACENTO curva apontando pra baixo. Saída: o rig desce.

## Título de bloco
Anotação ACENTO → linha 1 TÍTULO 380 → linha 2 + contorno vazado maior atrás (sem fill, stroke cinza, opacidade 70) deslizando devagar → sublinhado. Se termina num corte, não precisa de saída.

## Verificação
`ae_render_frame` (sai PNG com alpha) → `scripts/preview_sobre_video.sh <png> <tempo_timeline> <saida> <mapa.json> <video>` → olhe: sobreposição com o rosto, contraste, traços cobrindo a palavra.
