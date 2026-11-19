"""Read-only final-figure audit using this package's bundled local auditors."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys


def run_auditor(script: Path, args: list[str], output: Path) -> dict:
    if not script.is_file():
        return {'status': 'NOT_AUDITABLE', 'reason': f'Missing auditor: {script}'}
    try:
        proc = subprocess.run([sys.executable, '-X', 'utf8', str(script), *args],
                              capture_output=True, text=True, encoding='utf-8', timeout=60)
    except subprocess.TimeoutExpired:
        return {'status': 'NOT_AUDITABLE', 'reason': f'Auditor timed out: {script.name}'}
    output.with_suffix('.stdout.txt').write_text(proc.stdout, encoding='utf-8')
    output.with_suffix('.stderr.txt').write_text(proc.stderr, encoding='utf-8')
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {'status': 'NOT_AUDITABLE', 'exit_code': proc.returncode,
                'reason': 'Auditor did not produce JSON; see raw stdout/stderr.'}
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    if payload.get('verdict') == 'NOT APPLICABLE' and proc.returncode == 0:
        status = 'NOT_APPLICABLE'
    elif proc.returncode == 2 or payload.get('auditable') is False:
        status = 'NOT_AUDITABLE'
    elif proc.returncode != 0:
        status = 'FIX_REQUIRED'
    elif payload.get('summary', {}).get('warn', 0) or payload.get('warnings'):
        status = 'REVIEW_REQUIRED'
    else:
        status = 'PASS'
    return {'status': status, 'exit_code': proc.returncode, 'raw_report': str(output)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path, help='Final single-figure PDF; never modified')
    parser.add_argument('--panels', type=int, required=True, help='Total number of figure panels')
    parser.add_argument('--layout', type=Path, help='Final measured manifest or alignment report containing layout')
    parser.add_argument('--out', type=Path, required=True, help='New directory for this audit; refuses overwrite')
    parser.add_argument('--min-pt', type=float, default=5.0, help='Task-specific PDF glyph floor in pt')
    args = parser.parse_args()
    if args.panels < 1 or not math.isfinite(args.min_pt) or args.min_pt <= 0:
        parser.error('--panels and --min-pt must be positive')
    args.out.mkdir(parents=True, exist_ok=False)
    pdf = args.pdf.resolve()
    checks = {}
    geometry = None
    try:
        import fitz
        with fitz.open(pdf) as document:
            if len(document) != 1:
                checks['pdf_geometry'] = {'status': 'FIX_REQUIRED', 'reason': 'Expected one page per figure.',
                                          'page_count': len(document)}
            else:
                geometry = {'width_pt': document[0].rect.width, 'height_pt': document[0].rect.height}
                checks['pdf_geometry'] = {'status': 'PASS', **geometry}
    except (ImportError, OSError, RuntimeError, ValueError) as exc:
        checks['pdf_geometry'] = {'status': 'NOT_AUDITABLE', 'reason': str(exc)}

    scripts = Path(__file__).resolve().parent
    checks['pdf_text'] = run_auditor(scripts / 'audit_pdf_text.py',
        [str(pdf), '--min-pt', str(args.min_pt), '--json'], args.out / 'pdf_text.json')
    checks['collisions'] = run_auditor(scripts / 'audit_figure_collisions.py',
        [str(pdf), '--json', '--overlay-pdf', str(args.out / 'collisions_overlay.pdf')],
        args.out / 'collisions.json')

    if args.layout is None:
        checks['alignment'] = {'status': 'NOT_AUDITABLE' if args.panels > 1 else 'NOT_APPLICABLE',
                               'reason': 'No measured layout supplied.' if args.panels > 1 else 'Single panel.'}
    else:
        try:
            payload = json.loads(args.layout.read_text(encoding='utf-8-sig'))
            layout = payload.get('layout', payload)
            issues = []
            if len(layout['panels']) != args.panels:
                issues.append('Declared panel count differs from measured layout.')
            if geometry:
                for name in ['width_pt', 'height_pt']:
                    measured = float(layout['figure'][name])
                    if not math.isfinite(measured) or abs(measured - geometry[name]) > 0.5:
                        issues.append(f'PDF and measured layout differ in {name}.')
            checks['layout_binding'] = {'status': 'FIX_REQUIRED' if issues else 'PASS', 'issues': issues,
                                        'source': str(args.layout.resolve())}
            manifest = args.out / 'measured_layout.json'
            manifest.write_text(json.dumps(layout, ensure_ascii=False, indent=2), encoding='utf-8')
            checks['alignment'] = run_auditor(scripts / 'audit_panel_alignment.py',
                [str(manifest), '--json', '--overlay-svg', str(args.out / 'alignment_overlay.svg')],
                args.out / 'alignment.json')
        except (OSError, ValueError, KeyError, TypeError) as exc:
            checks['alignment'] = {'status': 'NOT_AUDITABLE', 'reason': str(exc)}

    statuses = {check['status'] for check in checks.values()}
    status = next((s for s in ['FIX_REQUIRED', 'NOT_AUDITABLE', 'REVIEW_REQUIRED'] if s in statuses), 'PASS')
    result = {'pdf': str(pdf), 'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest() if pdf.is_file() else None,
              'status': status, 'checks': checks, 'visual_review_required': True,
              'scientific_validity': 'Not established by this layout audit.',
              'scope': 'Single final PDF and declared final geometry; no source/data changes.'}
    destination = args.out / 'summary.json'
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': status, 'summary': str(destination.resolve()),
                      'visual_review_required': True}, ensure_ascii=False))
    return {'PASS': 0, 'REVIEW_REQUIRED': 0, 'FIX_REQUIRED': 1, 'NOT_AUDITABLE': 2}[status]


if __name__ == '__main__':
    raise SystemExit(main())
