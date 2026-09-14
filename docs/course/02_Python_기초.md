
# 02 : Python 기초
> Python으로 데이터를 다루기 위한 첫 문법: 값 저장 → 조건 판단 → 반복 처리 → 함수화
💡 
  강의 바로가기
  01 : 환경설정 · 02 : Python 기초 · 03 : NumPy · 04 : Pandas · 05 : API · 06 : Matplotlib · 07 : Plotly · 08 : Folium · 09-1 : 공간데이터와 좌표계 · 09-2 : 지오코딩
💡 
  학습 목표
  - 변수와 기본 자료형을 사용해 값을 저장하고 출력한다.
  - 조건문과 반복문으로 프로그램의 흐름을 제어한다.
  - 리스트·딕셔너리·집합 등 자료구조를 목적에 맞게 선택한다.
  - 반복되는 작업을 함수로 묶어 재사용한다.

## 0. 실습 준비: Jupyter Notebook
Jupyter Notebook은 설명(마크다운)과 실행 가능한 Python 코드 셀을 한 문서에 함께 작성하는 환경입니다. 셀을 위에서 아래 순서로 실행하며, 결과를 확인하고 코드를 조금씩 바꿔 보세요.
```Python
print("Hello, world!")
```
실행 결과
```Plain Text
Hello, world!
```
💡 
  print()는 괄호 안의 값을 화면에 출력합니다. 문자열은 따옴표로 감싸서 표현합니다.

### 출력과 주석
```Python
name = "홍길동"
age = 40
height = 180.1234

print(name)
print("이름은 %s, 나이는 %d세, 키는 %.2fcm입니다." % (name, age, height))

# 한 줄 주석
"""
여러 줄 주석
"""
```
실행 결과
```Plain Text
홍길동
이름은 홍길동, 나이는 40세, 키는 180.12cm입니다.
'\n여러 줄 주석\n'
```
💡 
  %s, %d, %.2f는 각각 문자열·정수·소수 둘째 자리까지의 실수를 출력하는 서식입니다. #은 실제 주석이므로 실행되지 않습니다. 반면 큰따옴표 3개로 만든 내용은 엄밀히 말하면 문자열이므로 Jupyter 셀의 마지막에 단독으로 두면 위처럼 결과로 표시될 수 있습니다.
💡 
  코드가 무엇을 하는지 나중에 다시 이해할 수 있도록, 왜 필요한 코드인지 중심으로 주석을 남깁니다.

## 1. 변수와 기본 자료형
변수는 값을 저장하기 위한 이름입니다. Python은 값을 대입할 때 자료형을 자동으로 판단합니다.
```Python
city = "Seoul"       # 문자열(str)
population = 9335000 # 정수(int)
area = 605.2         # 실수(float)
is_capital = True    # 불리언(bool)
unknown = None       # 아직 값이 없음
```
실행 결과
```Plain Text
(출력 없음)
```
💡 
  값을 변수에 대입만 하는 코드이므로 화면 출력은 없습니다. city, population, area, is_capital, unknown이라는 이름에 서로 다른 자료형의 값이 저장됩니다.

### 문자열(String)
문자열은 작은따옴표 또는 큰따옴표로 만듭니다. 각 문자는 0부터 시작하는 위치(index)로 접근할 수 있습니다.
```Python
text = "hello world"

print(text[0])      # h
print(text[-3])     # r
print(text[0:5])    # hello
print(len(text))    # 11
print("Python" + " is fun!")
```
실행 결과
```Plain Text
h
r
hello
11
Python is fun!
```
💡 
  문자열의 index는 0부터 시작하며 음수 index는 뒤에서부터 셉니다. text[0:5]는 0번부터 5번 직전까지 잘라내고, +는 문자열을 이어 붙입니다.
- 줄바꿈은 \n, 탭은 \t, 따옴표 자체는 \' 또는 \"로 표현합니다.
- 여러 줄 문자열은 큰따옴표 또는 작은따옴표 3개로 감쌉니다.

