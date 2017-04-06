test:
	mkdir -p tmp
	python test.py

clean:
	rm -rf ./tmp/

update:
	./update_vendor.sh
