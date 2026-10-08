CC      = gcc
CFLAGS  = -Wall -Wextra -Werror -g

.PHONY: all clean test

all: build/runlog

build/runlog: src/main.c src/runlog.c
	@mkdir -p build
	$(CC) $(CFLAGS) $^ -o $@

test: build/test_runlog
	./build/test_runlog

build/test_runlog: test/test_runlog.c src/runlog.c
	@mkdir -p build
	$(CC) $(CFLAGS) -fsanitize=address,undefined $^ -o $@

clean:
	@rm -rf build
