"""노트북을 실행해 오류 없이 끝까지 도는지 확인하고 출력을 저장한다."""
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent.parent
for name in sys.argv[1:]:
    path = ROOT / "notebooks" / name
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=600, kernel_name="python3",
                            resources={"metadata": {"path": str(ROOT)}})
    try:
        client.execute()
        nbformat.write(nb, path)
        print(f"OK    {name}")
    except Exception as e:
        msg = str(e).splitlines()
        print(f"FAIL  {name}")
        for line in msg[-12:]:
            print("      " + line)