### 숫자와 연산자
```Python
a = 5
b = 2

print(a + b)  # 덧셈: 7
print(a * b)  # 곱셈: 10
print(a / b)  # 나눗셈: 2.5
print(a // b) # 몫: 2
print(a % b)  # 나머지: 1
print(a ** b) # 거듭제곱: 25
```
실행 결과
```Plain Text
7
10
2.5
2
1
25
```
💡 
  /는 일반 나눗셈, //는 몫, %는 나머지, **는 거듭제곱 연산자입니다. 같은 두 숫자라도 연산자에 따라 결과가 달라집니다.

### 불리언(Boolean)과 비교
조건의 참·거짓은 True, False로 표현합니다.
```Python
temperature = 28

print(temperature > 25)   # True
print(temperature == 30)  # False
print(temperature != 30)  # True
```
실행 결과
```Plain Text
True
False
True
```
💡 
  비교 연산의 결과는 항상 True 또는 False입니다. ==는 같은지 비교하고, !=는 서로 다른지 비교합니다.

### 여러 변수 한 번에 대입하기
```Python
x, y, z = 1, 2, 3.3
print(x, y, z)
```
실행 결과
```Plain Text
1 2 3.3
```
💡 
  Python은 여러 값을 여러 변수에 한 줄로 대응시켜 대입할 수 있습니다. print()에 여러 값을 쉼표로 전달하면 기본적으로 공백을 사이에 두고 출력합니다.

## 2. 자료구조
  | 도시데이터 활용 예 | 표기 | 핵심 특징 | 자료구조 |
  | 변하지 않는 좌표 | ( ) | 순서 있음, 수정 불가 | Tuple |
  | 관측값 목록 | [ ] | 순서 있음, 수정 가능 | List |
  | 지역별 지표 | {key: value} | 키로 값에 접근 | Dictionary |
  | 고유 행정동 목록 | { } / set() | 순서 없음, 중복 제거 | Set |

### Tuple
```Python
coordinate = (37.5665, 126.9780)
print(coordinate[0])

# coordinate[0] = 0  # 오류: tuple은 수정할 수 없음
```
실행 결과
```Plain Text
37.5665
```
💡 
  Tuple도 index로 값을 읽을 수 있지만 생성 후 값을 수정할 수 없습니다. 마지막 줄은 #으로 주석 처리되어 있으므로 오류가 실제로 발생하지 않습니다.

### List
```Python
districts = ["종로구", "중구", "용산구"]
districts.append("성동구")
districts[0] = "강남구"
print(districts)

numbers = [1, 5, 3, 9]
numbers.sort()
print(numbers)
```
실행 결과
```Plain Text
['강남구', '중구', '용산구', '성동구']
[1, 3, 5, 9]
```
💡 
  append()는 리스트 끝에 값을 추가하고, index를 이용하면 기존 값을 바꿀 수 있습니다. sort()는 숫자를 오름차순으로 정렬하며 원본 리스트 자체를 변경합니다.
```Python
print("강남구" in districts)
print("송파구" not in districts)
```
실행 결과
```Plain Text
True
True
```
💡 
  in은 값이 자료구조 안에 있는지, not in은 없는지를 검사합니다. 앞 코드에서 districts에 강남구는 있고 송파구는 없기 때문에 둘 다 True가 됩니다.

### Dictionary
딕셔너리는 키(key) 와 값(value) 을 연결합니다.
```Python
profile = {
    "name": "서울",
    "population": 9335000,
    "area_km2": 605.2
}

print(profile["name"])
print(profile.get("population"))
print(profile.keys())
print(profile.values())

profile["population"] = 9400000
```
실행 결과
```Plain Text
서울
9335000
dict_keys(['name', 'population', 'area_km2'])
dict_values(['서울', 9335000, 605.2])
```
💡 
  딕셔너리는 key로 값에 접근합니다. keys()는 key 목록, values()는 값 목록을 보여 줍니다. 마지막 대입문은 화면 출력 없이 population 값을 9,400,000으로 수정합니다.
```Python
for key, value in profile.items():
    print(key, value)
```
실행 결과
```Plain Text
name 서울
population 9400000
area_km2 605.2
```
💡 
  items()는 딕셔너리의 key와 value를 한 쌍씩 꺼냅니다. 앞 코드에서 인구 값을 수정했기 때문에 반복문에서는 9,400,000이 출력됩니다.

