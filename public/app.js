/* =============================================================================
 * KOSIS 통계 대시보드 — 동작 로직
 * -----------------------------------------------------------------------------
 * 이 파일은 화면의 "움직이는 부분"을 담당합니다.
 *   1) data/*.json 에서 통계 시계열을 읽어온다
 *   2) 선택된 지표/지역에 맞는 계열을 골라낸다
 *   3) 요약 타일 · 꺾은선 차트(SVG) · 원자료 표를 그린다
 *
 * 차트는 외부 라이브러리 없이 SVG를 직접 그립니다.
 * (Cloudflare Pages는 정적 호스팅이라 빌드 과정 없이 그대로 동작합니다.)
 * ========================================================================== */

'use strict';

/** 데이터 파일 경로. 새 지표를 추가하려면 이 목록에 파일을 더하면 된다. */
const DATA_URL = 'data/dashboard.json';

/** 화면 요소 참조를 한곳에 모아둔다. */
const el = {
  metric: document.getElementById('metric'),
  groupnav: document.getElementById('groupnav'),
  note: document.getElementById('metric-note'),
  reload: document.getElementById('reload'),
  status: document.getElementById('status'),
  tiles: document.getElementById('tiles'),
  chart: document.getElementById('chart'),
  chartTitle: document.getElementById('chart-title'),
  tbody: document.querySelector('#table tbody'),
  source: document.getElementById('source'),
};

/** 앱이 들고 있는 상태. 로드된 원본 데이터를 그대로 보관한다. */
let dataset = null;

/* ---------------------------------------------------------------------------
 * 숫자 포맷 도우미
 * ------------------------------------------------------------------------- */

/** 정수는 천 단위 쉼표, 소수는 최대 2자리까지 표시한다. */
function fmt(value, unit) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  const decimals = Number.isInteger(value) ? 0 : Math.min(2, decimalsOf(value));
  const text = value.toLocaleString('ko-KR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
  return unit ? `${text} ${unit}` : text;
}

/** 원자료가 소수 몇 자리까지 주어졌는지 센다(최대 2자리까지만 의미 있음). */
function decimalsOf(value) {
  const s = String(value);
  const dot = s.indexOf('.');
  return dot === -1 ? 0 : s.length - dot - 1;
}

/** 전기 대비 증감률(%)을 계산한다. 이전 값이 없거나 0이면 null. */
function changeRate(current, previous) {
  if (previous === null || previous === undefined || previous === 0) return null;
  return ((current - previous) / previous) * 100;
}

/** 증감률을 "+1.2%" 형태의 문자열과 방향 클래스로 바꾼다. */
function deltaParts(rate, polarity) {
  if (rate === null) return { text: '—', cls: 'flat' };
  const sign = rate > 0 ? '+' : '';
  // polarity 'harm' 인 지표만 증가를 경고색으로 칠한다.
  // 강수량·면적처럼 좋고 나쁨이 없는 지표는 중립색으로 둔다.
  const cls = polarity !== 'harm' ? 'flat' : rate > 0.05 ? 'up' : rate < -0.05 ? 'down' : 'flat';
  return { text: `${sign}${rate.toFixed(1)}%`, cls };
}

/* ---------------------------------------------------------------------------
 * 데이터 로드
 * ------------------------------------------------------------------------- */

/** dashboard.json 을 읽어 상태에 보관하고 선택 메뉴를 채운다. */
async function loadData() {
  setStatus('불러오는 중…', true);
  try {
    const res = await fetch(DATA_URL, { cache: 'no-cache' });
    if (!res.ok) throw new Error(`데이터를 불러오지 못했습니다 (HTTP ${res.status})`);
    dataset = await res.json();
    buildGroupNav();
    syncMetricOptions();
    render();
    setStatus(`${dataset.source} · ${dataset.updated}`, false);
  } catch (err) {
    setStatus(err.message, false);
    el.tiles.innerHTML = `<p class="tile">데이터를 표시할 수 없습니다. ${err.message}</p>`;
  }
}

/** <select> 를 주어진 목록으로 다시 채운다. 기존 선택값은 가능하면 유지한다. */
function fillSelect(select, items) {
  const prev = select.value;
  select.innerHTML = '';
  for (const item of items) {
    const opt = document.createElement('option');
    opt.value = item.value;
    opt.textContent = item.label;
    select.appendChild(opt);
  }
  if (items.some((i) => i.value === prev)) select.value = prev;
}

/** 현재 선택된 그룹. 처음에는 첫 그룹을 연다. */
let activeGroup = null;

