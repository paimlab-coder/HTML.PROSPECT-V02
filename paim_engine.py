# -*- coding: utf-8 -*-
from __future__ import annotations
import csv, io, json, math, os, re, ssl, subprocess, sys, threading, time, urllib.parse, urllib.request, webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

HOST='127.0.0.1'; PORT=int(os.environ.get('PAIM_PORT','8000'))
TARGET=Path(r'C:\Users\diogo.paim\Downloads\PAIM_IA_PROSPECT_DEFINITIVO_BRASIL')
INDEX=TARGET/'index.html'; CACHE=TARGET/'cache_overture'; CACHE_TTL=24*3600
HTML_ESCAPED=r'''﻿&lt;!doctype html&gt;
&lt;html lang="pt-BR"&gt;
    &lt;head&gt;
        &lt;meta charset="utf-8"&gt;
        &lt;meta name="viewport" content="width=device-width,initial-scale=1"&gt;
        &lt;title&gt;PAIM IA PROSPECT VER46 DEFINITIVO BRASIL · LIMITE 1500 · Bertolini BSA&lt;/title&gt;
        &lt;style&gt;
            :root {
                --b: #06418a;
                --n: #042c5e;
                --o: #f58220;
                --bg: #f3f6fa;
                --ink: #172536;
                --mut: #637083;
                --line: #dce3ec
            }
            * { box-sizing: border-box }
            body { margin: 0; background: var(--bg); color: var(--ink); font: 14px/1.45 system-ui,Arial,sans-serif }
            .app { display: flex; min-height: 100vh }
            .side { width: 235px; flex: 0 0 235px; background: var(--b); color: white }
            .brand { background: var(--n); padding: 19px 14px; border-bottom: 3px solid var(--o) }
            .brand b { display: block }
            .brand small { color: #d7e4f3 }
            .nav { padding: 8px }
            .nav button { display: block; width: 100%; text-align: left; border: 0; border-radius: 7px; background: none; color: #e3eaf2; padding: 10px; cursor: pointer; font-weight: 650; margin-bottom: 2px; }
            .nav button.active,.nav button:hover { background: var(--o); color: white }
            .sf { padding: 12px; font-size: 11px; color: #d7e4f3 }
            .main { min-width: 0; flex: 1; max-height: 100vh; display: flex; flex-direction: column }
            .top { height: 52px; flex: 0 0 52px; background: white; border-bottom: 1px solid var(--line); padding: 0 18px; display: flex; align-items: center; justify-content: space-between }
            .top b { color: var(--b) }
            .content { padding: 18px; overflow: auto; flex: 1 }
            .view { display: none }
            .view.active { display: block }
            h1 { font-size: 23px; color: var(--b); margin: 0 0 5px }
            .sub,.small,.tag { font-size: 12px; color: var(--mut) }
            .sub { margin: 0 0 14px }
            .notice { background: #fff8e8; border: 1px solid #f0d18b; border-left: 5px solid var(--o); padding: 12px; border-radius: 8px; margin-bottom: 14px }
            .card { background: white; border: 1px solid var(--line); border-radius: 9px; padding: 15px; margin: 0 0 14px }
            .card h2 { font-size: 16px; color: var(--b); margin: 0 0 11px }
            .kpis { display: grid; grid-template-columns: repeat(auto-fit,minmax(145px,1fr)); gap: 9px; margin: 12px 0 }
            .kpi { background: white; border: 1px solid var(--line); border-radius: 8px; padding: 11px }
            .kpi span { display: block; font-size: 12px; color: var(--mut) }
            .kpi b { display: block; font-size: 23px; color: var(--b) }
            .row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center }
            .btn { border: 0; border-radius: 7px; background: var(--b); color: white; padding: 9px 12px; font-weight: 700; cursor: pointer; text-decoration: none; display: inline-block }
            .btn.orange { background: var(--o) }
            .btn.light { background: #e7edf5; color: var(--n) }
            .btn:disabled { opacity: .45 }
            .file-box { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px }
            .drop-zone { padding: 16px; border: 2px dashed #91a6c1; border-radius: 8px; background: #f8fbff; text-align: center; cursor: pointer }
            .file { padding: 9px; border: 1px dashed #91a6c1; border-radius: 7px; background: #f8fbff; max-width: 100% }
            .filters { display: grid; grid-template-columns: repeat(auto-fit,minmax(140px,1fr)); gap: 8px }
            .filters label { font-size: 12px; color: var(--mut); font-weight: 650 }
            .filters input,.filters select { display: block; width: 100%; padding: 8px; margin-top: 4px; border: 1px solid #c7d1de; border-radius: 6px; background: white }
            .tablebox { overflow: auto; max-height: 60vh; border: 1px solid var(--line); border-radius: 7px }
            table { border-collapse: collapse; width: 100%; min-width: 880px; font-size: 12px; background: white }
            th { position: sticky; top: 0; background: var(--b); color: white; text-align: left; padding: 9px; white-space: nowrap }
            td { padding: 8px; border-bottom: 1px solid #e7ecf2; vertical-align: top; max-width: 260px; overflow-wrap: anywhere }
            tr:nth-child(even) td { background: #f8fafc }
            .empty { text-align: center; padding: 25px; color: var(--mut) }
            .pill { border-radius: 99px; padding: 3px 7px; font-size: 11px; font-weight: 700; white-space: nowrap }
            .high { background: #dcfce7; color: #176b45 }
            .map-controls { display: grid; grid-template-columns: repeat(auto-fit,minmax(155px,1fr)); gap: 9px }
            .map-controls label { font-size: 11px; color: var(--mut); font-weight: 700 }
            .map-controls input,.map-controls select { width: 100%; padding: 8px; margin-top: 4px; border: 1px solid #c7d1de; border-radius: 6px; background: white }
            .map-actions { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px }
            .map-layout { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(450px, 1fr); gap: 14px }
            .card-header-flex { display: flex; justify-content: space-between; align-items: center; margin-bottom: 11px }
            .card-header-flex h3 { margin: 0; font-size: 16px; color: var(--b) }
            .map-note { margin-top: 10px; padding: 10px; background: #f3f7fb; border-left: 4px solid var(--o); border-radius: 6px; font-size: 12px }
            .filter-summary { margin: 10px 0; padding: 10px; background: #eef5ff; border-radius: 7px; color: var(--n); font-weight: 650 }
            .map-legend { background: white; padding: 10px 14px; border-radius: 8px; border: 1px solid var(--line); font-size: 11px; display: flex; flex-wrap: wrap; gap: 12px; margin-top: 10px }
            .legend-item { display: flex; align-items: center; gap: 6px; font-weight: 600 }
            .legend-icon { width: 12px; height: 12px; border-radius: 50%; display: inline-block }
            @media(max-width: 1100px) { .map-layout { grid-template-columns: 1fr } }
        &lt;/style&gt;
        &lt;!-- SheetJS --&gt;
        &lt;script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"&gt;&lt;/script&gt;
    
&lt;style id="ver30-map-styles"&gt;
.native-map{position:relative;overflow:hidden;min-height:550px;background:linear-gradient(145deg,#dbeaf4,#eef6e9 52%,#d7e8f2);border:1px solid #b9ccd9;border-radius:8px}.native-map-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(6,65,138,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(6,65,138,.08) 1px,transparent 1px);background-size:52px 52px}.native-label{position:absolute;font-size:12px;font-weight:700;color:#365d75}.native-pin{position:absolute;width:23px;height:23px;border:3px solid #fff;border-radius:50% 50% 50% 0;background:#f58220;box-shadow:0 3px 10px #0005;transform:translate(-50%,-100%) rotate(-45deg);z-index:3}.native-pin.internal{background:#06418a}.native-pin span{display:none;position:absolute;left:18px;top:-9px;transform:rotate(45deg);width:220px;background:#fff;color:#172536;padding:9px;border:1px solid #cad8e2;border-radius:7px;box-shadow:0 7px 18px #0003;font:12px/1.35 system-ui}.native-pin:hover{z-index:9}.native-pin:hover span{display:block}.native-map-badge{position:absolute;left:10px;bottom:10px;background:#fffffff2;padding:7px 10px;border:1px solid #c7d6e0;border-radius:7px;font-size:11px;z-index:7}.heat-dot{position:absolute;border-radius:50%;transform:translate(-50%,-50%);background:radial-gradient(circle,#f58220bb 0,#ffca36aa 34%,#1f78ff44 67%,transparent 72%);filter:blur(1px)}.bubble-dot{position:absolute;border-radius:50%;transform:translate(-50%,-50%);background:#06418abb;border:2px solid white;color:white;display:grid;place-items:center;font-size:10px;font-weight:800}.uf-grid{position:absolute;inset:45px 20px 40px;display:grid;grid-template-columns:repeat(6,1fr);gap:7px;align-content:center}.uf-cell{min-height:55px;border-radius:7px;display:grid;place-items:center;text-align:center;color:white;font-weight:800;padding:5px;box-shadow:inset 0 0 0 1px #ffffff55}.map-loading{position:absolute;inset:0;display:grid;place-items:center;background:#ffffffd9;z-index:20;text-align:center;padding:30px;color:#06418a;font-weight:800}.small-action{border:0;border-radius:5px;padding:4px 7px;background:#e7edf5;color:#042c5e;cursor:pointer}.source-note{font-size:11px;color:#637083;margin-top:6px}
&lt;/style&gt;

&lt;/head&gt;
    &lt;body&gt;
        &lt;div class="app"&gt;
            &lt;aside class="side"&gt;
                &lt;div class="brand"&gt;
                    &lt;b&gt;PAIM IA PROSPECT&lt;/b&gt;
                    &lt;small&gt;Bertolini Intralogística · VER46 DEFINITIVO&lt;/small&gt;
                &lt;/div&gt;
                &lt;nav class="nav" id="nav"&gt;
                    &lt;button class="active" data-tab="dash"&gt;▦ Dashboard Principal&lt;/button&gt;
                    &lt;button data-tab="bases"&gt;⇧ Central de Bases&lt;/button&gt;
                    &lt;button data-tab="search"&gt;⌕ Busca &amp;amp; Mercado (Hub)&lt;/button&gt;
                    &lt;button data-tab="geomapbase"&gt;◉ Mapa Hub Base&lt;/button&gt;
                    &lt;button data-tab="profile"&gt;▣ Empresa 360°&lt;/button&gt;
                    &lt;button data-tab="geomap"&gt;◉ Mapa de Prospecção&lt;/button&gt;
                    &lt;button data-tab="radar"&gt;◉ Radar de Mercado&lt;/button&gt;
                    &lt;button data-tab="icp"&gt;⚙ ICP &amp;amp; Score&lt;/button&gt;
                    &lt;button data-tab="opp"&gt;◎ Fila de Oportunidades&lt;/button&gt;
                    &lt;button data-tab="bdr"&gt;☷ Listas para BDR&lt;/button&gt;
                    &lt;button data-tab="sources"&gt;◌ Fontes Monitoradas&lt;/button&gt;
                    &lt;button data-tab="gov"&gt;◇ Configurações &amp;amp; Governança&lt;/button&gt;
                &lt;/nav&gt;
                &lt;div class="sf"&gt;Dados na memória da página. Exporte antes de fechar.&lt;/div&gt;
            &lt;/aside&gt;
            &lt;div class="main"&gt;
                &lt;header class="top"&gt;
                    &lt;b&gt;PAIM IA PROSPECT · MOTOR B2B BSA&lt;/b&gt;
                    &lt;span class="tag" id="topStatus"&gt;Nenhuma base carregada&lt;/span&gt;
                &lt;/header&gt;
                &lt;main class="content"&gt;
                    &lt;!-- DASHBOARD --&gt;
                    &lt;section class="view active" id="v-dash"&gt;
                        &lt;h1&gt;Dashboard Principal&lt;/h1&gt;
                        &lt;p class="sub"&gt;Resumo das cargas, sinais de mercado e contas qualificadas.&lt;/p&gt;
                        &lt;div class="notice"&gt;
                            &lt;b&gt;Plataforma ativa:&lt;/b&gt; importe um arquivo no Mapa do Hub ou utilize o Mapa de Prospecção para consultar fontes externas.
                        &lt;/div&gt;
                        &lt;div id="activeFilterSummary" class="filter-summary"&gt;Filtro atual: todos os registros&lt;/div&gt;
                        &lt;div class="kpis"&gt;
                            &lt;div class="kpi"&gt;&lt;span&gt;Empresas&lt;/span&gt;&lt;b id="dTotal"&gt;0&lt;/b&gt;&lt;/div&gt;
                            &lt;div class="kpi"&gt;&lt;span&gt;Prioridade alta&lt;/span&gt;&lt;b id="dHigh"&gt;0&lt;/b&gt;&lt;/div&gt;
                            &lt;div class="kpi"&gt;&lt;span&gt;Movimentações&lt;/span&gt;&lt;b id="dMoves"&gt;0&lt;/b&gt;&lt;/div&gt;
                            &lt;div class="kpi"&gt;&lt;span&gt;Com responsável&lt;/span&gt;&lt;b id="dResp"&gt;0&lt;/b&gt;&lt;/div&gt;
                            &lt;div class="kpi"&gt;&lt;span&gt;No filtro atual&lt;/span&gt;&lt;b id="dFiltered"&gt;0&lt;/b&gt;&lt;/div&gt;
                            &lt;div class="kpi"&gt;&lt;span&gt;Com telefone&lt;/span&gt;&lt;b id="dPhone"&gt;0&lt;/b&gt;&lt;/div&gt;
                            &lt;div class="kpi"&gt;&lt;span&gt;Com e-mail&lt;/span&gt;&lt;b id="dEmail"&gt;0&lt;/b&gt;&lt;/div&gt;
                        &lt;/div&gt;
                        &lt;div class="card"&gt;
                            &lt;h2&gt;Segmentos da base&lt;/h2&gt;
                            &lt;div id="segments" class="empty"&gt;Carregando segmentos...&lt;/div&gt;
                        &lt;/div&gt;
                    &lt;/section&gt;
                    &lt;!-- CENTRAL DE BASES --&gt;
                    &lt;section class="view" id="v-bases"&gt;
                        &lt;h1&gt;Central de Ingestão de Bases (XLSX / CSV)&lt;/h1&gt;
                        &lt;p class="sub"&gt;Importe arquivos de sua base nas zonas de upload abaixo para preenchimento dinâmico e preservação integral de colunas.&lt;/p&gt;
                        &lt;div class="file-box"&gt;
                            &lt;div class="drop-zone" onclick="document.getElementById('files').click()"&gt;
                                &lt;b&gt;1. Upload de Base Cadastral (XLSX/CSV)&lt;/b&gt;
                                &lt;p class="small"&gt;Listas da Receita Federal ou clientes&lt;/p&gt;
                            &lt;/div&gt;
                            &lt;div class="drop-zone" onclick="document.getElementById('files').click()"&gt;
                                &lt;b&gt;2. Upload de Sinais / Projetos (XLSX/CSV)&lt;/b&gt;
                                &lt;p class="small"&gt;Planilhas de investimentos ou mercado&lt;/p&gt;
                            &lt;/div&gt;
                        &lt;/div&gt;
                        &lt;div class="card"&gt;
                            &lt;h2&gt;Gerenciar Importação&lt;/h2&gt;
                            &lt;div class="row"&gt;
                                &lt;input class="file" id="files" type="file" accept=".csv,.txt,.xlsx,.xls" multiple&gt;
                                &lt;button class="btn" id="importBtn"&gt;Processar e Alimentar Base&lt;/button&gt;
                                &lt;button class="btn orange" id="exportBtn"&gt;Exportar Consolidado CSV&lt;/button&gt;
                                &lt;button class="btn light" id="clearBtn"&gt;Limpar Sessão&lt;/button&gt;
                            &lt;/div&gt;
                            &lt;div class="status" id="importStatus" style="margin-top:10px"&gt;Nenhuma base importada.&lt;/div&gt;
                        &lt;/div&gt;
                        &lt;div class="card"&gt;
                            &lt;h2&gt;Pré-visualização da Base Carregada (Todas as Colunas Preservadas)&lt;/h2&gt;
                            &lt;div class="tablebox"&gt;
                                &lt;table&gt;
                                    &lt;thead&gt;&lt;tr id="dynamicHeaders"&gt;&lt;th&gt;Carregue um arquivo para ver as colunas&lt;/th&gt;&lt;/tr&gt;&lt;/thead&gt;
                                    &lt;tbody id="dynamicRows"&gt;&lt;tr&gt;&lt;td class="empty"&gt;Nenhum dado importado na sessão.&lt;/td&gt;&lt;/tr&gt;&lt;/tbody&gt;
                                &lt;/table&gt;
                            &lt;/div&gt;
                        &lt;/div&gt;
                    &lt;/section&gt;
                    &lt;!-- BUSCA (HUB) --&gt;
                    &lt;section class="view" id="v-search"&gt;
                        &lt;h1&gt;Busca Empresarial e Inteligência de Mercado (Hub)&lt;/h1&gt;
                        &lt;div class="card"&gt;
                            &lt;div class="filters"&gt;
                                &lt;label&gt;País&lt;select id="fCountry" onchange="loadSearchStates()"&gt;&lt;/select&gt;&lt;/label&gt;
                                &lt;label&gt;Estado / UF&lt;select id="fUf" onchange="loadSearchCities()"&gt;&lt;option value=""&gt;Todos os Estados&lt;/option&gt;&lt;/select&gt;&lt;/label&gt;
                                &lt;label&gt;Cidade&lt;select id="fCity"&gt;&lt;option value=""&gt;Todas as Cidades&lt;/option&gt;&lt;/select&gt;&lt;/label&gt;
                                &lt;label&gt;Segmento&lt;select id="fSegment"&gt;&lt;option value=""&gt;Todos os Segmentos&lt;/option&gt;&lt;/select&gt;&lt;/label&gt;
                                &lt;label&gt;Busca livre&lt;input id="fText" placeholder="Empresa, CNPJ..."&gt;&lt;/label&gt;
                            &lt;/div&gt;
                            &lt;div class="row" style="margin-top:10px"&gt;
                                &lt;button class="btn" onclick="triggerHubSearch()"&gt;Atualizar Filtros&lt;/button&gt;
                                &lt;button class="btn light" onclick="clearHubFilters()"&gt;Limpar Filtros&lt;/button&gt;
                            &lt;/div&gt;
                        &lt;/div&gt;
                        &lt;div class="card"&gt;
                            &lt;h2&gt;Empresas no Hub &lt;span id="searchCount" class="tag"&gt;&lt;/span&gt;&lt;/h2&gt;
                            &lt;div class="tablebox"&gt;
                                &lt;table&gt;
                                    &lt;thead&gt;
                                        &lt;tr&gt;
                                            &lt;th&gt;Score&lt;/th&gt;&lt;th&gt;Empresa&lt;/th&gt;&lt;th&gt;CNPJ&lt;/th&gt;&lt;th&gt;Segmento&lt;/th&gt;&lt;th&gt;Cidade/UF&lt;/th&gt;&lt;th&gt;Contato&lt;/th&gt;
                                        &lt;/tr&gt;
                                    &lt;/thead&gt;
                                    &lt;tbody id="searchRows"&gt;&lt;/tbody&gt;
                                &lt;/table&gt;
                            &lt;/div&gt;
                        &lt;/div&gt;
                    &lt;/section&gt;
                    &lt;!-- MAPA HUB BASE --&gt;
                    &lt;section class="view" id="v-geomapbase"&gt;
                        &lt;h1&gt;Mapa do Hub · Base Importada&lt;/h1&gt;
                        &lt;p class="sub"&gt;Análise geográfica exclusiva dos dados carregados por Excel/CSV. Não consulta fontes externas.&lt;/p&gt;
                        &lt;div class="card"&gt;
                            &lt;div class="map-controls"&gt;
                                &lt;div&gt;&lt;label&gt;PAÍS&lt;/label&gt;&lt;select id="mbCountry" onchange="loadHbStates()"&gt;&lt;/select&gt;&lt;/div&gt;
                                &lt;div&gt;&lt;label&gt;ESTADO / UF&lt;/label&gt;&lt;select id="mbUf" onchange="loadHbCities()"&gt;&lt;option value=""&gt;Todos&lt;/option&gt;&lt;/select&gt;&lt;/div&gt;
                                &lt;div&gt;&lt;label&gt;CIDADE&lt;/label&gt;&lt;select id="mbCity"&gt;&lt;option value=""&gt;Todas&lt;/option&gt;&lt;/select&gt;&lt;/div&gt;
                                &lt;div&gt;&lt;label&gt;SEGMENTO&lt;/label&gt;&lt;select id="mbSegment"&gt;&lt;option value=""&gt;Todos os Segmentos&lt;/option&gt;&lt;/select&gt;&lt;/div&gt;
                            &lt;/div&gt;
                            &lt;div class="map-actions"&gt;
                                &lt;button class="btn primary" onclick="refreshMapBase()"&gt;Atualizar Mapa Hub Base&lt;/button&gt;
                                &lt;button class="btn orange" onclick="exportMapBaseXlsx()"&gt;Exportar XLSX&lt;/button&gt;
                                &lt;button class="btn light" onclick="exportMapBaseCsv()"&gt;Exportar CSV&lt;/button&gt;
                            &lt;/div&gt;
                            &lt;div class="row" style="margin-top:10px"&gt;
                                    &lt;label&gt;VISUALIZAÇÃO &lt;select id="hubMapMode" class="file" style="width:auto"&gt;&lt;option value="markers"&gt;Marcadores&lt;/option&gt;&lt;option value="heat"&gt;Mapa de calor&lt;/option&gt;&lt;option value="bubbles"&gt;Bolhas proporcionais&lt;/option&gt;&lt;option value="choropleth"&gt;Coroplético por UF&lt;/option&gt;&lt;/select&gt;&lt;/label&gt;
                                    &lt;span class="tag" id="hubSourceTag"&gt;Fonte: arquivo local Excel/CSV&lt;/span&gt;
                                &lt;/div&gt;
                                &lt;div class="map-legend" id="mapBaseLegend"&gt;&lt;/div&gt;
                        &lt;/div&gt;
                        &lt;div class="map-layout"&gt;
                            &lt;div id="prospectMapBase" style="height:550px;border-radius:8px"&gt;&lt;/div&gt;
                            &lt;aside class="card"&gt;
                                &lt;div class="card-header-flex"&gt;
                                    &lt;h3&gt;Empresas no Mapa Hub Base&lt;/h3&gt;
                                    &lt;span id="mapBaseCount" class="tag"&gt;0 contas&lt;/span&gt;
                                &lt;/div&gt;
                                &lt;div class="tablebox" style="max-height:480px"&gt;
                                    &lt;table&gt;
                                        &lt;thead&gt;
                                            &lt;tr&gt;
                                                &lt;th&gt;Empresa&lt;/th&gt;&lt;th&gt;CNPJ&lt;/th&gt;&lt;th&gt;Segmento&lt;/th&gt;&lt;th&gt;Cidade/UF&lt;/th&gt;&lt;th&gt;Score&lt;/th&gt;
                                            &lt;/tr&gt;
                                        &lt;/thead&gt;
                                        &lt;tbody id="mapBaseTableBody"&gt;
                                            &lt;tr&gt;&lt;td colspan="5" class="empty"&gt;Nenhuma empresa encontrada.&lt;/td&gt;&lt;/tr&gt;
                                        &lt;/tbody&gt;
                                    &lt;/table&gt;
                                &lt;/div&gt;
                            &lt;/aside&gt;
                        &lt;/div&gt;
                    &lt;/section&gt;
                    &lt;!-- EMPRESA 360 --&gt;
                    &lt;section class="view" id="v-profile"&gt;
                        &lt;h1&gt;Empresa 360°&lt;/h1&gt;
                        &lt;div class="card"&gt;
                            &lt;select id="profileSelect" class="file" style="width:100%"&gt;&lt;option value=""&gt;Selecione uma empresa&lt;/option&gt;&lt;/select&gt;
                            &lt;div id="profile" class="status" style="margin-top:10px"&gt;Selecione uma empresa acima.&lt;/div&gt;
                        &lt;/div&gt;
                    &lt;/section&gt;
                    &lt;!-- MAPA DE PROSPECÇÃO --&gt;
                    &lt;section class="view" id="v-geomap"&gt;
                        &lt;h1&gt;Mapa de Prospecção Externa&lt;/h1&gt;
                        &lt;div class="card"&gt;
                            &lt;div class="map-controls"&gt;
                                &lt;div&gt;&lt;label&gt;PAÍS&lt;/label&gt;&lt;select id="mCountry" onchange="loadMapStates()"&gt;&lt;/select&gt;&lt;/div&gt;
                                &lt;div&gt;&lt;label&gt;ESTADO / PROVÍNCIA&lt;/label&gt;&lt;select id="mUf" onchange="loadMapCities()"&gt;&lt;option value=""&gt;Todos&lt;/option&gt;&lt;/select&gt;&lt;/div&gt;
                                &lt;div&gt;&lt;label&gt;CIDADE&lt;/label&gt;&lt;select id="mCity"&gt;&lt;option value=""&gt;Todas&lt;/option&gt;&lt;/select&gt;&lt;/div&gt;
                                &lt;div&gt;&lt;label&gt;SEGMENTO&lt;/label&gt;&lt;select id="mSegment"&gt;&lt;option value=""&gt;Todos os Segmentos&lt;/option&gt;&lt;/select&gt;&lt;/div&gt;
                                &lt;div&gt;&lt;label&gt;RAIO: &lt;b id="mRadiusLabel"&gt;60 km&lt;/b&gt;&lt;/label&gt;&lt;input id="mRadius" type="range" min="5" max="100" step="5" value="60"&gt;&lt;/div&gt;
                                &lt;div&gt;&lt;label&gt;SCORE DE CONTATO&lt;/label&gt;&lt;select id="mScore"&gt;&lt;option value="0"&gt;Todos&lt;/option&gt;&lt;option value="45"&gt;45+&lt;/option&gt;&lt;option value="70"&gt;70+&lt;/option&gt;&lt;/select&gt;&lt;/div&gt;
                                &lt;div&gt;&lt;label&gt;LIMITE&lt;/label&gt;&lt;select id="mLimit"&gt;&lt;option&gt;25&lt;/option&gt;&lt;option selected&gt;50&lt;/option&gt;&lt;option&gt;100&lt;/option&gt;&lt;option&gt;200&lt;/option&gt;&lt;option&gt;500&lt;/option&gt;&lt;option&gt;1000&lt;/option&gt;&lt;option&gt;1500&lt;/option&gt;&lt;/select&gt;&lt;/div&gt;
                            &lt;/div&gt;
                            &lt;div class="map-actions"&gt;
                                &lt;button class="btn primary" id="mSearch"&gt;Prospectar com Overture Maps&lt;/button&gt;
                                &lt;button class="btn orange" id="mGoogle"&gt;Consultar no Google Maps&lt;/button&gt;
                                &lt;button class="btn light" id="mExport"&gt;Exportar Prospects CSV&lt;/button&gt;&lt;button class="btn orange" id="mAddBdr"&gt;Adicionar selecionados à Lista BDR&lt;/button&gt;
                                &lt;button class="btn light" onclick="clearMapFilters()"&gt;Limpar Filtros&lt;/button&gt;
                            &lt;/div&gt;
                            &lt;div class="map-note" id="mStatus"&gt;Selecione Estado, Cidade e Segmento. A prospecção usa Overture Maps, sem Google, API Key ou Overpass.&lt;/div&gt;
                        &lt;/div&gt;
                        &lt;div class="map-layout"&gt;
                            &lt;div id="prospectMap" style="height:550px;border-radius:8px"&gt;&lt;/div&gt;
                            &lt;aside class="card"&gt;
                                &lt;div class="card-header-flex"&gt;
                                    &lt;h3&gt;Empresas encontradas&lt;/h3&gt;
                                    &lt;div&gt;
                                        &lt;button class="btn orange" style="padding: 5px 10px; font-size: 11px;" id="btnExportMapXlsx"&gt;Exportar XLSX&lt;/button&gt;
                                        &lt;button class="btn light" style="padding: 5px 10px; font-size: 11px;" id="btnExportMapCSVTop"&gt;Exportar CSV&lt;/button&gt;
                                    &lt;/div&gt;
                                &lt;/div&gt;
                                &lt;div class="tablebox" style="max-height:480px"&gt;
                                    &lt;table&gt;
                                        &lt;thead&gt;
                                            &lt;tr&gt;
                                                &lt;th&gt;&lt;input type="checkbox" id="selectAllProspects" title="Selecionar todos"&gt;&lt;/th&gt;&lt;th&gt;Empresa&lt;/th&gt;&lt;th&gt;Origem&lt;/th&gt;&lt;th&gt;Segmento&lt;/th&gt;&lt;th&gt;Cidade/UF&lt;/th&gt;&lt;th&gt;Telefone / E-mail / Site&lt;/th&gt;&lt;th&gt;Score contato&lt;/th&gt;
                                            &lt;/tr&gt;
                                        &lt;/thead&gt;
                                        &lt;tbody id="mapCompanyTableBody"&gt;
                                            &lt;tr&gt;&lt;td colspan="7" class="empty"&gt;Nenhuma empresa encontrada com os filtros atuais.&lt;/td&gt;&lt;/tr&gt;
                                        &lt;/tbody&gt;
                                    &lt;/table&gt;
                                &lt;/div&gt;
                            &lt;/aside&gt;
                        &lt;/div&gt;
                    &lt;/section&gt;
                    &lt;!-- RADAR --&gt;
                    &lt;section class="view" id="v-radar"&gt;
                        &lt;h1&gt;Radar de Mercado&lt;/h1&gt;
                        &lt;div class="card"&gt;&lt;div class="tablebox"&gt;&lt;table&gt;&lt;thead&gt;&lt;tr&gt;&lt;th&gt;Empresa&lt;/th&gt;&lt;th&gt;Movimentação&lt;/th&gt;&lt;th&gt;Local&lt;/th&gt;&lt;/tr&gt;&lt;/thead&gt;&lt;tbody id="radarRows"&gt;&lt;tr&gt;&lt;td colspan="3" class="empty"&gt;Nenhum evento.&lt;/td&gt;&lt;/tr&gt;&lt;/tbody&gt;&lt;/table&gt;&lt;/div&gt;&lt;/div&gt;
                    &lt;/section&gt;
                    &lt;!-- ICP --&gt;
                    &lt;section class="view" id="v-icp"&gt;&lt;h1&gt;ICP &amp;amp; Score&lt;/h1&gt;&lt;div class="card"&gt;&lt;div id="regrasIcp"&gt;Critérios padrão ativos.&lt;/div&gt;&lt;/div&gt;&lt;/section&gt;
                    &lt;!-- OPORTUNIDADES --&gt;
                    &lt;section class="view" id="v-opp"&gt;&lt;h1&gt;Fila de Oportunidades&lt;/h1&gt;&lt;div class="card"&gt;&lt;div class="tablebox"&gt;&lt;table&gt;&lt;thead&gt;&lt;tr&gt;&lt;th&gt;#&lt;/th&gt;&lt;th&gt;Empresa&lt;/th&gt;&lt;th&gt;Local&lt;/th&gt;&lt;th&gt;Score&lt;/th&gt;&lt;/tr&gt;&lt;/thead&gt;&lt;tbody id="oppRows"&gt;&lt;tr&gt;&lt;td colspan="4" class="empty"&gt;Nenhuma oportunidade.&lt;/td&gt;&lt;/tr&gt;&lt;/tbody&gt;&lt;/table&gt;&lt;/div&gt;&lt;/div&gt;&lt;/section&gt;
                    &lt;!-- BDR --&gt;
                    &lt;section class="view" id="v-bdr"&gt;&lt;h1&gt;Listas para BDR&lt;/h1&gt;&lt;div class="card"&gt;&lt;div class="tablebox"&gt;&lt;table&gt;&lt;thead&gt;&lt;tr&gt;&lt;th&gt;Empresa&lt;/th&gt;&lt;th&gt;Responsável&lt;/th&gt;&lt;th&gt;Contato&lt;/th&gt;&lt;/tr&gt;&lt;/thead&gt;&lt;tbody id="bdrRows"&gt;&lt;tr&gt;&lt;td colspan="3" class="empty"&gt;Nenhuma conta.&lt;/td&gt;&lt;/tr&gt;&lt;/tbody&gt;&lt;/table&gt;&lt;/div&gt;&lt;/div&gt;&lt;/section&gt;
                    &lt;!-- FONTES MONITORADAS --&gt;
                    &lt;section class="view" id="v-sources"&gt;&lt;h1&gt;Fontes Monitoradas&lt;/h1&gt;&lt;div class="card"&gt;&lt;div class="tablebox"&gt;&lt;table&gt;&lt;thead&gt;&lt;tr&gt;&lt;th&gt;Fonte&lt;/th&gt;&lt;th&gt;Status&lt;/th&gt;&lt;th&gt;Última Coleta&lt;/th&gt;&lt;/tr&gt;&lt;/thead&gt;&lt;tbody id="sourceFiles"&gt;&lt;tr&gt;&lt;td colspan="3" class="empty"&gt;Nenhuma fonte cadastrada.&lt;/td&gt;&lt;/tr&gt;&lt;/tbody&gt;&lt;/table&gt;&lt;/div&gt;&lt;/div&gt;&lt;/section&gt;
                    &lt;!-- GOVERNANÇA --&gt;
                    &lt;section class="view" id="v-gov"&gt;&lt;h1&gt;Configurações &amp;amp; Governança&lt;/h1&gt;&lt;div class="card"&gt;&lt;div id="govStatus" class="status"&gt;Sessão local em memória ativa.&lt;/div&gt;&lt;/div&gt;&lt;/section&gt;
                &lt;/main&gt;
            &lt;/div&gt;
        &lt;/div&gt;
        
    



&lt;script id="paim-ver44"&gt;

(function(){
'use strict';
const $=id=&gt;document.getElementById(id), norm=v=&gt;String(v??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
const esc=v=&gt;String(v??'').replace(/[&amp;&lt;&gt;"']/g,c=&gt;({'&amp;':'&amp;amp;','&lt;':'&amp;lt;','&gt;':'&amp;gt;','"':'&amp;quot;',"'":'&amp;#39;'}[c]));
const MemoryStorage=(()=&gt;{const d=new Map();return{getItem:k=&gt;d.has(k)?d.get(k):null,setItem:(k,v)=&gt;d.set(String(k),String(v)),removeItem:k=&gt;d.delete(String(k)),clear:()=&gt;d.clear()}})();
const SafeStorage=(()=&gt;{try{const k='__paim__';localStorage.setItem(k,'1');localStorage.removeItem(k);return localStorage}catch(e){return MemoryStorage}})();
const LOC=__MUNICIPALITIES__;
const SEG=["Operador logístico", "Centro de distribuição", "Transportadora", "Alimentos", "Bebidas", "Eletrodomésticos", "Autopeças", "Metalúrgica", "Moveleira", "Farmacêutica", "Atacadista", "Supermercado", "E-commerce", "Agronegócio", "Fertilizantes", "Papel e celulose", "Plásticos", "Química", "Têxtil", "Construção", "Siderurgia"];
const Hub={rows:[],raw:[],headers:[],filtered:[]};
const Prospect={rows:[],selected:new Set()};
const BDR=[];
window.PAIM_MAPS={HubMapModule:Hub,ProspectMapModule:Prospect};
function option(v){return `&lt;option value="${esc(v)}"&gt;${esc(v)}&lt;/option&gt;`}
function fill(prefix){const country=$(prefix+'Country'),uf=$(prefix+'Uf'),city=$(prefix+'City');if(country){country.innerHTML=option('Brasil');country.value='Brasil'}if(uf){uf.innerHTML='&lt;option value=""&gt;Todos os Estados&lt;/option&gt;'+Object.keys(LOC).map(option).join('')}if(city)city.innerHTML='&lt;option value=""&gt;Selecione uma cidade&lt;/option&gt;'}
function cities(prefix){const u=$(prefix+'Uf'),c=$(prefix+'City');if(!c)return;c.innerHTML='&lt;option value=""&gt;Selecione uma cidade&lt;/option&gt;'+((LOC[u?.value]||[]).map(option).join(''))}
function setup(){['f','m','mb'].forEach(fill);['fSegment','mSegment','mbSegment'].forEach(id=&gt;{if($(id))$(id).innerHTML='&lt;option value=""&gt;Todos os Segmentos&lt;/option&gt;'+SEG.map(option).join('')});window.loadSearchStates=()=&gt;{};window.loadSearchCities=()=&gt;{cities('f');renderHubViews()};window.loadMapStates=()=&gt;{};window.loadMapCities=()=&gt;cities('m');window.loadHbStates=()=&gt;{};window.loadHbCities=()=&gt;{cities('mb');renderHubMap()};}
function g(o,names){for(const n of names){const k=Object.keys(o).find(x=&gt;norm(x)===norm(n));if(k!==undefined&amp;&amp;o[k]!==''&amp;&amp;o[k]!=null)return o[k]}return''}
function num(v){const n=Number(String(v??'').replace(',','.'));return Number.isFinite(n)?n:null}
function normalizeRow(o,i){return{id:'hub-'+i,empresa:g(o,['empresa','razao social','razão social','nome fantasia','cliente','conta','company'])||`Registro ${i+1}`,cnpj:g(o,['cnpj','documento']),uf:String(g(o,['uf','estado','state'])).toUpperCase(),cidade:g(o,['cidade','municipio','município','city']),segmento:g(o,['segmento','setor','ramo','industry','cnae'])||'Não informado',telefone:g(o,['telefone','phone','celular','whatsapp']),email:g(o,['email','e-mail']),website:g(o,['website','site']),latitude:num(g(o,['latitude','lat'])),longitude:num(g(o,['longitude','lng','lon','long'])),score:Number(g(o,['score','pontuacao','pontuação']))||0,source:'Arquivo importado',raw:o}}
function parseCsv(text){const ls=text.replace(/^\uFEFF/,'').split(/\r?\n/).filter(Boolean),sep=(ls[0]?.split(';').length&gt;=ls[0]?.split(',').length?';':',');const parse=l=&gt;{let a=[],v='',q=false;for(let i=0;i&lt;l.length;i++){const c=l[i];if(c==='"'){if(q&amp;&amp;l[i+1]==='"'){v+='"';i++}else q=!q}else if(c===sep&amp;&amp;!q){a.push(v);v=''}else v+=c}a.push(v);return a};const h=parse(ls.shift()||'');return ls.map(l=&gt;{const a=parse(l),o={};h.forEach((k,i)=&gt;o[k]=a[i]||'');return o})}
async function importFiles(){const input=$('files');if(!input?.files.length){alert('Selecione Excel ou CSV.');return}let all=[];for(const f of input.files){if(/\.csv$|\.txt$/i.test(f.name))all.push(...parseCsv(await f.text()));else if(window.XLSX){const wb=XLSX.read(new Uint8Array(await f.arrayBuffer()),{type:'array'});for(const n of wb.SheetNames)all.push(...XLSX.utils.sheet_to_json(wb.Sheets[n],{defval:''}))}else alert('SheetJS não carregou. Use CSV.')}Hub.raw=all;Hub.headers=all.length?Object.keys(all[0]):[];Hub.rows=all.map(normalizeRow);$('importStatus').textContent=`${Hub.rows.length} registros importados. ${Hub.rows.filter(r=&gt;r.latitude!==null&amp;&amp;r.longitude!==null).length} com coordenadas.`;renderAll()}
function filter(prefix,rows){const uf=$(prefix+'Uf')?.value||'',city=$(prefix+'City')?.value||'',seg=$(prefix+'Segment')?.value||'',text=$(prefix+'Text')?.value||'';return rows.filter(r=&gt;(!uf||norm(r.uf)===norm(uf))&amp;&amp;(!city||norm(r.cidade)===norm(city))&amp;&amp;(!seg||norm(r.segmento)===norm(seg))&amp;&amp;(!text||norm(Object.values(r).join(' ')).includes(norm(text))))}
function renderPreview(){if($('dynamicHeaders'))$('dynamicHeaders').innerHTML=Hub.headers.length?Hub.headers.map(h=&gt;`&lt;th&gt;${esc(h)}&lt;/th&gt;`).join(''):'&lt;th&gt;Carregue um arquivo&lt;/th&gt;';if($('dynamicRows'))$('dynamicRows').innerHTML=Hub.raw.length?Hub.raw.slice(0,100).map(r=&gt;'&lt;tr&gt;'+Hub.headers.map(h=&gt;`&lt;td&gt;${esc(r[h])}&lt;/td&gt;`).join('')+'&lt;/tr&gt;').join(''):'&lt;tr&gt;&lt;td class="empty"&gt;Nenhum dado importado.&lt;/td&gt;&lt;/tr&gt;'}
function renderHubViews(){const rows=filter('f',Hub.rows),set=(id,v)=&gt;{if($(id))$(id).textContent=v};set('dTotal',Hub.rows.length);set('dHigh',Hub.rows.filter(r=&gt;r.score&gt;=70).length);set('dFiltered',rows.length);set('dPhone',Hub.rows.filter(r=&gt;r.telefone).length);set('dEmail',Hub.rows.filter(r=&gt;r.email).length);set('activeFilterSummary',`Filtro atual: ${rows.length} registros`);set('searchCount',`${rows.length} contas`);if($('searchRows'))$('searchRows').innerHTML=rows.map(r=&gt;`&lt;tr&gt;&lt;td&gt;${r.score}&lt;/td&gt;&lt;td&gt;&lt;b&gt;${esc(r.empresa)}&lt;/b&gt;&lt;/td&gt;&lt;td&gt;${esc(r.cnpj||'-')}&lt;/td&gt;&lt;td&gt;${esc(r.segmento)}&lt;/td&gt;&lt;td&gt;${esc(r.cidade+'/'+r.uf)}&lt;/td&gt;&lt;td&gt;${esc(r.telefone||r.email||'-')}&lt;/td&gt;&lt;/tr&gt;`).join('')||'&lt;tr&gt;&lt;td colspan="6" class="empty"&gt;Nenhuma empresa.&lt;/td&gt;&lt;/tr&gt;';const c={};Hub.rows.forEach(r=&gt;c[r.segmento]=(c[r.segmento]||0)+1);if($('segments'))$('segments').innerHTML=Object.entries(c).sort((a,b)=&gt;b[1]-a[1]).slice(0,12).map(([k,v])=&gt;`&lt;div style="display:flex;justify-content:space-between;padding:5px"&gt;&lt;span&gt;${esc(k)}&lt;/span&gt;&lt;b&gt;${v}&lt;/b&gt;&lt;/div&gt;`).join('')||'&lt;div class="empty"&gt;Importe uma base.&lt;/div&gt;';if($('profileSelect'))$('profileSelect').innerHTML='&lt;option value=""&gt;Selecione uma empresa&lt;/option&gt;'+Hub.rows.map(r=&gt;`&lt;option value="${r.id}"&gt;${esc(r.empresa)}&lt;/option&gt;`).join('');if($('oppRows'))$('oppRows').innerHTML=rows.filter(r=&gt;r.score&gt;=70).map((r,i)=&gt;`&lt;tr&gt;&lt;td&gt;${i+1}&lt;/td&gt;&lt;td&gt;${esc(r.empresa)}&lt;/td&gt;&lt;td&gt;${esc(r.cidade+'/'+r.uf)}&lt;/td&gt;&lt;td&gt;${r.score}&lt;/td&gt;&lt;/tr&gt;`).join('')||'&lt;tr&gt;&lt;td colspan="4" class="empty"&gt;Nenhuma oportunidade.&lt;/td&gt;&lt;/tr&gt;';renderBDR()}
function bounds(rows){const p=rows.filter(r=&gt;Number.isFinite(+r.latitude)&amp;&amp;Number.isFinite(+r.longitude));if(!p.length)return{a:-34,b:6,c:-74,d:-34};const la=p.map(r=&gt;+r.latitude),lo=p.map(r=&gt;+r.longitude),pa=Math.max(.1,(Math.max(...la)-Math.min(...la))*.15),po=Math.max(.1,(Math.max(...lo)-Math.min(...lo))*.15);return{a:Math.min(...la)-pa,b:Math.max(...la)+pa,c:Math.min(...lo)-po,d:Math.max(...lo)+po}}
function proj(r,z){return{x:5+(+r.longitude-z.c)/Math.max(.001,z.d-z.c)*90,y:5+(z.b-(+r.latitude))/Math.max(.001,z.b-z.a)*90}}
function shell(t,n){return`&lt;div class="native-map-grid"&gt;&lt;/div&gt;&lt;div class="native-label" style="left:12px;top:10px"&gt;${esc(t)}&lt;/div&gt;&lt;div class="native-label" style="right:12px;top:10px"&gt;N ↑&lt;/div&gt;&lt;div class="native-map-badge"&gt;${n} ponto(s)&lt;/div&gt;`}
function renderHubMap(){const rows=filter('mb',Hub.rows);Hub.filtered=rows;const box=$('prospectMapBase');if(!box)return;box.className='native-map';const geo=rows.filter(r=&gt;Number.isFinite(+r.latitude)&amp;&amp;Number.isFinite(+r.longitude)),mode=$('hubMapMode')?.value||'markers',z=bounds(geo);let h=shell('Mapa do Hub · Excel/CSV',geo.length);if(mode==='choropleth'){const c={};rows.forEach(r=&gt;c[r.uf||'NI']=(c[r.uf||'NI']||0)+1);const mx=Math.max(1,...Object.values(c));h+='&lt;div class="uf-grid"&gt;'+Object.entries(c).map(([k,v])=&gt;`&lt;div class="uf-cell" style="background:rgba(6,65,138,${.25+.75*v/mx})"&gt;${esc(k)}&lt;br&gt;${v}&lt;/div&gt;`).join('')+'&lt;/div&gt;'}else geo.forEach(r=&gt;{const p=proj(r,z);if(mode==='heat')h+=`&lt;div class="heat-dot" style="left:${p.x}%;top:${p.y}%;width:85px;height:85px"&gt;&lt;/div&gt;`;else if(mode==='bubbles')h+=`&lt;div class="bubble-dot" style="left:${p.x}%;top:${p.y}%;width:45px;height:45px"&gt;${r.score||''}&lt;/div&gt;`;else h+=`&lt;div class="native-pin internal" style="left:${p.x}%;top:${p.y}%"&gt;&lt;span&gt;&lt;b&gt;${esc(r.empresa)}&lt;/b&gt;&lt;br&gt;${esc(r.segmento)}&lt;br&gt;${esc(r.cidade+'/'+r.uf)}&lt;/span&gt;&lt;/div&gt;`});if(!rows.length)h+='&lt;div class="map-loading"&gt;Carregue um Excel/CSV na Central de Bases.&lt;/div&gt;';else if(!geo.length&amp;&amp;mode!=='choropleth')h+=`&lt;div class="map-loading"&gt;${rows.length} registros sem latitude/longitude.&lt;/div&gt;`;box.innerHTML=h;$('mapBaseCount').textContent=`${rows.length} contas`;$('mapBaseTableBody').innerHTML=rows.map(r=&gt;`&lt;tr&gt;&lt;td&gt;&lt;b&gt;${esc(r.empresa)}&lt;/b&gt;&lt;/td&gt;&lt;td&gt;${esc(r.cnpj||'-')}&lt;/td&gt;&lt;td&gt;${esc(r.segmento)}&lt;/td&gt;&lt;td&gt;${esc(r.cidade+'/'+r.uf)}&lt;/td&gt;&lt;td&gt;${r.score}&lt;/td&gt;&lt;/tr&gt;`).join('')||'&lt;tr&gt;&lt;td colspan="5" class="empty"&gt;Sem dados.&lt;/td&gt;&lt;/tr&gt;'}
function existing(r){const n=norm(r.empresa),site=norm(r.website);return Hub.rows.some(x=&gt;norm(x.empresa)===n||(site&amp;&amp;norm(x.website)===site))}
async function prospect(){const p={uf:$('mUf').value,city:$('mCity').value,segment:$('mSegment').value,km:+$('mRadius').value,limit:+$('mLimit').value,min_score:+$('mScore').value};if(!p.uf||!p.city||!p.segment){$('mStatus').textContent='Selecione Estado, Cidade e Segmento.';return}$('mSearch').disabled=true;$('mStatus').innerHTML='Baixando recorte do Overture Maps e classificando o segmento...&lt;div class="progress"&gt;&lt;i style="width:35%"&gt;&lt;/i&gt;&lt;/div&gt;';try{const r=await fetch('/api/prospect',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)}),text=await r.text();let d;try{d=JSON.parse(text)}catch(_){throw Error(text.slice(0,200)||'Resposta inválida')}if(!r.ok||!d.ok)throw Error(d.error||`HTTP ${r.status}`);Prospect.rows=d.rows.map((x,i)=&gt;({...x,_id:x.id||`prospect-${i}`,situacao:existing(x)?'Já existe na base':'Nova empresa'}));Prospect.selected.clear();renderProspects();$('mStatus').textContent=`${Prospect.rows.length} prospects exibidos. ${d.scanned} places examinados; ${d.matched} compatíveis; ${d.rejected} rejeitados pelo filtro. ${p.city}/${p.uf}. Fonte: Overture Maps.`}catch(e){$('mStatus').textContent='Falha: '+e.message;console.error(e)}finally{$('mSearch').disabled=false}}
function renderProspects(){const a=Prospect.rows,box=$('prospectMap');box.className='native-map';let h=shell('Prospecção externa · Overture Maps',a.length),z=bounds(a);a.forEach(r=&gt;{const p=proj(r,z);h+=`&lt;div class="native-pin" style="left:${p.x}%;top:${p.y}%"&gt;&lt;span&gt;&lt;b&gt;${esc(r.empresa)}&lt;/b&gt;&lt;br&gt;${esc(r.categoria)}&lt;br&gt;${esc(r.telefone||r.website||'')}&lt;/span&gt;&lt;/div&gt;`});if(!a.length)h+='&lt;div class="map-loading"&gt;Selecione os filtros e clique em Prospectar com Overture Maps.&lt;/div&gt;';box.innerHTML=h;$('mapCompanyTableBody').innerHTML=a.length?a.map(r=&gt;`&lt;tr&gt;&lt;td&gt;&lt;input class="prospectCheck" type="checkbox" data-id="${esc(r._id)}"&gt;&lt;/td&gt;&lt;td&gt;&lt;b&gt;${esc(r.empresa)}&lt;/b&gt;&lt;br&gt;&lt;small&gt;${esc(r.endereco||'-')}&lt;/small&gt;&lt;/td&gt;&lt;td&gt;${esc(r.origem)}&lt;br&gt;&lt;span class="${r.situacao==='Nova empresa'?'prospect-new':'prospect-existing'}"&gt;${esc(r.situacao)}&lt;/span&gt;&lt;/td&gt;&lt;td&gt;${esc(r.segmento)}&lt;br&gt;&lt;small&gt;${esc(r.categoria)}&lt;/small&gt;&lt;/td&gt;&lt;td&gt;${esc((r.cidade||'-')+'/'+(r.uf||'-'))}&lt;/td&gt;&lt;td&gt;${esc([r.telefone,r.email,r.website].filter(Boolean).join(' · ')||'-')}&lt;/td&gt;&lt;td&gt;${r.score}&lt;/td&gt;&lt;/tr&gt;`).join(''):'&lt;tr&gt;&lt;td colspan="7" class="empty"&gt;Nenhum prospect externo.&lt;/td&gt;&lt;/tr&gt;';document.querySelectorAll('.prospectCheck').forEach(c=&gt;c.addEventListener('change',()=&gt;c.checked?Prospect.selected.add(c.dataset.id):Prospect.selected.delete(c.dataset.id)))}
function exportRows(rows,name,xlsx){if(!rows.length){alert('Nenhum resultado para exportar.');return}const d=rows.map(r=&gt;({Empresa:r.empresa,Origem:r.origem||r.source,Segmento:r.segmento,Categoria:r.categoria||'',Endereco:r.endereco||'',Cidade:r.cidade,UF:r.uf,CEP:r.cep||'',Telefone:r.telefone||'',Email:r.email||'',Website:r.website||'',Latitude:r.latitude,Longitude:r.longitude,Score:r.score,Situacao:r.situacao||''}));if(xlsx&amp;&amp;window.XLSX){const wb=XLSX.utils.book_new(),ws=XLSX.utils.json_to_sheet(d);XLSX.utils.book_append_sheet(wb,ws,'Resultados');XLSX.writeFile(wb,name);return}const hs=Object.keys(d[0]),csv=[hs.join(';'),...d.map(r=&gt;hs.map(k=&gt;'"'+String(r[k]??'').replace(/"/g,'""')+'"').join(';'))].join('\n'),a=document.createElement('a');a.href=URL.createObjectURL(new Blob(['\ufeff'+csv],{type:'text/csv'}));a.download=name.replace(/\.xlsx$/i,'.csv');a.click();URL.revokeObjectURL(a.href)}
function renderBDR(){if($('bdrRows'))$('bdrRows').innerHTML=BDR.map(r=&gt;`&lt;tr&gt;&lt;td&gt;${esc(r.empresa)}&lt;/td&gt;&lt;td&gt;Pendente&lt;/td&gt;&lt;td&gt;${esc(r.telefone||r.email||r.website||'-')}&lt;/td&gt;&lt;/tr&gt;`).join('')||'&lt;tr&gt;&lt;td colspan="3" class="empty"&gt;Nenhuma conta.&lt;/td&gt;&lt;/tr&gt;'}
function renderAll(){renderPreview();renderHubViews();renderHubMap();renderProspects();$('topStatus').textContent=Hub.rows.length?`Base local: ${Hub.rows.length} registros`:'Motor Overture conectado'}
async function health(){try{const r=await fetch('/api/health'),d=await r.json();if(!d.ok)throw Error();$('topStatus').textContent='Overture Maps conectado';return true}catch(e){$('mStatus').textContent='Servidor Python não detectado. Execute paim_prospect_ver44_definitivo.py.';return false}}
function init(){setup();health();document.querySelector('#nav').addEventListener('click',e=&gt;{const b=e.target.closest('button');if(!b)return;document.querySelectorAll('.nav button').forEach(x=&gt;x.classList.remove('active'));b.classList.add('active');document.querySelectorAll('.view').forEach(x=&gt;x.classList.remove('active'));$('v-'+b.dataset.tab)?.classList.add('active');if(b.dataset.tab==='geomap')renderProspects();if(b.dataset.tab==='geomapbase')renderHubMap()});$('importBtn').addEventListener('click',importFiles);$('mSearch').addEventListener('click',prospect);$('hubMapMode').addEventListener('change',renderHubMap);$('mRadius').addEventListener('input',e=&gt;$('mRadiusLabel').textContent=e.target.value+' km');$('btnExportMapXlsx').addEventListener('click',()=&gt;exportRows(Prospect.rows,'prospects_overture.xlsx',true));$('btnExportMapCSVTop').addEventListener('click',()=&gt;exportRows(Prospect.rows,'prospects_overture.csv',false));$('mExport').addEventListener('click',()=&gt;exportRows(Prospect.rows,'prospects_overture.csv',false));$('mGoogle').addEventListener('click',()=&gt;window.open('https://www.google.com/maps/search/?api=1&amp;query='+encodeURIComponent([$('mSegment').value,$('mCity').value,$('mUf').value,'Brasil'].join(' ')),'_blank','noopener'));$('mAddBdr').addEventListener('click',()=&gt;{const selected=Prospect.rows.filter(r=&gt;Prospect.selected.has(r._id));selected.forEach(r=&gt;{if(!BDR.some(x=&gt;x._id===r._id))BDR.push(r)});renderBDR();alert(`${selected.length} prospect(s) adicionados à Lista BDR.`)});$('selectAllProspects')?.addEventListener('change',e=&gt;{document.querySelectorAll('.prospectCheck').forEach(c=&gt;{c.checked=e.target.checked;c.dispatchEvent(new Event('change'))})});$('profileSelect').addEventListener('change',e=&gt;{const r=Hub.rows.find(x=&gt;x.id===e.target.value);$('profile').innerHTML=r?Object.entries(r).filter(([k])=&gt;k!=='raw').map(([k,v])=&gt;`&lt;div style="padding:7px;border-bottom:1px solid #ddd"&gt;&lt;b&gt;${esc(k)}:&lt;/b&gt; ${esc(v)}&lt;/div&gt;`).join(''):'Selecione uma empresa.'});window.refreshMapBase=renderHubMap;window.triggerHubSearch=renderHubViews;window.clearHubFilters=()=&gt;{['fUf','fCity','fSegment','fText'].forEach(id=&gt;$(id).value='');renderHubViews()};window.clearMapFilters=()=&gt;{['mUf','mCity','mSegment'].forEach(id=&gt;$(id).value='');Prospect.rows=[];renderProspects()};window.exportMapBaseXlsx=()=&gt;exportRows(Hub.filtered,'hub_base_filtrada.xlsx',true);window.exportMapBaseCsv=()=&gt;exportRows(Hub.filtered,'hub_base_filtrada.csv',false);$('clearBtn').addEventListener('click',()=&gt;{Hub.rows=[];Hub.raw=[];renderAll()});$('exportBtn').addEventListener('click',()=&gt;exportRows(Hub.rows,'hub_base_consolidada.csv',false));['fUf','fCity','fSegment','fText'].forEach(id=&gt;$(id)?.addEventListener('input',renderHubViews));['mbUf','mbCity','mbSegment'].forEach(id=&gt;$(id)?.addEventListener('change',renderHubMap));renderAll()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();

&lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;
'''
CITY={}
MUNICIPIOS_URL='https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv'
MUNICIPIOS_CSV=TARGET/'municipios_brasil.csv'
UF_BY_CODE={11:'RO',12:'AC',13:'AM',14:'RR',15:'PA',16:'AP',17:'TO',21:'MA',22:'PI',23:'CE',24:'RN',25:'PB',26:'PE',27:'AL',28:'SE',29:'BA',31:'MG',32:'ES',33:'RJ',35:'SP',41:'PR',42:'SC',43:'RS',50:'MS',51:'MT',52:'GO',53:'DF'}
RULES={
'Operador logístico':{'cat':['logistics','warehouse','freight','shipping','distribution_center','trucking','courier','moving_company'],'name':['logistic','logística','transportes','transportadora','cargas','frete','armazém','armazenagem','distribuição','cargo'],'neg':['automotive_repair','travel_service','tour_operator','gas_station','bus_station','taxi','car_rental','motorcycle']},
'Centro de distribuição':{'cat':['warehouse','distribution_center','storage'],'name':['centro de distribuição','distribution center','armazém','depósito'],'neg':['shop','supermarket']},
'Transportadora':{'cat':['trucking','freight','logistics','transportation_service','shipping'],'name':['transportadora','transportes','cargas','frete'],'neg':['travel_service','tour_operator','taxi','bus_station','automotive_repair']},
'Metalúrgica':{'cat':['metalworking','steel','foundry','manufacturer'],'name':['metalúrgica','siderúrgica','aço','metal'],'neg':['jewelry','scrap']},
'Alimentos':{'cat':['food_manufacturer','food_processing','meat','dairy'],'name':['alimentos','frigorífico','laticínio','massas'],'neg':['restaurant','cafe','bar']},
'Bebidas':{'cat':['beverage_manufacturer','brewery','winery'],'name':['bebidas','cervejaria','vinícola','engarrafadora'],'neg':['bar','liquor_store']},
'Eletrodomésticos':{'cat':['appliance_store','electronics_store','manufacturer'],'name':['eletrodomésticos','eletro'],'neg':['repair']},
'Autopeças':{'cat':['auto_parts_store','automotive_supplier'],'name':['autopeças','auto peças'],'neg':['automotive_repair','car_wash']},
'Moveleira':{'cat':['furniture_manufacturer','furniture_store','carpenter'],'name':['móveis','moveleira','marcenaria'],'neg':[]},
'Farmacêutica':{'cat':['pharmaceutical_company','pharmaceutical_manufacturer'],'name':['farmacêutica','pharma','medicamentos'],'neg':['pharmacy']},
'Atacadista':{'cat':['wholesaler','wholesale_store'],'name':['atacadista','atacado','distribuidora'],'neg':['supermarket']},
'Supermercado':{'cat':['supermarket','hypermarket'],'name':['supermercado','hipermercado'],'neg':[]},
'E-commerce':{'cat':['ecommerce','online_store'],'name':['e-commerce','ecommerce','marketplace'],'neg':[]},
'Agronegócio':{'cat':['agricultural_service','agricultural_supplier'],'name':['agronegócio','agro','sementes'],'neg':['farm']},
'Fertilizantes':{'cat':['fertilizer_supplier','chemical_manufacturer'],'name':['fertilizantes','adubo','agroquímica'],'neg':[]},
'Papel e celulose':{'cat':['paper_mill','pulp_mill','paper_manufacturer'],'name':['papel','celulose'],'neg':['stationery']},
'Plásticos':{'cat':['plastic_manufacturer','polymer_manufacturer'],'name':['plásticos','polímeros'],'neg':[]},
'Química':{'cat':['chemical_manufacturer','chemical_company'],'name':['química','químicos'],'neg':['pharmacy']},
'Têxtil':{'cat':['textile_manufacturer','textile_mill'],'name':['têxtil','tecelagem'],'neg':['clothing_store']},
'Construção':{'cat':['construction_company','building_materials_supplier'],'name':['construtora','construção','engenharia'],'neg':['hardware_store']},
'Siderurgia':{'cat':['steel_manufacturer','iron_and_steel_industry'],'name':['siderúrgica','aço','steel'],'neg':[]}}