### Set(집합)
집합은 중복을 자동으로 제거하며, 합집합·교집합·차집합 연산에 적합합니다.
```Python
a = {1, 2, 2, 3}
b = {3, 4, 5}

print(a)      # {1, 2, 3}
print(a | b)  # 합집합
print(a & b)  # 교집합
print(a - b)  # 차집합
```
실행 결과 예시
```Plain Text
{1, 2, 3}
{1, 2, 3, 4, 5}
{3}
{1, 2}
```
💡 
  Set은 중복값을 자동으로 제거합니다. |는 합집합, &는 교집합, -는 차집합입니다. Set은 순서를 보장하지 않으므로 출력 순서는 실행 환경에 따라 달라질 수 있습니다.

## 3. 흐름 제어

### 조건문: if · elif · else
조건에 따라 서로 다른 코드를 실행합니다. 들여쓰기(보통 공백 4칸)는 코드 블록을 구분하므로 매우 중요합니다.
```Python
speed = 201

if speed == 99:
    print("적정 속도입니다.")
elif speed > 200:
    print("너무 빠릅니다.")
else:
    print("안전한 속도입니다.")
```
실행 결과
```Plain Text
너무 빠릅니다.
```
💡 
  speed가 99는 아니지만 200보다 크기 때문에 두 번째 조건인 elif speed > 200이 참이 되어 해당 문장만 실행됩니다.

### for 반복문
for문은 정해진 순서의 데이터를 하나씩 꺼내 처리할 때 사용합니다.
```Python
for i in range(5):
    print(i)  # 0부터 4까지

fruits = ["사과", "바나나", "딸기"]
for fruit in fruits:
    print(fruit)
```
실행 결과
```Plain Text
0
1
2
3
4
사과
바나나
딸기
```
💡 
  range(5)는 0부터 4까지의 값을 차례로 만들고, 두 번째 for문은 리스트의 과일을 앞에서부터 하나씩 꺼내 출력합니다.
```Python
pairs = [(1, 2), (3, 4), (5, 6)]

for first, last in pairs:
    print(first + last)
```
실행 결과
```Plain Text
3
7
11
```
💡 
  각 tuple의 두 값을 first, last에 동시에 나누어 담은 뒤 더합니다. 이를 unpacking이라고 합니다.

#### continue와 리스트 컴프리헨션
```Python
numbers = [1, 2, 3, 4]
doubled = []

for number in numbers:
    doubled.append(number * 2)

tripled = [number * 3 for number in numbers]
print(doubled, tripled)
```
실행 결과
```Plain Text
[2, 4, 6, 8] [3, 6, 9, 12]
```
💡 
  첫 번째 방식은 반복문으로 하나씩 추가하고, 두 번째 방식은 리스트 컴프리헨션으로 같은 작업을 한 줄에 표현합니다. 두 방식 모두 기존 값에 계산을 적용한 새 리스트를 만듭니다.
continue는 현재 반복의 나머지를 건너뛰고 다음 반복으로 넘어갑니다.
```Python
for fruit in fruits:
    if fruit == "바나나":
        continue
    print(fruit)
```
실행 결과
```Plain Text
사과
딸기
```
💡 
  바나나를 만났을 때 continue가 실행되어 그 반복의 print()를 건너뜁니다. 반복문 자체는 끝나지 않고 다음 과일인 딸기로 계속 진행합니다.

### while 반복문
조건이 참인 동안 반복합니다. 반복을 끝낼 조건을 반드시 포함해야 합니다.
```Python
i = 0
while i < 5:
    print(i)
    i += 1
```
실행 결과
```Plain Text
0
1
2
3
4
```
💡 
  i < 5가 참인 동안 반복하고 매번 i를 1씩 증가시킵니다. i가 5가 되면 조건이 거짓이 되어 반복이 종료됩니다.
break는 반복문을 즉시 종료합니다.
```Python
coffee = 3

while True:
    coffee -= 1
    print("남은 커피:", coffee)
    if coffee == 0:
        break
```
실행 결과
```Plain Text
남은 커피: 2
남은 커피: 1
남은 커피: 0
```
💡 
  while True는 그대로 두면 무한 반복이지만, 커피가 0이 되는 순간 break가 실행되어 반복문을 즉시 종료합니다.

