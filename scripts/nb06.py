import sys; sys.path.insert(0, "scripts")
from build_notebooks import build

c = []
c.append(("md", """# 06 : Matplotlib

강의자료: `docs/course/06_Matplotlib.md`

목적에 맞는 그래프를 고르는 연습.

| 목적 | 그래프 |
| --- | --- |
| 분포 | Histogram, Density |
| 관계 | Scatter |
| 비교 | Bar, Box |
| 추세 | Line |

## 데이터

URL에서 바로 읽는다. 내려받아 둘 필요가 없다.

- `drinks.csv` — 193개국 주류 소비량
- `ufo.csv` — UFO 목격 기록 80,543건

출처: `https://github.com/justmarkham/DAT8`

저장 위치는 `outputs/figures/`."""))

c.append(("code", '''import matplotlib.pyplot as plt
import setuptools                # Python 3.12에서 distutils가 빠져 필요한 shim
import koreanize_matplotlib      # 한글 폰트 등록 — import만 하면 적용된다
import numpy as np
import pandas as pd
from pathlib import Path

FIG = Path("outputs/figures")
FIG.mkdir(parents=True, exist_ok=True)

plt.style.use("default")
print("준비 완료")'''))

c.append(("md", "## 1. 데이터 불러오기"))
c.append(("code", '''url = "https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv"
drink_cols = ["country", "beer", "spirit", "wine", "pure", "continent"]

# na_filter=False — 대륙 'NA'(북미)가 결측치로 읽히는 것을 막는다
drinks = pd.read_csv(url, header=0, names=drink_cols, na_filter=False)

print(drinks.shape)
print(drinks["continent"].value_counts())
drinks.head()'''))

c.append(("md", "## 2. Histogram — 분포"))
c.append(("code", '''fig, ax = plt.subplots(figsize=(8, 4))
drinks["beer"].plot(kind="hist", bins=10, ax=ax, edgecolor="white")
ax.set_title("맥주 소비량 분포 (bins=10)")
ax.set_xlabel("1인당 연간 맥주 소비량 (잔)")
ax.set_ylabel("국가 수")
fig.tight_layout()
fig.savefig(FIG / "1_1.png", dpi=120)
plt.show()'''))

c.append(("code", '''# bins를 늘리면 더 잘게 쪼개 보인다. 너무 잘게 쪼개면 잡음까지 보인다.
fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
for ax, b in zip(axes, [10, 20, 40]):
    drinks["beer"].plot(kind="hist", bins=b, ax=ax, edgecolor="white")
    ax.set_title(f"bins={b}")
    ax.set_xlabel("맥주 소비량")
fig.suptitle("bins에 따라 분포가 다르게 보인다")
fig.tight_layout()
fig.savefig(FIG / "1_3.png", dpi=120)
plt.show()'''))

c.append(("code", '''# 대륙별로 나눠 그린다. sharex/sharey로 축을 맞춰야 서로 비교가 된다.
drinks.hist(column="beer", by="continent", figsize=(11, 6),
            layout=(2, 3), sharex=True, sharey=True, bins=15, edgecolor="white")
plt.suptitle("대륙별 맥주 소비량 분포 (축 통일)")
plt.tight_layout()
plt.savefig(FIG / "1_4.png", dpi=120)
plt.show()'''))

c.append(("md", "## 3. Scatter — 관계"))
c.append(("code", '''fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(drinks["beer"], drinks["wine"], alpha=0.5)
ax.set_xlabel("맥주")
ax.set_ylabel("와인")
ax.set_title("맥주와 와인 소비량의 관계")
fig.tight_layout()
fig.savefig(FIG / "2_1.png", dpi=120)
plt.show()

print("상관계수:", round(drinks["beer"].corr(drinks["wine"]), 3))'''))

c.append(("code", '''# 세 번째 변수를 색으로 얹는다
fig, ax = plt.subplots(figsize=(8, 5))
sc = ax.scatter(drinks["beer"], drinks["wine"],
                c=drinks["spirit"], s=drinks["pure"] * 12 + 10,
                cmap="viridis", alpha=0.7, edgecolor="white", linewidth=0.5)
ax.set_xlabel("맥주")
ax.set_ylabel("와인")
ax.set_title("색=증류주, 크기=순알코올")
fig.colorbar(sc, ax=ax, label="증류주 소비량")
fig.tight_layout()
fig.savefig(FIG / "2_3.png", dpi=120)
plt.show()'''))

c.append(("md", "## 4. Bar — 비교"))
c.append(("code", '''fig, axes = plt.subplots(1, 2, figsize=(12, 4))

drinks["continent"].value_counts().plot(kind="bar", ax=axes[0], color="#1f6feb")
axes[0].set_title("대륙별 국가 수")
axes[0].tick_params(axis="x", rotation=0)

drinks.groupby("continent")[["beer", "spirit", "wine"]].mean().plot(
    kind="bar", ax=axes[1])
axes[1].set_title("대륙별 평균 소비량")
axes[1].tick_params(axis="x", rotation=0)

fig.tight_layout()
fig.savefig(FIG / "3_2.png", dpi=120)
plt.show()'''))

c.append(("code", '''# 누적 막대 — 전체 크기와 구성비를 같이 본다
fig, ax = plt.subplots(figsize=(8, 4))
drinks.groupby("continent")[["beer", "spirit", "wine"]].mean().plot(
    kind="bar", stacked=True, ax=ax)
ax.set_title("대륙별 평균 소비량 (누적)")
ax.tick_params(axis="x", rotation=0)
fig.tight_layout()
fig.savefig(FIG / "3_3.png", dpi=120)
plt.show()'''))

