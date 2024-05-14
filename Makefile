@all:
	python -m build --wheel --no-isolation

package:
	python -m build --no-isolation

install:
	python -m installer --destdir="${DESTDIR}" dist/*.whl
