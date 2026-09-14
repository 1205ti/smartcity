import sys; sys.path.insert(0, "scripts")
from build_notebooks import build

# ── 02 Python 기초 ────────────────────────────────────────────────────────
c = []
c.append(("md", """# 02 : Python 기초

강의자료: `docs/course/02_Python_기초.md`

변수·자료형부터 조건/반복, 자료구조, 함수까지. 데이터 분석에 들어가기 전 문법 기초.
외부 데이터 없이 전부 코드 안에서 돌아간다."""))

c.append(("md", "## 1. print와 문자열 포매팅"))
c.append(("code", '''print("Hello, World!")

# %s 문자열, %d 정수, %.2f 소수점 둘째 자리
name, age, height = "홍길동", 25, 175.456
print("이름: %s, 나이: %d, 키: %.2f" % (name, age, height))

# f-string — 최근에는 이 방식을 더 많이 쓴다
print(f"이름: {name}, 나이: {age}, 키: {height:.2f}")'''))

c.append(("md", "## 2. 변수와 기본 자료형"))
c.append(("code", '''s = "문자열"      # str
i = 42            # int
f = 3.14          # float
b = True          # bool
n = None          # NoneType — 값이 없음을 나타낸다

for v in (s, i, f, b, n):
    print(f"{str(v):8s} {type(v)}")'''))

c.append(("md", "## 3. 문자열 인덱싱과 슬라이싱"))
c.append(("code", '''text = "스마트도시데이터분석"

print(text[0])       # 첫 글자
print(text[-1])      # 마지막 글자
print(text[0:3])     # 0 이상 3 미만
print(text[3:])      # 3부터 끝까지
print(len(text))     # 길이
print(text + " 수업")  # 연결'''))

c.append(("md", "## 4. 연산자"))
c.append(("code", '''a, b = 7, 3

print(f"{a} + {b} = {a + b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b:.4f}")   # 실수 나눗셈
print(f"{a} // {b} = {a // b}")     # 몫
print(f"{a} % {b} = {a % b}")       # 나머지
print(f"{a} ** {b} = {a ** b}")     # 거듭제곱

print(a > b, a == b, a != b)

x, y, z = 1, 2, 3   # 다중 대입
print(x, y, z)'''))

c.append(("md", """## 5. 자료구조 네 가지

| 자료구조 | 표기 | 순서 | 변경 | 중복 |
| --- | --- | --- | --- | --- |
| Tuple | `()` | O | X | O |
| List | `[]` | O | O | O |
| Dictionary | `{k: v}` | O | O | 키 중복 불가 |
| Set | `{}` | X | O | X |"""))

c.append(("code", '''# Tuple — 한 번 만들면 못 바꾼다
t = (1, 2, 3, "네")
print(t, t[0], len(t))

# t[0] = 99  # TypeError: 'tuple' object does not support item assignment'''))

c.append(("code", '''# List — 순서가 있고 바꿀 수 있다
scores = [85, 92, 78, 95, 88]
scores.append(100)
print("추가 후:", scores)

scores.sort()
print("정렬 후:", scores)

scores.sort(reverse=True)
print("내림차순:", scores)

print("95가 있나?", 95 in scores)
print("슬라이싱:", scores[:3])'''))

c.append(("code", '''# Dictionary — 키로 값을 찾는다
student = {"name": "김철수", "age": 20, "major": "도시공학"}

print(student["name"])
print(student.get("grade", "정보 없음"))   # 없는 키는 get으로 안전하게

student["grade"] = "A"    # 추가
print(student)

print("키:", list(student.keys()))
print("값:", list(student.values()))

for k, v in student.items():
    print(f"  {k}: {v}")'''))

c.append(("code", '''# Set — 중복이 없고 순서도 없다
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print("합집합:", a | b)
print("교집합:", a & b)
print("차집합:", a - b)

print("중복 제거:", set([1, 1, 2, 2, 3]))'''))

c.append(("md", "## 6. 조건문"))
c.append(("code", '''score = 85

if score >= 90:
    grade = "A"
elif score >= 80:      # 들여쓰기 4칸이 블록을 만든다
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"점수 {score} → 학점 {grade}")'''))

c.append(("md", "## 7. 반복문 — for"))
c.append(("code", '''for i in range(5):
    print(i, end=" ")
print()

for i in range(2, 10, 2):   # 시작, 끝(미만), 간격
    print(i, end=" ")
print()

# tuple unpacking — 쌍으로 묶인 값을 한 번에 푼다
cities = [("서울", 947), ("부산", 335), ("대구", 238)]
for name, pop in cities:
    print(f"{name}: {pop}만 명")'''))

