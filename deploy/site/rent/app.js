/* =============================================================================
 * 서울 전세가 조회 — 동작 로직
 * -----------------------------------------------------------------------------
 * 자치구 → 법정동 → 주택유형을 고르면 평균 전세가와 거래 건수를 보여준다.
 *
 * 데이터는 전처리된 jeonse.json(96KB) 하나뿐이다. API를 호출하지 않으므로
 * 인증키가 필요 없고, 브라우저에 키가 노출될 일도 없다.
 * (강의자료 과제 2 옵션 1)
 * ========================================================================== */

'use strict';

const DATA_URL = 'data/jeonse.json';

/** 거래가 이보다 적으면 평균을 시세로 보기 어렵다. 화면에 경고를 띄운다. */
const THIN_TRADE = 10;

const el = {
  gu: document.getElementById('gu'),
  dong: document.getElementById('dong'),
  usage: document.getElementById('usage'),
  result: document.getElementById('result'),
  compare: document.getElementById('compare'),
  compareTitle: document.getElementById('compare-title'),
  rank: document.getElementById('rank'),
  rankTitle: document.getElementById('rank-title'),
};

let rows = [];

/** 만원 단위를 읽기 쉽게. 1억 이상은 "N억 M,MMM만원"으로 쪼갠다. */
function won(man) {
  if (man >= 10000) {
    const eok = Math.floor(man / 10000);
    const rest = man % 10000;
    return rest ? `${eok}억 ${rest.toLocaleString('ko-KR')}만원` : `${eok}억원`;
  }
  return `${man.toLocaleString('ko-KR')}만원`;
}

function fillSelect(select, values, keepIfPossible = true) {
  const prev = select.value;
  select.innerHTML = values
    .map((v) => `<option value="${v}">${v}</option>`)
    .join('');
  if (keepIfPossible && values.includes(prev)) select.value = prev;
}

const uniq = (arr) => [...new Set(arr)].sort((a, b) => a.localeCompare(b, 'ko'));

/** 자치구가 바뀌면 그 구의 동만, 동이 바뀌면 그 동에 있는 유형만 남긴다. */
function syncDong() {
  fillSelect(el.dong, uniq(rows.filter((r) => r.gu === el.gu.value).map((r) => r.dong)));
}

function syncUsage() {
  const inDong = rows.filter((r) => r.gu === el.gu.value && r.dong === el.dong.value);
  fillSelect(el.usage, uniq(inDong.map((r) => r.usage)));
}

function current() {
  return rows.find((r) => r.gu === el.gu.value
                       && r.dong === el.dong.value
                       && r.usage === el.usage.value);
}

function renderResult(row) {
  if (!row) {
    el.result.innerHTML = '<p class="empty">해당 조건의 전세 거래가 없습니다.</p>';
    return;
  }
  const thin = row.n < THIN_TRADE
    ? `<p class="warn">거래가 ${row.n}건뿐입니다. 이 평균은 동네 시세라기보다
       그 몇 건의 값에 가깝습니다.</p>`
    : '';
  el.result.innerHTML = `
    <p class="where">${row.gu} ${row.dong} · ${row.usage}</p>
    <p class="price">${won(row.avg)}</p>
    <p class="meta">전세 거래 ${row.n.toLocaleString('ko-KR')}건의 평균</p>
    ${thin}`;
}

/** 막대 목록을 그린다. 가장 큰 값을 100%로 잡는다. */
function bars(container, items, activeKey) {
  if (!items.length) {
    container.innerHTML = '<p class="empty">견줄 자료가 없습니다.</p>';
    return;
  }
  const max = Math.max(...items.map((i) => i.avg));
  container.innerHTML = items
    .map((i) => `
      <div class="bar-row ${i.key === activeKey ? 'on' : ''}">
        <span class="name">${i.label}</span>
        <span class="bar-track"><span class="bar-fill"
              style="width:${(i.avg / max * 100).toFixed(1)}%"></span></span>
        <span class="val">${i.avg.toLocaleString('ko-KR')}</span>
      </div>`)
    .join('');
}

function renderCompare(row) {
  if (!row) return;
  const items = rows
    .filter((r) => r.gu === row.gu && r.dong === row.dong)
    .sort((a, b) => b.avg - a.avg)
    .map((r) => ({ key: r.usage, label: r.usage, avg: r.avg }));
  el.compareTitle.textContent = `${row.dong}의 주택유형별 평균 전세가 (만원)`;
  bars(el.compare, items, row.usage);
}

function renderRank(row) {
  if (!row) return;
  // 거래가 얇은 동을 섞으면 순위가 뒤틀린다. 기준 미만은 뺀다.
  const items = rows
    .filter((r) => r.gu === row.gu && r.usage === row.usage && r.n >= THIN_TRADE)
    .sort((a, b) => b.avg - a.avg)
    .map((r) => ({ key: r.dong, label: r.dong, avg: r.avg }));

  el.rankTitle.textContent = `${row.gu} · ${row.usage} 동별 평균 전세가 (만원)`;

  const at = items.findIndex((i) => i.key === row.dong);
  const note = at >= 0
    ? `${row.dong}은 ${items.length}개 동 중 ${at + 1}번째입니다.`
    : `${row.dong}은 거래 ${THIN_TRADE}건 미만이라 순위에서 빠졌습니다.`;
  el.rank.innerHTML = `<p class="hint">${note}</p>`;

  const box = document.createElement('div');
  el.rank.appendChild(box);
  bars(box, items, row.dong);
}

function render() {
  const row = current();
  renderResult(row);
  renderCompare(row);
  renderRank(row);
}

async function init() {
  try {
    const res = await fetch(DATA_URL);
    rows = await res.json();

    fillSelect(el.gu, uniq(rows.map((r) => r.gu)), false);
    syncDong();
    syncUsage();
    render();
  } catch (err) {
    el.result.innerHTML = `<p class="empty">데이터를 불러오지 못했습니다. ${err.message}</p>`;
  }
}

el.gu.addEventListener('change', () => { syncDong(); syncUsage(); render(); });
el.dong.addEventListener('change', () => { syncUsage(); render(); });
el.usage.addEventListener('change', render);

init();