## 4. 함수
함수는 특정 작업을 이름으로 묶은 코드입니다. 입력값(매개변수)을 받아 결과값을 return할 수 있습니다.
```Python
def add(x, y):
    return x + y

result = add(20, 30)
print(result)
```
실행 결과
```Plain Text
50
```
💡 
  add(20, 30)을 호출하면 함수 안의 return x + y가 50을 반환합니다. 반환된 값은 result에 저장된 뒤 출력됩니다.

### 입력과 반환값의 형태
```Python
def say():
    return "Hi!"

def print_hi():
    print("Hi!")

def calc(a, b):
    return a + b, a * b

sum_value, product_value = calc(1, 2)
print(sum_value, product_value)
```
실행 결과
```Plain Text
3 2
```
💡 
  함수는 정의만 해서는 실행되지 않습니다. 이 코드에서는 calc(1, 2)만 실제 호출되며 합 3과 곱 2를 한 번에 반환합니다. 반환된 두 값은 각각 sum_value, product_value에 나뉘어 저장됩니다.

### 여러 개의 입력 받기
```Python
def mysum(*args):
    total = 0
    for number in args:
        total += number
    return total

print(mysum(1, 2, 3, 4, 5))
```
실행 결과
```Plain Text
15
```
💡 
  *args는 개수가 정해지지 않은 여러 입력값을 tuple로 받습니다. 반복문이 모든 숫자를 total에 누적해 최종 합 15를 반환합니다.
💡 
  return을 실행한 뒤의 코드는 실행되지 않습니다. 하나의 함수 안에서 반환할 값을 모두 만든 후 마지막에 return하세요.

## 실습 과제

### 과제 1. 소수 판별 함수
자연수 하나를 입력받아 소수(1과 자기 자신만 약수로 갖는 수)인지 판별하는 is_prime(n) 함수를 작성해 보세요.
- 소수 예: 2, 3, 5, 7, 11
- for문, 나머지 연산자(%), 조건문을 사용합니다.
- 1은 소수가 아님을 처리합니다.
```Python
def is_prime(n):
    # 여기에 코드를 작성하세요
    pass
```
실행 결과
```Plain Text
(출력 없음)
```
💡 
  현재 코드는 함수의 골격만 정의한 상태입니다. pass는 아무 작업도 하지 않고 넘어가게 하는 문장이므로, 함수를 완성하고 직접 호출하기 전에는 결과가 출력되지 않습니다.

### 과제 2. 과일가게 매출 계산
사과·바나나·오렌지를 각각 10개씩 보유한 가게가 있습니다. 가격은 각각 1,000원·500원·700원입니다.
1. 과일 이름을 키, 가격과 재고를 값으로 하는 딕셔너리를 만드세요.
1. 모든 재고를 판매했을 때 과일별 매출과 총매출을 계산하세요.
1. 가격 또는 재고가 바뀌어도 계산되도록 반복문과 함수를 사용해 보세요.
```Python
fruits = {
    "apple": {"price": 1000, "stock": 10},
    "banana": {"price": 500, "stock": 10},
    "orange": {"price": 700, "stock": 10},
}

# 여기에 매출 계산 코드를 작성하세요
```
실행 결과
```Plain Text
(출력 없음)
```
💡 
  현재 셀은 과일별 가격과 재고를 중첩 딕셔너리로 준비만 합니다. 매출 계산이나 print() 코드가 아직 없기 때문에 화면에 결과는 나오지 않습니다.

## 핵심 정리
- 변수는 값을 저장하고, 자료형은 값을 다루는 방식을 정합니다.
- if는 판단, for와 while은 반복을 담당합니다.
- 리스트는 순서 있는 목록, 딕셔너리는 키-값 정보, 집합은 고유값 처리에 적합합니다.
- 함수는 반복 작업을 재사용 가능하고 읽기 쉬운 코드로 만듭니다.
- 다음 주차의 NumPy·Pandas 분석은 이 네 가지 기초 위에서 시작됩니다.
---
💡 
  이전 강의: 01 : 환경설정
💡 
  다음 강의: 03 : NumPy