c.append(("code", '''# continue — 조건에 맞으면 이번 회차를 건너뛴다
for i in range(10):
    if i % 2 == 0:
        continue
    print(i, end=" ")
print()

# 리스트 컴프리헨션 — for문을 한 줄로
squares = [x ** 2 for x in range(1, 6)]
print("제곱:", squares)

evens = [x for x in range(20) if x % 2 == 0]
print("짝수:", evens)'''))

c.append(("md", "## 8. 반복문 — while"))
c.append(("code", '''count = 0
while count < 5:
    print(count, end=" ")
    count += 1
print()

# break — 조건을 만나면 반복을 끝낸다
n = 0
while True:
    n += 1
    if n > 100:
        break
print("멈춘 값:", n)'''))

c.append(("md", "## 9. 함수"))
c.append(("code", '''def greet(name):
    """인사말을 만들어 돌려준다."""
    return f"안녕하세요, {name}님!"

print(greet("홍길동"))


def stats(numbers):
    """여러 값을 한 번에 돌려줄 수 있다. 반환값은 튜플이 된다."""
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

lo, hi, avg = stats([85, 92, 78, 95, 88])
print(f"최소 {lo}, 최대 {hi}, 평균 {avg:.1f}")


def total(*args):
    """*args — 개수를 정하지 않고 받는다."""
    return sum(args)

print(total(1, 2, 3), total(1, 2, 3, 4, 5))'''))

c.append(("md", """## 과제 1 — 소수 판별 함수

`is_prime(n)`을 완성한다. n이 소수면 `True`, 아니면 `False`.

소수는 1과 자기 자신으로만 나누어지는 2 이상의 정수다."""))
c.append(("code", '''def is_prime(n):
    if n < 2:
        return False
    # 약수는 항상 짝을 이루므로 제곱근까지만 확인하면 충분하다.
    # 예를 들어 36 = 4 x 9 에서 4를 확인했다면 9는 볼 필요가 없다.
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


for n in [1, 2, 3, 4, 17, 20, 97, 100]:
    print(f"{n:4d} → {is_prime(n)}")

print("\\n100 이하 소수:", [n for n in range(101) if is_prime(n)])'''))

c.append(("md", """## 과제 2 — 과일가게 매출 계산

중첩 딕셔너리에서 과일별 매출과 총매출을 구한다."""))
c.append(("code", '''fruits = {
    "사과": {"가격": 1500, "판매량": 30},
    "바나나": {"가격": 2000, "판매량": 25},
    "딸기": {"가격": 5000, "판매량": 10},
    "포도": {"가격": 3500, "판매량": 18},
}


def revenue(info):
    """과일 하나의 매출 = 가격 x 판매량"""
    return info["가격"] * info["판매량"]


total_revenue = 0
for name, info in fruits.items():
    r = revenue(info)
    total_revenue += r
    print(f"{name:4s} {info['가격']:>6,}원 x {info['판매량']:3d}개 = {r:>8,}원")

print("-" * 38)
print(f"{'총매출':4s} {total_revenue:>26,}원")

# 매출이 가장 큰 과일 — max에 key를 주면 기준을 바꿀 수 있다
best = max(fruits, key=lambda name: revenue(fruits[name]))
print(f"\\n최대 매출: {best} ({revenue(fruits[best]):,}원)")'''))

p1 = build("02_python_basics.ipynb", c)

# ── 03 NumPy ──────────────────────────────────────────────────────────────
c = []
c.append(("md", """# 03 : NumPy

강의자료: `docs/course/03_NumPy.md`

ndarray 생성·인덱싱·기술통계·axis 방향 계산·원소별 연산·전치.
외부 데이터 없이 배열 리터럴만 쓴다."""))

c.append(("code", "import numpy as np\nprint(np.__version__)"))

c.append(("md", "## 1. 배열 생성"))
c.append(("code", '''arr = np.array([1, 2, 3, 4, 5])
print(arr)
print(type(arr))
print("shape:", arr.shape)   # (5,) — 원소 5개짜리 1차원'''))

c.append(("code", '''# append는 원본을 바꾸지 않고 새 배열을 돌려준다
a = np.array([1, 2, 3])
b = np.append(a, [4, 5])
print("원본:", a)
print("결과:", b)

# 숫자와 문자열을 섞으면 전부 문자열로 승격된다 (dtype은 하나여야 하므로)
mixed = np.append(np.array([1, 2, 3]), ["넷"])
print(mixed, mixed.dtype)'''))

c.append(("md", "## 2. 차원"))
c.append(("code", '''d1 = np.array([1, 2, 3])
d2 = np.array([[1, 2, 3], [4, 5, 6]])
d3 = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])

for name, a in [("1차원", d1), ("2차원", d2), ("3차원", d3)]:
    print(f"{name}  ndim={a.ndim}  shape={a.shape}  크기={a.size}")'''))

