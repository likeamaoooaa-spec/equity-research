#!/usr/bin/env python3
"""
extract_financials.py
Parse inline XBRL SEC filings (10-K, 10-Q) and extract key financial metrics.
Outputs financial-data.js for the index.html dashboard.
"""

import json
import os
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup


# ── Key XBRL tags we want to extract ──────────────────────────────
INCOME_STMT_TAGS = {
    'RevenueFromContractWithCustomerExcludingAssessedTax': 'Revenue',
    'Revenues': 'Revenue',
    'SalesRevenueNet': 'Revenue',
    'CostOfRevenue': 'CostOfRevenue',
    'CostOfGoodsAndServicesSold': 'CostOfRevenue',
    'GrossProfit': 'GrossProfit',
    'OperatingExpenses': 'OperatingExpenses',
    'OperatingIncomeLoss': 'OperatingIncome',
    'NetIncomeLoss': 'NetIncome',
    'EarningsPerShareBasic': 'EPS_Basic',
    'EarningsPerShareDiluted': 'EPS_Diluted',
    'ResearchAndDevelopmentExpense': 'R&D',
    'SellingGeneralAndAdministrativeExpense': 'SG&A',
    'SellingAndMarketingExpense': 'S&M',
    'GeneralAndAdministrativeExpense': 'G&A',
}

BALANCE_SHEET_TAGS = {
    'Assets': 'TotalAssets',
    'AssetsCurrent': 'CurrentAssets',
    'Liabilities': 'TotalLiabilities',
    'LiabilitiesCurrent': 'CurrentLiabilities',
    'StockholdersEquity': 'StockholdersEquity',
    'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest': 'StockholdersEquity',
    'CashAndCashEquivalentsAtCarryingValue': 'Cash',
    'CashCashEquivalentsAndShortTermInvestments': 'CashAndShortTermInvestments',
    'AccountsReceivableNetCurrent': 'AccountsReceivable',
    'PropertyPlantAndEquipmentNet': 'PP&E',
    'Goodwill': 'Goodwill',
    'LongTermDebt': 'LongTermDebt',
    'LongTermDebtNoncurrent': 'LongTermDebt',
    'ConvertibleNotesPayable': 'ConvertibleDebt',
}

CASHFLOW_TAGS = {
    'NetCashProvidedByUsedInOperatingActivities': 'CFO',
    'NetCashProvidedByUsedInInvestingActivities': 'CFI',
    'NetCashProvidedByUsedInFinancingActivities': 'CFF',
    'DepreciationDepletionAndAmortization': 'D&A',
    'ShareBasedCompensation': 'SBC',
    'PaymentsToAcquirePropertyPlantAndEquipment': 'CapEx',
    'CapitalExpendituresIncurredButNotYetPaid': 'CapEx',
}

ALL_TAGS = {}
ALL_TAGS.update(INCOME_STMT_TAGS)
ALL_TAGS.update(BALANCE_SHEET_TAGS)
ALL_TAGS.update(CASHFLOW_TAGS)


def parse_xbrl_file(filepath: str) -> dict:
    """Parse a single inline XBRL HTML file and extract financial data."""
    with open(filepath, 'r', encoding='ascii', errors='replace') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # ── 1. Build context map: context_id -> {start, end, instant, has_segment} ──
    contexts = {}
    for ctx in soup.find_all('xbrli:context'):
        ctx_id = ctx.get('id', '')
        period = ctx.find('xbrli:period')
        segment = ctx.find('xbrli:segment')

        if not period:
            continue

        info = {'has_segment': segment is not None}

        start = period.find('xbrli:startdate')
        end = period.find('xbrli:enddate')
        instant = period.find('xbrli:instant')

        if start and end:
            info['start'] = start.text.strip()
            info['end'] = end.text.strip()
            info['type'] = 'duration'
        elif instant:
            info['instant'] = instant.text.strip()
            info['type'] = 'instant'

        contexts[ctx_id] = info

    # ── 2. Extract ix:nonfraction values ──
    raw_data = []
    for tag in soup.find_all('ix:nonfraction'):
        name = tag.get('name', '')
        short_name = name.split(':')[-1] if ':' in name else name

        if short_name not in ALL_TAGS:
            continue

        ctx_id = tag.get('contextref', '')
        ctx_info = contexts.get(ctx_id, {})

        # Skip segment-specific values (e.g., by stock class, by equity component)
        if ctx_info.get('has_segment', True):
            continue

        # Parse the numeric value
        text_val = tag.get_text(strip=True).replace(',', '').replace('$', '')
        if text_val in ('—', '–', '-', ''):
            continue

        try:
            value = float(text_val)
        except ValueError:
            continue

        # Apply scale factor
        scale = int(tag.get('scale', '0'))
        value = value * (10 ** scale)

        # Apply sign
        if tag.get('sign', '') == '-':
            value = -value

        metric_name = ALL_TAGS[short_name]

        raw_data.append({
            'metric': metric_name,
            'value': value,
            'context': ctx_info,
            'unit': tag.get('unitref', ''),
        })

    return raw_data


