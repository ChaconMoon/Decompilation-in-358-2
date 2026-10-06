# ============================================================
#  Makefile Raíz — Decompilation in 358-2
# ============================================================

SUBDIRS := $(shell find fase-0-fundamentos-c -maxdepth 3 -name Makefile)
DIRS    := $(patsubst %/Makefile,%,$(SUBDIRS))

.PHONY: all clean $(DIRS)

all: $(DIRS)

$(DIRS):
	$(MAKE) -C "$@"

clean:
	@for d in $(DIRS); do \
		$(MAKE) -C "$$d" clean; \
	done
