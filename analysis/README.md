# Análise reproduzível

Esta pasta contém a camada estrutural reproduzível do diagnóstico. As decisões semânticas e a comparação final permanecem documentadas no cockpit público.

## `build_dataset.py`

Lê os três CSVs fornecidos, converte campos numéricos e booleanos, preserva `source_row`, reconcilia contagens e gera uma camada JSON tipada.

Para executar, coloque os arquivos autorizados em:

```text
analysis/data/
├── organic-competitors.csv
├── top-pages.csv
└── organic-keywords.csv
```

Na raiz do repositório:

```bash
python analysis/scripts/build_dataset.py
```

O JSON será gravado em `analysis/outputs/dataset.json`. Diretórios alternativos podem ser informados com `--source-dir` e `--output`.

Os CSVs não são distribuídos neste repositório.

## Escopo do código

O script cobre tipagem, preservação da linha-fonte e reconciliação de contagens. Taxonomia, fusões, elegibilidade e força da ponte dependem de contexto e estão expostas no cockpit com critérios, evidências e limites. O MCDA utiliza fórmulas auditáveis no próprio Google Sheets.

## Reprodutibilidade e privacidade

- o dado bruto permanece fora do GitHub;
- `source_row` conecta cada transformação à linha original;
- totais esperados falham de forma visível quando o input muda;
- nenhum script consulta concorrentes ou serviços externos;
- qualquer adaptação para outro dataset exige novo contrato de esquema.
