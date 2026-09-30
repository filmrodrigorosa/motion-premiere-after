# Extrair a identidade visual de uma referência

## Se for um .aep
1. No projeto novo do AE: `project.import_file` com o .aep de referência (ele entra como pasta e não mexe no original).
2. `ae_project_info` → comps, sólidos (cores de fundo) e footage.
3. `font.list_used` → fontes (postScriptName) e onde aparecem. Veja se alguma é `isSubstitute` (fonte faltando).
4. `ae_render_frame` em 3–4 momentos da comp master → olhe a composição, a hierarquia e o uso de cor.
5. `ae_layer_info` (includeProperties=false) na comp mais rica → nomes das camadas, fillColor de cada texto, tamanhos.
6. `ae_layer_info` num traço/shape típico → cor do stroke, largura, arremate, estreitamento (taper), Trim Paths e o tipo de interpolação dos keys (6614 = hold → animação em passos).
7. Procure camada de controle (ex.: "CONTROLES" com cores em efeitos) e expressões de cor: é aí que fica a paleta oficial.

## Se forem imagens ou brand kit
Tire as cores dominantes (amostras) e identifique as fontes (pergunte se não souber). Descreva os elementos recorrentes.

## Ficha (preencha e mostre ao usuário em 3–5 linhas)
- **Cores**: fundo claro, fundo escuro, texto, acento (RGB 0–1 + hex)
- **Fontes**: título, apoio/anotação, legenda miúda
- **Traço**: cor, espessura na resolução final, ponta, forma de desenhar
- **Ritmo**: suave (bezier) ou em passos (`posterizeTime(12)` nos traços)
- **Elementos-assinatura**: ex.: contorno vazado atrás do título, sublinhado à mão, card, selo
- **Escala**: a referência costuma ser 1080p. Numa sequência 4K, dobre tamanhos e espessuras.
