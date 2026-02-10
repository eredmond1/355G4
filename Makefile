# Makefile

PYTHON = python3
TARGET = AB

all: $(TARGET)

$(TARGET): AB.py
	echo "#!/usr/bin/env $(PYTHON)" > $(TARGET)
	cat AB.py >> $(TARGET)
	chmod +x $(TARGET)

clean:
	rm -f $(TARGET)