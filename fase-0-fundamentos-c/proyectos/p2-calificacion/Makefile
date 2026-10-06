CC      = gcc
CFLAGS  = -Wall -Wextra -g

all: build/calificacion

build/calificacion: src/main.c
	@mkdir -p build
	$(CC) $(CFLAGS) $< -o $@

clean:
	@rm -rf build
