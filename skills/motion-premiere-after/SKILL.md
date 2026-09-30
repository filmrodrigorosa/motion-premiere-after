---
name: motion-premiere-after
description: Motion graphics de ponta a ponta para vídeos falados (YouTube, tutoriais, talking head) — lê a sequência aberta no Premiere Pro e a transcrição, sugere os momentos que merecem motion (palavras-chave, lower third, callouts, logos, listas, CTA, zooms), espera o usuário aprovar a tabela, anima no After Effects seguindo a identidade visual de um projeto de referência (.aep, vinheta, brand kit ou imagens), leva as comps pro Premiere por Dynamic Link, reenquadra a pessoa com zoom suave (ease) e coloca efeitos sonoros sincronizados. Use sempre que pedirem motion, animações, lower third, "anima os trechos fortes", "coloca motion nesse vídeo", zoom com ease, SFX nas animações, ou mandarem um .aep/vinheta pedindo animações no mesmo estilo — mesmo que não falem "skill".
---

# Motion: Premiere → After Effects → Premiere

Precisa de dois MCPs: `premiere-pro` (bridge CEP; catálogo via `search_tools` + `invoke_tool`) e `higgsfield-use-after-effects`. Antes de mexer no After, leia `ae_get_skill(name: "ae-clean-rig")`.

## 0. Perguntas (só o que não dá pra descobrir)
Pergunte de uma vez:
- Qual sequência? Se só tiver uma, use essa. A montagem está travada?
- Tem transcrição no Premiere, ou é preciso gerar?
- Quais tipos de motion quer, quanto (padrão bom: poucos, só os momentos mais fortes, nada poluído) e se quer zooms?
- Qual é a **referência de identidade** (.aep, imagens, brand kit)? As fontes estão instaladas?
- Lower third: nome e segunda linha (@, cargo). Logos: pode usar? Tem o arquivo?
- CTA: pra onde a seta aponta (descrição, card, comentário)?
- Onde salvar? (padrão: pasta do projeto de vídeo). Overlay por cima do vídeo, via Dynamic Link?
- Tem pasta de SFX? Se não tiver, pergunte se pode seguir sem som.
- **Aprovar a tabela antes de animar** é o padrão.

## 1. Ler o projeto
1. `verify_premiere_connection` → caminho do `.prproj`. Se o verificador de permissão falhar, tente de novo uma vez.
2. Transcrição: o Premiere guarda no `.prproj`. Se tiver uma skill de leitura de transcrição, use. Se não, exporte pelo painel Texto ou transcreva com whisper. Nomes de marca costumam vir errados (ex.: "Cloud" = Claude). Corrija na tabela.
3. Monte o mapa mídia→timeline: `list_sequence_tracks` + `get_clip_properties` (inPoint) de cada clipe, e salve como `mapa.json` (`[{"inicio","in","dur"}]`). `tl = inicio + (t_mídia − in)`. `scripts/mapa_palavras.py` converte as palavras da transcrição.
4. Confira o frame rate real. Uma sequência que "é 24" costuma ser 23,976 (duração de 100 quadros = 4,1708 s). As comps do AE têm que usar o mesmo valor.

## 2. Tabela de sugestões → aprovação
Colunas: # · timecode da timeline (HH:MM:SS:QQ) · fala · proposta · tipo. Critérios que funcionam:
- palavra-chave do tema dita com ênfase;
- lower third na primeira vez que a pessoa se apresenta ou diz o nome;
- comparação/lista quando ela contrasta coisas (✓ / riscado);
- logo quando cita a ferramenta;
- CTA com seta quando manda baixar/clicar;
- título na virada de bloco ("bora ver como funciona");
- zoom em ênfase ou piada.
Deixe respiros sem nada. Pare e espere a aprovação.