c.append(("md", "## 3. 인덱싱"))
c.append(("code", '''arr = np.array([10, 20, 30, 40, 50])
print(arr[0], arr[2], arr[-1])

arr[0] = 99          # 값 수정
print(arr)

m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("2행 3열:", m[1, 2])    # 행, 열 (0부터)
print("2행 전체:", m[1])
print("3열 전체:", m[:, 2])'''))

c.append(("md", "## 4. 슬라이싱"))
c.append(("code", '''arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

print(arr[2:5])      # 2 이상 5 미만
print(arr[:3])       # 처음부터 3 미만
print(arr[7:])       # 7부터 끝까지
print(arr[-3:])      # 뒤에서 3개
print(arr[::2])      # 두 칸씩 건너뛰기'''))

c.append(("md", "## 5. arange"))
c.append(("code", '''print(np.arange(10))
print(np.arange(2, 10))
print(np.arange(0, 20, 5))
print(np.arange(0, 1, 0.25))   # 실수 간격도 된다'''))

c.append(("md", "## 6. 기술통계"))
c.append(("code", '''data = np.array([23, 45, 12, 67, 34, 89, 21, 56])

print(f"개수   {len(data)}")
print(f"합계   {data.sum()}")
print(f"곱     {data.prod()}")
print(f"최소   {data.min()}  (위치 {data.argmin()})")
print(f"최대   {data.max()}  (위치 {data.argmax()})")
print(f"평균   {data.mean():.2f}")
print(f"표준편차 {data.std():.2f}")

for q in (25, 50, 75):
    print(f"{q}% 분위수 {np.percentile(data, q):.2f}")'''))

c.append(("md", """## 7. axis — 어느 방향으로 계산할 것인가

`axis=0`은 행을 따라 내려가며 **열별로**, `axis=1`은 열을 따라 가로지르며 **행별로** 계산한다.
헷갈리면 "사라지는 축"을 생각하면 된다. `axis=0`이면 행 축이 사라져 열만 남는다."""))
c.append(("code", '''m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

print("전체 합계:", m.sum())
print("열별 합계 (axis=0):", m.sum(axis=0))   # 1+4+7, 2+5+8, 3+6+9
print("행별 합계 (axis=1):", m.sum(axis=1))   # 1+2+3, 4+5+6, 7+8+9
print("열별 평균 (axis=0):", m.mean(axis=0))'''))

c.append(("md", "## 8. 원소별 연산"))
c.append(("code", '''a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print("덧셈:", a + b)
print("뺄셈:", b - a)
print("곱셈:", a * b)          # 행렬곱이 아니라 원소별 곱
print("나눗셈:", b / a)
print("스칼라 곱:", a * 10)     # 브로드캐스팅

print("제곱근:", np.sqrt(np.array([1, 4, 9, 16])))
print("자연로그:", np.log(np.array([1, np.e, np.e ** 2])))'''))

c.append(("md", "## 9. 전치"))
c.append(("code", '''m = np.array([[1, 2, 3], [4, 5, 6]])
print("원본", m.shape)
print(m)
print("\\n전치", m.T.shape)
print(m.T)'''))

c.append(("md", """## 과제 1 — 미세먼지 배열 분석

3개 지점 x 4개 시간대의 PM2.5 측정값."""))
c.append(("code", '''pm25 = np.array([[35, 42, 38, 45],    # 지점 1
                 [28, 31, 29, 33],    # 지점 2
                 [52, 58, 61, 55]])   # 지점 3

# 1) 차원과 모양
print(f"ndim={pm25.ndim}  shape={pm25.shape}")

# 2) 두 번째 지점
print("\\n두 번째 지점:", pm25[1])

# 3) 지점별 평균은 행 방향(axis=1), 시간대별 평균은 열 방향(axis=0)
print("\\n지점별 평균:", pm25.mean(axis=1).round(2))
print("시간대별 평균:", pm25.mean(axis=0).round(2))

# 4) 전체 최대값과 위치
#    argmax는 1차원으로 편 기준의 위치를 주므로 unravel_index로 (행, 열)로 되돌린다
flat = pm25.argmax()
row, col = np.unravel_index(flat, pm25.shape)
print(f"\\n최대값 {pm25.max()} — 지점 {row + 1}, 시간대 {col + 1}")

# 5) 전치
print(f"\\n전치 전 {pm25.shape} → 전치 후 {pm25.T.shape}")
print(pm25.T)'''))

p2 = build("03_numpy.ipynb", c)
print(p1.name, p2.name)
