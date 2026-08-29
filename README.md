# Conversor de moedas — case de SEO e AEO para InfinitePay

Protótipo funcional e material técnico de um case de aquisição orgânica. A recomendação foi construída a partir de 829 registros fornecidos no desafio, passando por diagnóstico de qualidade, taxonomia, deduplicação, elegibilidade, análise multicritério e sensibilidade.

## Resumo executivo

Minha recomendação é construir um conversor de moedas em `/materiais/conversor-de-moedas`.

O conversor combinou demanda observada, baixa dificuldade no recorte, aderência defensável à InfinitePay e estabilidade quando as premissas do modelo foram alteradas. A página resolve primeiro a tarefa do usuário. Somente depois do cálculo, uma pergunta opcional identifica contexto de compra internacional e apresenta uma continuidade legítima para o Cartão de Crédito InfinitePay.

O caminho analítico foi:

```text
829 registros
→ 406 páginas classificadas
→ 45 páginas de ferramenta
→ 37 tarefas distintas
→ 33 candidatas
→ 6 elegíveis
→ 3 finalistas
→ 1 recomendação
```

Os dados permitem escolher a alternativa mais forte dentro do recorte. Eles não permitem prever tráfego, conversão ou receita. Por isso, a recomendação vem acompanhada de um roadmap de 90 dias para validar descoberta, utilidade, ativação e impacto de negócio em camadas separadas.

### Materiais

- [Análise, evidências e roadmap de 90 dias](https://docs.google.com/spreadsheets/d/1yRQ55ZR2J5SK3bCQIhVkVBmvOJc9aaN3cZ6WMWqt_yM/edit)
- [Demonstração funcional](https://marquesicaro-star.github.io/cloudwalk-seo-case-conversor-moedas/)
- Código, metodologia resumida e scripts reproduzíveis neste repositório

## Demonstração

[Abrir o conversor publicado no GitHub Pages](https://marquesicaro-star.github.io/cloudwalk-seo-case-conversor-moedas/)

A URL acima hospeda somente a demonstração técnica. A URL de produção recomendada para a InfinitePay é `/materiais/conversor-de-moedas`.

## Decisão

Propor uma página única em `/materiais/conversor-de-moedas`. Ela resolve primeiro a conversão com uma taxa de referência datada. Somente depois do cálculo, uma pergunta opcional identifica contexto de compra internacional e apresenta uma continuidade legítima para o Cartão de Crédito InfinitePay. O diretório segue o hub real de ferramentas da InfinitePay; o slug preserva o termo-cabeça observado.

O conversor obteve 90,0 no cenário-base do modelo multicritério, contra 82,8 do editor de imagem e 53,4 da calculadora de juros simples. Permaneceu em primeiro nos quatro cenários de peso e preservou nota e posição quando a evidência complementar foi retirada.

Esses números sustentam uma escolha comparativa dentro do recorte. Não são previsão de tráfego, conversão ou receita.

## Por que as outras finalistas não venceram

- **Editor de imagem:** ficou como fallback operacional. É mais simples de executar inteiramente no navegador, mas teve desempenho inferior ao conversor no modelo multicritério e nos quatro cenários de peso.
- **Calculadora de juros simples:** é determinística e fácil de demonstrar, mas apresentou uma combinação mais fraca de demanda, viabilidade competitiva e ponte de aquisição.

A facilidade de implementação não foi adicionada como um novo critério depois do ranking. Ela entrou como gate de viabilidade para impedir que conveniência técnica reordenasse retroativamente a decisão.

## Página

- HTML, CSS e JavaScript estáticos, sem etapa de build;
- conteúdo útil e headings disponíveis no HTML;
- title, description, canonical, robots e sitemap;
- `WebApplication` e `FAQPage` coerentes com o conteúdo visível;
- fonte e data da taxa junto ao resultado;
- taxa manual como fallback;
- instrumentação preparada em `window.dataLayer`;
- experiência responsiva e acessível;
- CTA comercial exibido somente após autoseleção de contexto.

## Executar localmente

Na raiz do repositório:

```bash
python -m http.server 8000
```

Depois, abra `http://localhost:8000`.

## Análise e estratégia

O [cockpit de análise e roadmap de 90 dias](https://docs.google.com/spreadsheets/d/1yRQ55ZR2J5SK3bCQIhVkVBmvOJc9aaN3cZ6WMWqt_yM/edit) contém:

- as três fontes preservadas e o diagnóstico de qualidade;
- as camadas derivadas de páginas e keywords;
- a passagem de 45 páginas de ferramenta para 37 tarefas;
- a formação de 33 candidatas e o filtro que manteve seis elegíveis;
- o MCDA, a shortlist, a comparação final e a sensibilidade;
- resumo executivo;
- roadmap SEO/AEO;
- arquitetura do conjunto de páginas.

O dataset original não está neste repositório. A camada reproduzível de tipagem e reconciliação está em [`analysis/scripts`](analysis/scripts), acompanhada de instruções de reuso e limites de escopo.

## Roadmap de 90 dias

- **Dias 0–30 — publicar e medir:** validar indexação, cálculo, eventos, qualidade técnica e governança da taxa de referência.
- **Dias 31–60 — aprender e otimizar:** agrupar consultas reais, analisar conclusão por dispositivo e origem, testar uma variável por vez e construir a camada AEO a partir das perguntas observadas.
- **Dias 61–90 — expandir com evidência:** criar páginas por par de moedas somente se houver intenção distinta, procura recorrente, utilidade própria e canibalização controlada; conectar o CTA às etapas posteriores do funil quando a infraestrutura permitir.

O roadmap completo, com métricas, guardrails e critérios de decisão, está no cockpit de análise.

## Uso de IA

A IA apoiou exploração, classificação provisória, fórmulas, código e documentação. O tratamento estrutural permaneceu reproduzível. Critérios, pesos e exceções foram revisados antes da aplicação; a confiança ficou separada da nota, e cenários de sensibilidade testaram as premissas relevantes.

## O que os dados não permitem concluir

- tráfego orgânico ou CTR futuro;
- participação capturável da demanda estimada;
- pares de moedas prioritários;
- proporção interessada em compra internacional;
- cadastro, aprovação, ativação, receita ou LTV;
- efeito causal de schema, AEO ou da ferramenta;
- inexistência absoluta de solução equivalente fora do protocolo executado.

## Estrutura

```text
.
├── index.html
├── styles.css
├── app.js
├── robots.txt
├── sitemap.xml
├── analysis/
│   ├── README.md
│   ├── METHODOLOGY.md
│   └── scripts/
└── scripts/
    └── audit_public_package.py
```

## Nota

Este é um protótipo de processo seletivo, não uma página oficial publicada pela InfinitePay. O canonical e o sitemap representam a URL de produção proposta, que ainda não existe no site da empresa. Para avaliar a implementação, use a demonstração no GitHub Pages indicada acima.