def _download_municipalities():
 TARGET.mkdir(parents=True,exist_ok=True)
 if MUNICIPIOS_CSV.exists() and MUNICIPIOS_CSV.stat().st_size>100000:return
 req=urllib.request.Request(MUNICIPIOS_URL,headers={'User-Agent':'PAIM-IA-PROSPECT/1.0'})
 ctx=ssl.create_default_context()
 try:
  with urllib.request.urlopen(req,timeout=60,context=ctx) as r:MUNICIPIOS_CSV.write_bytes(r.read())
 except Exception:
  ctx.check_hostname=False;ctx.verify_mode=ssl.CERT_NONE
  with urllib.request.urlopen(req,timeout=60,context=ctx) as r:MUNICIPIOS_CSV.write_bytes(r.read())

def load_municipalities():
 _download_municipalities();raw=MUNICIPIOS_CSV.read_text(encoding='utf-8-sig');sample=raw[:4096]
 try:dia=csv.Sniffer().sniff(sample,delimiters=',;')
 except csv.Error:dia=csv.excel
 loc={}
 for row in csv.DictReader(io.StringIO(raw),dialect=dia):
  try:
   name=row.get('nome') or row.get('nome_municipio') or row.get('municipio');code=int(row.get('codigo_uf') or 0);uf=UF_BY_CODE.get(code);lat=float(str(row.get('latitude')).replace(',','.'));lon=float(str(row.get('longitude')).replace(',','.'))
  except Exception:continue
  if not name or not uf:continue
  CITY[f'{uf}|{name}']=(lat,lon);loc.setdefault(uf,[]).append(name)
 for uf in loc:loc[uf]=sorted(set(loc[uf]),key=lambda x:x.casefold())
 total=sum(len(v) for v in loc.values())
 if total<5500:raise RuntimeError(f'Base municipal incompleta: {total} municípios carregados')
 return dict(sorted(loc.items()))

