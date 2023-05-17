CC=gcc
CFLAGS=-c -Wall
--
all: filtro_mediana.so run

perf: filtro_mediana.c
    gcc -o filtro_mediana filtro_mediana.c
    ./filtro_mediana input_image.jpg output_image.jpg
    time ./filtro_mediana input_image.jpg output_image.jpg

filtro_mediana.so: filtro_mediana.c
	$(CC) -shared -o filtro_mediana.so filtro_mediana.c

run: filtro_2.py
	python filtro_2.py

clean:
	rm -f *.o *.so
