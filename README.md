# Pipeline de Dados — NYC

Este é um projeto de Engenharia de Dados que desenvolve um pipeline para integrar dados de viagens de táxis amarelos de Nova York e dados climáticos.

## Fontes e fluxo de dados

1. **Viagens de táxi:** extração dos dados disponibilizados em arquivos Parquet.
2. **Dados climáticos:** extração pela API NASA POWER.
3. **Armazenamento intermediário:** os dados extraídos são armazenados no Amazon S3.
4. **Data Warehouse:** os dados são carregados no MySQL para apoiar consultas e análises.

O fluxo geral é:

**Parquet de viagens + API NASA POWER → Amazon S3 → MySQL**