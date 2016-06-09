#----------------------- MAKEFILE VARIABLE DEFINITION -------------------------
HELP2MAN     := $(shell which help2man)
SKAFF        := $(shell which skaff)

ifeq (, $(wildcard skaff.1))
	TARGET = skaff.1
else
	TARGET = skaff_new.1
endif
#------------------------------------------------------------------------------

#---------------------------------- RECIPE ------------------------------------
all: help2man

help2man:
ifeq (, $(HELP2MAN))
	$(error "help2man is not available")
endif
ifeq (, $(SKAFF))
	$(error "skaff executable cannot be located")
endif
	-help2man $(SKAFF) > $(TARGET)

help:
	@echo Help
	# Empty recipe for now

#------------------------------------------------------------------------------

#----------------------------- SPECIAL DIRECTIVE ------------------------------
.PHONY: all help2man help
.IGNORE:
#------------------------------------------------------------------------------
