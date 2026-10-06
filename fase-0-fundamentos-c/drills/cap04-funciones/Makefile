CC      = gcc
CFLAGS  = -Wall -Wextra -g

SRCS := $(shell find . -name '*.c')
BINS := $(foreach src,$(SRCS),$(dir $(src))build/$(basename $(notdir $(src))))

.PHONY: all clean

all: $(BINS)

define COMPILE_RULE
$(dir $(1))build/$(basename $(notdir $(1))): $(1)
	@mkdir -p $(dir $(1))build
	$(CC) $(CFLAGS) $$< -o $$@
endef

$(foreach src,$(SRCS),$(eval $(call COMPILE_RULE,$(src))))

clean:
	@find . -path '*/build/*' -type f -delete
	@echo "Chapter 4 build limpio."
