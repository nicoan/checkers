all: install run

# Build engine and install python dependencies
install: venv src/engine/mm.so
	. venv/bin/activate && pip install -r requirements.txt

# Create venv if it does not exist
venv:
	test -d venv || virtualenv -p python2 venv

# Build C engine
src/engine/mm.so:
	gcc -shared -fPIC -O3 src/engine/minimax.c -o src/engine/mm.so

run:
	. venv/bin/activate && cd ./src && python ./main.py && cd ..

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
	find -iname "*.o" -delete
	find -iname "*.so" -delete