## 3. Extrair a identidade da referência
Siga `references/extrair-identidade.md`. O resultado é uma ficha curta: cores (RGB 0–1), fontes (PostScript), traços (cor, espessura, ponta), ritmo (keys hold? passos de 12 fps?), elementos recorrentes. Use a ficha como fonte única nas comps. Construa do zero. Precomps da referência só servem de consulta.

## 4. After Effects — construção
Receitas por tipo de tela em `references/receitas-ae.md`. Regras:
- Projeto novo na pasta do vídeo. Uma comp por tela `MG_NN_ASSUNTO`, na resolução e no fps da sequência, com duração = trecho da tela, numa pasta própria.
- Camada guia `REF_GUIA` com um quadro do vídeo (guia não renderiza). Camada de ajuste com Sombra projetada suave pra dar leitura sobre o vídeo, copiada entre as comps (`layer.copy_to_comp`).
- Entrada de cada elemento = **inPoint da camada** no quadro da palavra falada + pop curto (escala 112→100 em 2 quadros). Traços com Trim Paths. Saída = opacidade em ~4 quadros.
- Shape layer: zere Posição e Âncora (`[0,0]`) e use vértices em coordenadas da comp. `property.set` em caminho falha: pra alongar, escale a camada a partir da âncora.
- Coloque o design no espaço livre do quadro (olhe o quadro de verdade, não chute).
- **Verifique cada tela sobre o vídeo real**: `ae_render_frame` + `scripts/preview_sobre_video.sh`. Olhe a imagem e corrija antes de seguir.
- Salve o projeto (`ae_save_project`) antes de importar no Premiere.

## 5. Premiere — Dynamic Link, reenquadramento e zoom
Trechos prontos em `references/premiere-jsx.md` (`execute_extendscript`, arg `script`, **sempre com `return`**):
1. `importAEComps` num bin próprio → `overwriteClip` na V2 no quadro de início de cada tela.
2. **Reenquadrar** telas com texto grande: zoom na pessoa, que fica de lado, e o design ocupa o espaço livre. Se o editor já fez um reenquadramento no projeto, leia a escala e a posição dele (Motion via script) e reuse os valores. Corte V1+A1 nos limites da tela (`razor_timeline_at_time` só nas trilhas 0) e confira os cortes, que podem cair 1 quadro depois.
3. **Zoom sempre com ease**: grave a curva quadro a quadro (o script não confirma bezier). Entrada ~0,5 s. Saída suave só nos cortes que você fez; nos cortes do editor, mantenha o corte seco.
4. Keyframes de clipe usam **tempo de mídia** (`inPoint + tl − start`). Componente Motion = matchName `AE.ADBE Motion`, porque o nome de exibição muda com o idioma. Um clipe que nasce de um corte herda os keys do original: refaça.
5. Confira com `capture_frame` (ele acrescenta ".png" ao caminho). Salve com `app.project.save()`.

## 6. Efeitos sonoros
Mapa em `references/sfx.md`: traços/escrita/cliques numa trilha, impactos/passagens noutra, cada som no quadro da entrada do elemento. Avise que os sons ficaram em 0 dB e peça pra ouvir e ajustar.

## Armadilhas conhecidas (MCP premiere-pro)
- `import_media` com `binName` deixa o item na raiz. `batch_apply_effect` aplica em todos os clipes. `ripple_delete` não faz ripple. Evite os três.
- Ferramentas "expanded" têm schema aberto: leia os argumentos no código do pacote (`dist/tools/expanded.js`).
- Numa fonte manuscrita, teste as letras (ex.: "d" que parece "o") antes de usar em nomes.

## Entrega
Diga o que foi feito, com os tempos de cada tela e os arquivos. Diga o que foi verificado de verdade (quadros conferidos) e o que não foi (ex.: não ouviu a mixagem). Cite desvios da tabela e como desfazer. Ao mudar o texto no After, avise que o Premiere atualiza pelo Dynamic Link (se não atualizar: botão direito → Atualizar).
