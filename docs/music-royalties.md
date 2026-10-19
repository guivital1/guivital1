# Engenharia de dados aplicada a royalties musicais

> Case técnico baseado na documentação pública de [MUV Royalties Ops](https://github.com/MUSICAS-DO-BRASIL/muv-royalties-ops). Referência consultada em 19/10/2026; marcos de execução mantêm suas datas originais.

## O problema

Recebimentos de royalties chegam por fontes e formatos diferentes. Preparar uma competência exige ler arquivos, interpretar campos, aplicar regras de negócio e conferir os resultados contra a operação financeira existente.

O desafio de engenharia é transformar essas etapas em processos reproduzíveis, preservando a origem e a capacidade de conciliar cada resultado.

## O fluxo de dados

```text
Arquivos de origem
      ↓
Leitura e staging
      ↓
Validação e normalização
      ↓
Regras de negócio e conciliação
      ↓
Planilhas operacionais + evidências de auditoria
```

| Decisão | Aplicação |
| --- | --- |
| Preservar a origem | Os documentos originais do operador não são movidos nem apagados pelas rotinas. |
| Tornar regras explícitas | Preparação, classificação e conciliação são tratadas em código Python. |
| Controlar duplicidade | Publicações SOCINPRO equivalentes preservam o demonstrativo existente; divergências bloqueiam a publicação. |
| Manter proveniência | Cada publicação SOCINPRO recebe evidências técnicas em diretório próprio. |
| Verificar recuperação | A validação sintética restaura arquivos e PostgreSQL em volumes novos e compara hashes e registros. |
| Separar código e operação | Documentos financeiros, credenciais e configurações operacionais ficam fora do controle de versão. |

## Evidências e limites

O [marco público de 21/09/2026](https://github.com/MUSICAS-DO-BRASIL/muv-royalties-ops#estado-atual) registra **227 testes aprovados e um skip de Windows**, além de validação Docker, persistência e restauração sintética. Esse número descreve aquele marco histórico.

A infraestrutura já verifica a saúde do PostgreSQL; a documentação desse marco ainda lista schema e persistência financeira como pendentes. Etapas de Excel COM exigem Windows, e testes sintéticos não substituem homologação financeira com documentos autorizados.

[Explorar código e documentação →](https://github.com/MUSICAS-DO-BRASIL/muv-royalties-ops) · [Voltar ao perfil](../README.md)
