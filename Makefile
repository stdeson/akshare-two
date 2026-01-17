.PHONY: clean build upload test-upload

clean:
	rm -rf dist/ build/ *.egg-info

build: clean
	uv build

upload: build
	uv publish

test-upload: build
	uv publish --publish-url https://test.pypi.org/legacy/