/** 데이터에 들어 있는 그룹으로 탭 버튼을 만든다. */
function buildGroupNav() {
  const groups = [...new Set(dataset.metrics.map((m) => m.group))];
  activeGroup = groups.includes(activeGroup) ? activeGroup : groups[0];
  el.groupnav.innerHTML = groups
    .map((g) => `<button type="button" data-group="${g}"` +
                `${g === activeGroup ? ' class="on"' : ''}>${g}</button>`)
    .join('');
  el.groupnav.querySelectorAll('button').forEach((btn) => {
    btn.addEventListener('click', () => {
      activeGroup = btn.dataset.group;
      buildGroupNav();
      syncMetricOptions();
      render();
    });
  });
}

/** 선택된 그룹에 속한 지표로 선택 메뉴를 채운다. */
function syncMetricOptions() {
  const items = dataset.metrics
    .filter((m) => m.group === activeGroup)
    .map((m) => ({ value: m.id, label: m.name }));
  fillSelect(el.metric, items);
}

/** 현재 선택된 지표 객체 */
function currentMetric() {
  const inGroup = dataset?.metrics.filter((m) => m.group === activeGroup) ?? [];
  return inGroup.find((m) => m.id === el.metric.value) ?? inGroup[0];
}

/* ---------------------------------------------------------------------------
 * 화면 그리기
 * ------------------------------------------------------------------------- */

/** 타일 · 차트 · 표 · 출처를 한 번에 다시 그린다. */
function render() {
  const metric = currentMetric();
  if (!metric) return;

  el.chartTitle.textContent = `${metric.name} 추이 (${metric.unit})`;
  el.note.textContent = metric.note || '';
  renderTiles(metric);
  renderChart(metric.points, metric.unit, metric.chart);
  renderTable(metric.points, metric.unit, metric.polarity);
  renderSource(metric);
}

/** 최신값 · 전기 대비 · 기간 내 최고/최저를 요약 타일로 보여준다. */
function renderTiles(metric) {
  const pts = metric.points;
  const last = pts[pts.length - 1];
  const prev = pts[pts.length - 2];
  const values = pts.map((p) => p.value);
  const max = pts[values.indexOf(Math.max(...values))];
  const min = pts[values.indexOf(Math.min(...values))];
  const delta = deltaParts(changeRate(last.value, prev?.value), metric.polarity);

  el.tiles.innerHTML = `
    <dl class="tile">
      <dt>최근값 (${last.period})</dt>
      <dd>${fmt(last.value, metric.unit)}
        <span class="delta ${delta.cls}">전기 대비 ${delta.text}</span></dd>
    </dl>
    <dl class="tile">
      <dt>기간 내 최고 (${max.period})</dt>
      <dd>${fmt(max.value, metric.unit)}</dd>
    </dl>
    <dl class="tile">
      <dt>기간 내 최저 (${min.period})</dt>
      <dd>${fmt(min.value, metric.unit)}</dd>
    </dl>
    <dl class="tile">
      <dt>수록 구간</dt>
      <dd>${pts[0].period} – ${last.period}<span class="delta flat">${pts.length}개 시점</span></dd>
    </dl>`;
}

