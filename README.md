# motion-premiere-after

Skill para o **Claude Code** que faz motion graphics em vídeos falados, de ponta a ponta:

1. Lê a sequência aberta no **Premiere Pro** e a transcrição.
2. Sugere os momentos fortes (palavras-chave, lower third, listas, logos, CTA, zooms) numa tabela. **Você aprova antes.**
3. Extrai a identidade visual de uma referência sua (um `.aep` de vinheta, imagens ou brand kit).
4. Anima tudo no **After Effects**, com texto editável e o tempo casado com a fala.
5. Leva as comps para o Premiere por **Dynamic Link**, reenquadra você com **zoom suave (ease)** e coloca **efeitos sonoros** sincronizados.

## Requisitos
- macOS com **Premiere Pro** e **After Effects** instalados (testado nas versões 26.x / 2026)
- [Claude Code](https://claude.com/claude-code)
- [Node.js](https://nodejs.org/) 20+
- `ffmpeg` (para as prévias: `brew install ffmpeg`)

## 1. Instalar os dois MCPs
Os MCPs são de terceiros. Instale pelas fontes oficiais:

**Premiere Pro** — [hetpatel-11/Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP) (MIT)
```bash
npm install -g adobe-premiere-pro-mcp
premiere-pro-mcp --install-cep
premiere-pro-mcp --doctor
```
Reinicie o Premiere e abra `Janela > Extensões > MCP Bridge (CEP)`. Siga o README do projeto para registrar no Claude Code, se o instalador não fizer isso sozinho.

**After Effects** — pacote npm [`fnf-after-effects-mcp`](https://www.npmjs.com/package/fnf-after-effects-mcp) ("Higgsfield use After Effects")
```bash
npm install -g fnf-after-effects-mcp
fnf-after-effects doctor
fnf-after-effects config
```
Adicione ao Claude Code a entrada que o `config` imprimir, com o nome `higgsfield-use-after-effects`. No After, ative **Permitir que scripts gravem arquivos e acessem a rede**.

## 2. Instalar a skill
No Claude Code:
```
/plugin marketplace add filmrodrigorosa/motion-premiere-after
/plugin install motion-premiere-after@filmrodrigorosa
```
Ou copie manualmente a pasta `skills/motion-premiere-after` para `~/.claude/skills/`.

## 3. Usar
Com o Premiere (sequência aberta + MCP Bridge ligado) e o After abertos:
```
/motion-premiere-after anima os trechos fortes desse vídeo; a referência visual é /caminho/da/vinheta.aep
```
Ou só peça: "coloca motion nesse vídeo", "faz lower third e as animações dos momentos fortes".

A skill faz algumas perguntas (lower third, CTA, SFX, onde salvar), mostra a tabela de sugestões e só anima depois do seu ok.

## Dicas
- A sequência "24p" costuma ser **23,976**. A skill confere e casa o fps das comps.
- Use a sua própria pasta de SFX (a da vinheta é ideal). A skill não baixa sons.
- Teste a fonte manuscrita antes de usar em nomes: algumas deixam o "d" parecido com "o".

## Licença
MIT. Os MCPs citados têm licenças próprias.
