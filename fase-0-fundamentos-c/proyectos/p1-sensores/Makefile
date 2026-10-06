CC      = gcc
CFLAGS  = -Wall -Wextra -g

all: build/sensores

build/sensores: src/main.c
	@mkdir -p build
	$(CC) $(CFLAGS) $< -o $@

clean:
	@rm -rf build
