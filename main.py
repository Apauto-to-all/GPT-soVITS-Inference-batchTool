import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages.all_pages import AllPages

if __name__ == "__main__":
    app = AllPages()
    app.appRun()
