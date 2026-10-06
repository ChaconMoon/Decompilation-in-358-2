CC      = gcc
CFLAGS  = -Wall -Wextra -g

all: build/runlog

build/runlog: src/main.c
	@mkdir -p build
	$(CC) $(CFLAGS) $< -o $@

clean:
	@rm -rf build