def build_index():
 import html
 TARGET.mkdir(parents=True,exist_ok=True);loc=load_municipalities();page=html.unescape(HTML_ESCAPED).replace('__MUNICIPALITIES__',json.dumps(loc,ensure_ascii=False));INDEX.write_text(page,encoding='utf-8')
def bbox(lat,lon,km):
 dlat=km/111.0;dlon=km/(111*max(.2,math.cos(math.radians(lat))));return lon-dlon,lat-dlat,lon+dlon,lat+dlat
def cli():
 import shutil
 x=shutil.which('overturemaps');return [x] if x else [sys.executable,'-m','overturemaps']
def text(v):
 if v is None:return''
 if isinstance(v,(str,int,float)):return str(v)
 if isinstance(v,list):return' '.join(text(x) for x in v)
 if isinstance(v,dict):return' '.join(text(x) for x in v.values())
 return str(v)
def get_place_file(city,uf,km):
 key_city=f'{uf}|{city}'
 if key_city not in CITY:raise ValueError(f'Município não encontrado na base: {city}/{uf}')
 lat,lon=CITY[key_city];w,s,e,n=bbox(lat,lon,km);CACHE.mkdir(parents=True,exist_ok=True);key=re.sub(r'[^a-z0-9]+','_',city.lower())+f'_{km}km.geojsonseq';p=CACHE/key
 if p.exists() and time.time()-p.stat().st_mtime<CACHE_TTL:return p,(w,s,e,n),True
 tmp=p.with_suffix('.tmp');cmd=cli()+['download',f'--bbox={w:.6f},{s:.6f},{e:.6f},{n:.6f}','-f','geojsonseq','--type=place','-o',str(tmp)]
 cp=subprocess.run(cmd,capture_output=True,text=True,timeout=240)
 if cp.returncode!=0:raise RuntimeError((cp.stderr or cp.stdout)[-1800:])
 tmp.replace(p);return p,(w,s,e,n),False
def props(f):
 p=f.get('properties') or {};names=p.get('names') or {};tax=p.get('taxonomy') or {};return p,names.get('primary') or '',str(tax.get('primary') or p.get('basic_category') or '')
def classify(f,segment):
 p,name,cat=props(f);rule=RULES.get(segment,{'cat':[],'name':[segment.lower()],'neg':[]});base=(name+' '+cat+' '+text(p.get('taxonomy'))).lower()
 if any(x in base for x in rule['neg']):return False,0
 cat_hit=sum(1 for x in rule['cat'] if x in cat.lower());name_hit=sum(1 for x in rule['name'] if x in name.lower());score=cat_hit*60+name_hit*45
 return score>=45,score
def normalize(f,segment,uf):
 p,name,cat=props(f);addr=(p.get('addresses') or [{}])[0] or {};co=(f.get('geometry') or {}).get('coordinates') or [None,None];phones=p.get('phones') or [];emails=p.get('emails') or [];sites=p.get('websites') or []
 contact=(20 if phones else 0)+(20 if sites else 0)+(15 if emails else 0)+(15 if addr.get('freeform') else 0)+(15 if name else 0)+15
 return{'id':f.get('id',''),'empresa':name,'origem':'Overture Maps','segmento':segment,'categoria':cat,'endereco':addr.get('freeform') or '','cidade':addr.get('locality') or '','uf':addr.get('region') or uf,'cep':addr.get('postcode') or '','telefone':phones[0] if phones else '','email':emails[0] if emails else '','website':sites[0] if sites else '','longitude':co[0] if len(co)>1 else None,'latitude':co[1] if len(co)>1 else None,'score':min(100,contact)}
def prospect(city,uf,segment,km,limit,min_score):
 key_city=f'{uf}|{city}'
 if key_city not in CITY:raise ValueError(f'Município não configurado: {city}/{uf}')
 path,bb,cached=get_place_file(city,uf,km);rows=[];seen=set();scanned=matched=rejected=parse_errors=0
 with path.open('r',encoding='utf-8-sig') as fh:
  for line in fh:
   line=line.strip().lstrip('\x1e')
   if not line:continue
   try:f=json.loads(line)
   except json.JSONDecodeError:parse_errors+=1;continue
   if f.get('type')!='Feature':continue
   scanned+=1;ok,_=classify(f,segment)
   if not ok:rejected+=1;continue
   matched+=1;r=normalize(f,segment,uf)
   if not r['empresa'] or r['score']<min_score or r['latitude'] is None:continue
   k=(r['empresa'].lower(),round(float(r['latitude']),4),round(float(r['longitude']),4))
   if k in seen:continue
   seen.add(k);rows.append(r)
   if len(rows)>=limit:break
 return{'ok':True,'rows':rows,'scanned':scanned,'matched':matched,'rejected':rejected,'parse_errors':parse_errors,'cached':cached,'bbox':bb}
class H(BaseHTTPRequestHandler):
 def out(self,c,o,t='application/json; charset=utf-8'):
  raw=o if isinstance(o,bytes) else json.dumps(o,ensure_ascii=False).encode();self.send_response(c);self.send_header('Content-Type',t);self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)
 def do_GET(self):
  if self.path in('/','/index.html'):return self.out(200,INDEX.read_bytes(),'text/html; charset=utf-8')
  if self.path=='/api/health':return self.out(200,{'ok':True,'version':'46','source':'Overture Maps'})
  return self.out(404,{'ok':False,'error':'Não encontrado'})
 def do_POST(self):
  if self.path!='/api/prospect':return self.out(404,{'ok':False,'error':'Não encontrado'})
  try:
   n=int(self.headers.get('Content-Length','0'));p=json.loads(self.rfile.read(n) or b'{}');d=prospect(str(p.get('city','')),str(p.get('uf','')),str(p.get('segment','')),max(5,min(100,int(p.get('km',20)))),max(1,min(1500,int(p.get('limit',50)))),max(0,min(100,int(p.get('min_score',0)))));return self.out(200,d)
  except subprocess.TimeoutExpired:return self.out(504,{'ok':False,'error':'Download Overture excedeu 240 segundos'})
  except Exception as e:return self.out(500,{'ok':False,'error':f'{type(e).__name__}: {e}'})
 def log_message(self,fmt,*args):print('[HTTP]',fmt%args)
def main():
 build_index();os.chdir(TARGET)
 try:srv=ThreadingHTTPServer((HOST,PORT),H)
 except OSError as e:print('Porta 8000 ocupada. Feche versões antigas. Detalhe:',e);input('Enter para sair...');return
 url=f'http://{HOST}:{PORT}/index.html';print('='*66);print(' PAIM IA PROSPECT VER46 DEFINITIVO BRASIL · LIMITE 1500 · OVERTURE MAPS');print('='*66);print('Municípios carregados:',len(CITY));print('Pasta:',TARGET);print('Aplicação:',url);print('Não feche esta janela. Ctrl+C encerra.');threading.Timer(1,lambda:webbrowser.open(url)).start()
 try:srv.serve_forever()
 except KeyboardInterrupt:pass
 finally:srv.server_close()
if __name__=='__main__':main()
