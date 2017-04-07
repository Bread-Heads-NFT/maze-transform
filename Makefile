test:
	mkdir -p tmp
	python test.py
	./gen 10 10 tmp/grid-10x10-gen.png
	./solve tmp/grid-10x10-gen.png tmp/grid-10x10-gen-solved.png

clean:
	rm -rf ./tmp/

update:
	./update_vendor.sh
