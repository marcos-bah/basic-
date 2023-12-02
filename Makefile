.PHONY: bpp

FILE_EXT := $(suffix $(filter-out bpp,$(MAKECMDGOALS)))

bpp:
	@if [ "$(FILE_EXT)" != ".bpp" ]; then \
		echo "Arquivo com extensão inválida! Use .bpp"; \
		exit 1; \
	fi
	@if [ ! -d "logs" ]; then \
		mkdir -p logs; \
	fi
	@python basic.py "$(filter-out $@,$(MAKECMDGOALS))"

%:
	@:
