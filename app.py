# -*- coding: utf-8 -*-
"""PAIM IA PROSPECT - app.py com CORS explicito para GitHub Pages."""
from __future__ import annotations
import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, make_response, request

import paim_engine as engine

app = Flask(__name__)

# Origem exata do GitHub Pages. Pode ser sobrescrita no Render por CORS_ORIGINS.
ALLOWED_ORIGINS = {
    origin.strip().rstrip('/')
    for origin in os.environ.get(
        'CORS_ORIGINS',
        'https://paimlab-coder.github.io'
    ).split(',')
    if origin.strip()
}

# Render Free usa filesystem efemero. Arquivos temporarios/cache ficam em /tmp.
runtime = Path(tempfile.gettempdir()) / 'paim_prospect_runtime'
runtime.mkdir(parents=True, exist_ok=True)
engine.TARGET = runtime
engine.CACHE = runtime / 'cache_overture'
engine.MUNICIPIOS_CSV = runtime / 'municipios_brasil.csv'
engine.CITY.clear()

_startup_error = None
try:
    engine.load_municipalities()
except Exception as exc:
    _startup_error = f'{type(exc).__name__}: {exc}'


def cors_origin():
    origin = (request.headers.get('Origin') or '').rstrip('/')
    return origin if origin in ALLOWED_ORIGINS else None


@app.after_request
def add_cors_headers(response):
    origin = cors_origin()
    if origin:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Vary'] = 'Origin'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
        response.headers['Access-Control-Max-Age'] = '86400'
    return response


# Responde o preflight sem passar pela rotina pesada de prospeccao.
@app.route('/api/<path:any_path>', methods=['OPTIONS'])
def api_options(any_path):
    origin = cors_origin()
    if not origin:
        return jsonify({'ok': False, 'error': 'Origem CORS não autorizada.'}), 403
    return make_response('', 204)


@app.get('/')
def root():
    return jsonify({
        'ok': True,
        'service': 'PAIM IA PROSPECT API',
        'version': '46-github-get',
        'source': 'Overture Maps',
        'municipalities': len(engine.CITY),
        'startup_error': _startup_error,
        'allowed_origins': sorted(ALLOWED_ORIGINS),
    })


@app.get('/api/health')
def health():
    status = 200 if not _startup_error and len(engine.CITY) >= 5500 else 503
    return jsonify({
        'ok': status == 200,
        'version': '46-github-get',
        'source': 'Overture Maps',
        'municipalities': len(engine.CITY),
        'error': _startup_error,
    }), status


@app.route('/api/prospect', methods=['GET','POST'])
def prospect_api():
    if _startup_error:
        return jsonify({'ok': False, 'error': _startup_error}), 503

    payload = request.args.to_dict() if request.method == 'GET' else (request.get_json(silent=True) or {})
    try:
        city = str(payload.get('city', '')).strip()
        uf = str(payload.get('uf', '')).strip().upper()
        segment = str(payload.get('segment', '')).strip()
        km = max(5, min(100, int(payload.get('km', 20))))
        limit = max(1, min(1500, int(payload.get('limit', 50))))
        min_score = max(0, min(100, int(payload.get('min_score', 0))))

        if not city or not uf or not segment:
            return jsonify({
                'ok': False,
                'error': 'UF, cidade e segmento são obrigatórios.'
            }), 400

        data = engine.prospect(city, uf, segment, km, limit, min_score)
        return jsonify(data)
    except Exception as exc:
        return jsonify({
            'ok': False,
            'error': f'{type(exc).__name__}: {exc}'
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '10000'))
    app.run(host='0.0.0.0', port=port)
