### Notes for the reader
- The bhservice folder contains material provided by the book for testing purpose. At the moment of writing the link provided by the author was not working but I managed to find it online.
- `file_monitor.py` was, accordingly to book notes, inspired by http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
- `PyMI` provides a Python native module wrapper over the Windows Management Infrastructure (MI) API. It includes also a drop-in replacement for the Python WMI module used in the book, proving much faster execution times and no dependency on pywin32. Get it with `pip install PyMI`.
- Had some issues with `import wmi`. You may check here: https://stackoverflow.com/questions/20654047/cant-import-wmi-python-module
- Testing for this chapter is not finished. I am surely able to grab the process in `file_monitor.py` but had not yet successfully tested an injection. 
