"""강의별 실습 노트북을 생성한다.

각 노트북은 강의자료(docs/course/)의 실습 흐름을 따라간다.
셀은 (타입, 내용) 튜플 리스트로 정의하고 nbformat으로 조립한다.
"""
import nbformat as nbf
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "notebooks"
OUT.mkdir(exist_ok=True)


def build(filename, cells):
    nb = nbf.v4.new_notebook()
    nb.cells = [nbf.v4.new_markdown_cell(c) if t == "md" else nbf.v4.new_code_cell(c)
                for t, c in cells]
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3.12 (smartcity)",
                       "language": "python", "name": "smartcity"},
        "language_info": {"name": "python", "version": "3.12.13"},
    }
    path = OUT / filename
    nbf.write(nb, path)
    return path