/** 꺾은선 차트를 SVG로 직접 그린다. */
function renderChart(points, unit, kind) {
  const W = 800, H = 360;
  const pad = { top: 20, right: 24, bottom: 44, left: 68 };
  const innerW = W - pad.left - pad.right;
  const innerH = H - pad.top - pad.bottom;

  const values = points.map((p) => p.value);
  // y축 범위에 5% 여백을 줘서 선이 테두리에 붙지 않게 한다.
  const bars = kind === 'bar';
  const rawMin = bars ? Math.min(0, ...values) : Math.min(...values);
  const rawMax = Math.max(...values);
  const span = (rawMax - rawMin) || Math.abs(rawMax) || 1;
  const yMin = bars ? rawMin : rawMin - span * 0.05;
  const yMax = rawMax + span * 0.05;

  const x = (i) => pad.left + (points.length === 1 ? innerW / 2 : (i / (points.length - 1)) * innerW);
  const y = (v) => pad.top + innerH - ((v - yMin) / (yMax - yMin)) * innerH;

  const ticks = 5;
  const gridLines = [];
  const yLabels = [];
  for (let t = 0; t <= ticks; t++) {
    const value = yMin + ((yMax - yMin) * t) / ticks;
    const py = y(value);
    gridLines.push(`<line x1="${pad.left}" y1="${py}" x2="${W - pad.right}" y2="${py}" />`);
    yLabels.push(`<text x="${pad.left - 10}" y="${py + 4}" text-anchor="end">${fmt(round(value))}</text>`);
  }

  // x축 라벨이 겹치지 않도록 일정 간격으로 솎아낸다.
  const step = Math.max(1, Math.ceil(points.length / 8));
  const xLabels = points
    .map((p, i) => (i % step === 0 || i === points.length - 1
      ? `<text x="${x(i)}" y="${H - pad.bottom + 20}" text-anchor="middle">${p.period}</text>`
      : ''))
    .join('');

  if (bars) {
    // 수록 연도가 띄엄띄엄한 계열은 꺾은선으로 이으면 없는 추세를 만들어낸다.
    const slot = innerW / points.length;
    const w = Math.min(46, slot * 0.6);
    const rects = points
      .map((p, i) => {
        const cx = pad.left + slot * (i + 0.5);
        const top = y(p.value);
        const h = Math.max(1, pad.top + innerH - top);
        return `<rect class="series-bar" x="${(cx - w / 2).toFixed(1)}" y="${top.toFixed(1)}" `
             + `width="${w.toFixed(1)}" height="${h.toFixed(1)}" rx="3">`
             + `<title>${p.period}: ${fmt(p.value, unit)}</title></rect>`;
      })
      .join('');
    const barLabels = points
      .map((p, i) => `<text x="${(pad.left + slot * (i + 0.5)).toFixed(1)}" `
                   + `y="${H - pad.bottom + 20}" text-anchor="middle">${p.period}</text>`)
      .join('');
    el.chart.innerHTML = `
      <g class="grid">${gridLines.join('')}</g>
      ${rects}
      <g class="axis">
        <line x1="${pad.left}" y1="${pad.top + innerH}" x2="${W - pad.right}" y2="${pad.top + innerH}" />
        ${yLabels.join('')}
        ${barLabels}
      </g>`;
    return;
  }

  const line = points.map((p, i) => `${i === 0 ? 'M' : 'L'}${x(i).toFixed(1)},${y(p.value).toFixed(1)}`).join(' ');
  const area = `${line} L${x(points.length - 1).toFixed(1)},${(pad.top + innerH).toFixed(1)} `
             + `L${x(0).toFixed(1)},${(pad.top + innerH).toFixed(1)} Z`;
  const dots = points
    .map((p, i) => `<circle class="series-dot" cx="${x(i).toFixed(1)}" cy="${y(p.value).toFixed(1)}" r="3">`
                 + `<title>${p.period}: ${fmt(p.value, unit)}</title></circle>`)
    .join('');

  el.chart.innerHTML = `
    <g class="grid">${gridLines.join('')}</g>
    <path class="series-area" d="${area}" />
    <path class="series-line" d="${line}" />
    ${dots}
    <g class="axis">
      <line x1="${pad.left}" y1="${pad.top + innerH}" x2="${W - pad.right}" y2="${pad.top + innerH}" />
      ${yLabels.join('')}
      ${xLabels}
    </g>`;
}

/** 축 라벨용으로 자릿수를 적당히 줄인다. */
function round(v) {
  const abs = Math.abs(v);
  if (abs >= 1000) return Math.round(v);
  if (abs >= 10) return Math.round(v * 10) / 10;
  return Math.round(v * 100) / 100;
}

/** 원자료를 표로 보여준다. 최근 시점이 위로 오도록 뒤집는다. */
function renderTable(points, unit, polarity) {
  el.tbody.innerHTML = points
    .map((p, i) => ({ p, prev: points[i - 1] }))
    .reverse()
    .map(({ p, prev }) => {
      const d = deltaParts(changeRate(p.value, prev?.value), polarity);
      return `<tr><td>${p.period}</td><td>${fmt(p.value, unit)}</td>`
           + `<td class="delta ${d.cls}">${d.text}</td></tr>`;
    })
    .join('');
}

/** 출처와 KOSIS 바로가기 링크를 표시한다. */
function renderSource(metric) {
  const link = metric.url
    ? ` <a href="${metric.url}" rel="noopener" target="_blank">KOSIS 바로가기</a>`
    : '';
  el.source.innerHTML = `<p>출처: 국가통계포털 KOSIS, 「${metric.survey}」, 「${metric.table}」${link}</p>`;
}

/** 상태 메시지 표시 및 버튼 잠금 */
function setStatus(text, busy) {
  el.status.textContent = text;
  el.reload.disabled = Boolean(busy);
}

/* ---------------------------------------------------------------------------
 * 이벤트 연결
 * ------------------------------------------------------------------------- */

el.metric.addEventListener('change', render);
el.reload.addEventListener('click', loadData);

loadData();