def determine_filing_period(filepath: str) -> dict:
    """Determine the filing type and period from the filename."""
    basename = os.path.basename(filepath)

    # PLTR format: 10-K_FY2025_2026-02-17.html or 10-Q_2025_03_31_2025-05-06.html
    m_10k = re.match(r'10-K_FY(\d{4})_', basename)
    if m_10k:
        fy = int(m_10k.group(1))
        return {'type': '10-K', 'fiscal_year': fy, 'period_end': f'{fy}-12-31', 'label': f'FY{fy}'}

    m_10q = re.match(r'10-Q_(\d{4})_(\d{2})_(\d{2})_', basename)
    if m_10q:
        y, m, d = m_10q.group(1), m_10q.group(2), m_10q.group(3)
        quarter_map = {'03': 'Q1', '06': 'Q2', '09': 'Q3'}
        q = quarter_map.get(m, f'Q?({m})')
        return {'type': '10-Q', 'period_end': f'{y}-{m}-{d}', 'label': f'{y}{q}'}

    # RKLB format: 2026-02-26_10-K_000181999426000013.html or 2026-05-07_10-Q_000181999426000028.html
    m_rklb = re.match(r'(\d{4}-\d{2}-\d{2})_(10-[KQ])_', basename)
    if m_rklb:
        filing_date = m_rklb.group(1)
        filing_type = m_rklb.group(2)
        return {'type': filing_type, 'filing_date': filing_date, 'label': filing_date}

    return {'type': 'unknown', 'label': basename}


