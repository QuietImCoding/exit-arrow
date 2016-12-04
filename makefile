make: app.py utils/dbUtils.py
	#kek

run: make
	python app.py

clean:
	rm -f *~
	rm -f data/*.db