c.append(("md", "## 5. Box — 분포 비교"))
c.append(("code", '''print("증류주 5수 요약:")
print(drinks["spirit"].describe().round(1))

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
drinks[["beer", "spirit", "wine"]].plot(kind="box", ax=axes[0])
axes[0].set_title("주류별 분포")

drinks.boxplot(column="spirit", by="continent", ax=axes[1])
axes[1].set_title("대륙별 증류주 소비량")
axes[1].set_xlabel("")
plt.suptitle("")
fig.tight_layout()
fig.savefig(FIG / "4_3.png", dpi=120)
plt.show()'''))

c.append(("md", "## 6. Line — 추세"))
c.append(("code", '''ufo = pd.read_csv("https://raw.githubusercontent.com/justmarkham/DAT8/master/data/ufo.csv")
print(ufo.shape)

ufo["Time"] = pd.to_datetime(ufo["Time"])
ufo["YearMonth"] = ufo["Time"].dt.to_period("M")

recent = ufo[ufo["Time"] >= "1970-01-01"]
monthly = recent.groupby("YearMonth").size()

fig, ax = plt.subplots(figsize=(11, 4))
monthly.plot(ax=ax, linewidth=1)
ax.set_title("월별 UFO 목격 건수 (1970년 1월 이후)")
ax.set_xlabel("연월")
ax.set_ylabel("목격 건수")
fig.tight_layout()
fig.savefig(FIG / "5_1.png", dpi=120)
plt.show()'''))

c.append(("md", """## 연습 문제

강의자료가 지정한 다섯 문제를 그대로 푼다.

1. `wine` Histogram을 bins 10·20·40으로 비교
2. `beer`–`spirit` Scatter에 `wine`을 크기·색으로 표현
3. 대륙별 `wine` 평균 Bar
4. 대륙별 `spirit` Box — 중앙값과 이상치 비교
5. UFO 연도별 건수에 제목·축이름을 붙여 PNG 저장"""))

c.append(("md", "### 1. wine Histogram — bins 10 / 20 / 40"))
c.append(("code", '''fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
for ax, b in zip(axes, [10, 20, 40]):
    drinks["wine"].plot(kind="hist", bins=b, ax=ax, edgecolor="white", color="#8250df")
    ax.set_title(f"bins={b}")
    ax.set_xlabel("와인 소비량")
fig.suptitle("와인 소비량 분포 — bins에 따른 차이")
fig.tight_layout()
fig.savefig(FIG / "ex1_wine_hist.png", dpi=120)
plt.show()

# bins가 적으면 0 근처에 몰린 것만 보이고, 많으면 중간 봉우리가 드러난다.
print(drinks["wine"].describe().round(1).to_string())'''))

c.append(("md", "### 2. beer–spirit Scatter, wine을 크기·색으로"))
c.append(("code", '''fig, ax = plt.subplots(figsize=(8, 5))
sc = ax.scatter(drinks["beer"], drinks["spirit"],
                s=drinks["wine"] * 0.6 + 12,   # 크기 = 와인
                c=drinks["wine"], cmap="plasma",
                alpha=0.7, edgecolor="white", linewidth=0.5)
ax.set_xlabel("맥주")
ax.set_ylabel("증류주")
ax.set_title("맥주와 증류주의 관계 (크기·색 = 와인)")
fig.colorbar(sc, ax=ax, label="와인 소비량")
fig.tight_layout()
fig.savefig(FIG / "ex2_beer_spirit_wine.png", dpi=120)
plt.show()

print("상관계수 beer-spirit:", round(drinks["beer"].corr(drinks["spirit"]), 3))'''))

c.append(("md", "### 3~4. 대륙별 wine 평균 Bar, spirit Box"))
c.append(("code", '''fig, axes = plt.subplots(1, 2, figsize=(13, 4))

drinks.groupby("continent")["wine"].mean().sort_values().plot(
    kind="barh", ax=axes[0], color="#8250df")
axes[0].set_title("대륙별 평균 와인 소비량")
axes[0].set_xlabel("잔")

drinks.boxplot(column="spirit", by="continent", ax=axes[1])
axes[1].set_title("대륙별 증류주 소비량")
axes[1].set_xlabel("")
plt.suptitle("")
fig.tight_layout()
fig.savefig(FIG / "ex3_4_wine_spirit.png", dpi=120)
plt.show()

# Box plot은 중앙값(가운데 선)과 이상치(점)를 같이 보여 준다
print("대륙별 증류주 중앙값:")
print(drinks.groupby("continent")["spirit"].median().round(1).to_string())'''))

c.append(("md", "### 5. UFO 연도별 — 제목·축이름을 붙여 저장"))
c.append(("code", '''yearly = ufo[ufo["Time"] >= "1970-01-01"].groupby(ufo["Time"].dt.year).size()

fig, ax = plt.subplots(figsize=(11, 4))
yearly.plot(ax=ax, marker="o", markersize=3, linewidth=1.5)
ax.set_title("연도별 UFO 목격 신고 건수 (1970년 이후)")
ax.set_xlabel("연도")
ax.set_ylabel("신고 건수")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(FIG / "ex5_ufo_yearly.png", dpi=120)
plt.show()

print("저장된 그림:", sorted(p.name for p in FIG.glob("*.png")))'''))

print(build("06_matplotlib.ipynb", c).name)