def resolve_period_for_data(raw_data: list, filing_info: dict) -> dict:
    """
    From raw_data extracted from one filing, produce a clean dict of metrics
    keyed by period (e.g., 'FY2025', '2024Q3', etc.).
    """
    periods = {}

    for item in raw_data:
        ctx = item['context']
        metric = item['metric']
        value = item['value']

        # Determine the period label
        if ctx.get('type') == 'duration':
            start = ctx['start']
            end = ctx['end']
            start_y = int(start[:4])
            start_m = int(start[5:7])
            end_y = int(end[:4])
            end_m = int(end[5:7])
            end_d = int(end[8:10])

            # Full year (approx 12 months)
            duration_months = (end_y - start_y) * 12 + (end_m - start_m)
            if duration_months >= 10:  # ~annual
                period_key = f'FY{end_y}'
            elif duration_months >= 7:  # 9-month YTD (not a clean quarter)
                quarter = 3
                period_key = f'{end_y}Q{quarter}_YTD'
            elif duration_months >= 4:  # 6-month YTD
                quarter = 2
                period_key = f'{end_y}Q{quarter}_YTD'
            else:
                # Quarterly
                quarter_map = {3: 1, 6: 2, 9: 3, 12: 4}
                quarter = quarter_map.get(end_m, (end_m + 2) // 3)
                period_key = f'{end_y}Q{quarter}'
        elif ctx.get('type') == 'instant':
            inst = ctx['instant']
            inst_y = int(inst[:4])
            inst_m = int(inst[5:7])
            # Balance sheet instant dates
            quarter_map_inst = {3: 1, 6: 2, 9: 3, 12: 4}
            q = quarter_map_inst.get(inst_m, (inst_m + 2) // 3)
            if inst_m == 12:
                period_key = f'FY{inst_y}'
            else:
                period_key = f'{inst_y}Q{q}'
        else:
            continue

        if period_key not in periods:
            periods[period_key] = {'period': period_key}

        # Only keep the first value for each metric per period (avoid duplicates)
        if metric not in periods[period_key]:
            periods[period_key][metric] = value

    return periods


def collect_ticker_data(ticker: str, data_dir: str) -> list:
    """Collect all financial data for a ticker from its filing directory."""
    all_periods = {}

    # Gather all HTML files
    html_files = []
    for root, dirs, files in os.walk(data_dir):
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    html_files.sort()
    print(f'  Found {len(html_files)} HTML filings for {ticker}')

    for filepath in html_files:
        basename = os.path.basename(filepath)
        filing_info = determine_filing_period(filepath)
        print(f'    Processing: {basename} ({filing_info["type"]})')

        try:
            raw_data = parse_xbrl_file(filepath)
            periods = resolve_period_for_data(raw_data, filing_info)

            for period_key, metrics in periods.items():
                if period_key not in all_periods:
                    all_periods[period_key] = {'period': period_key}
                # Merge, keeping first (or latest filing if duplicate)
                for k, v in metrics.items():
                    if k != 'period':
                        all_periods[period_key][k] = v
        except Exception as e:
            print(f'    ERROR: {e}')

    # Sort by period
    result = sorted(all_periods.values(), key=lambda x: x['period'])
    return result


def period_sort_key(period: str) -> tuple:
    """Generate a sortable key from period string like 'FY2025', '2024Q1', etc."""
    m = re.match(r'FY(\d{4})', period)
    if m:
        return (int(m.group(1)), 4)  # FY = Q4

    m = re.match(r'(\d{4})Q(\d)', period)
    if m:
        return (int(m.group(1)), int(m.group(2)))

    m = re.match(r'(\d{4})Q(\d)_YTD', period)
    if m:
        return (int(m.group(1)), int(m.group(2)) + 0.5)

    return (0, 0)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    research_dir = os.path.join(base_dir, 'research')

    all_data = {}

    # Process each ticker that has a data/ directory
    for ticker in sorted(os.listdir(research_dir)):
        ticker_dir = os.path.join(research_dir, ticker)
        data_dir = os.path.join(ticker_dir, 'data')

        if not os.path.isdir(data_dir):
            continue

        print(f'\nProcessing {ticker}...')
        periods = collect_ticker_data(ticker, data_dir)

        # Filter: keep only clean quarterly and annual periods (skip YTD)
        clean_periods = [p for p in periods if '_YTD' not in p['period']]

        # De-duplicate: for FY periods, if we have both annual and Q4 data, prefer annual
        seen = {}
        for p in clean_periods:
            key = p['period']
            if key in seen:
                # Merge - more data is better
                seen[key].update({k: v for k, v in p.items() if k not in seen[key]})
            else:
                seen[key] = p

        final_periods = sorted(seen.values(), key=lambda x: period_sort_key(x['period']))

        # Convert values: actual dollars -> millions for readability
        for p in final_periods:
            for k, v in list(p.items()):
                if k == 'period' or k in ('EPS_Basic', 'EPS_Diluted'):
                    continue
                if isinstance(v, (int, float)):
                    p[k] = round(v / 1_000_000, 2)  # actual dollars -> millions

        all_data[ticker] = final_periods
        print(f'  => {len(final_periods)} periods extracted')

    # ── Write output ──
    output_path = os.path.join(base_dir, 'financial-data.js')
    js_content = f'// Auto-generated by extract_financials.py\n'
    js_content += f'// Last updated: {__import__("datetime").datetime.now().isoformat()}\n'
    js_content += f'const FINANCIAL_DATA = {json.dumps(all_data, indent=2, ensure_ascii=False)};\n'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f'\n✅ Written to {output_path}')

    # Summary
    for ticker, periods in all_data.items():
        print(f'\n{ticker}:')
        for p in periods:
            rev = p.get('Revenue', '—')
            ni = p.get('NetIncome', '—')
            print(f'  {p["period"]}: Revenue={rev}M, NetIncome={ni}M')


if __name__ == '__main__':
    main()
