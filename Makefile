PYTHON := python2.7
BUILD_DIR := buildtmp

AURORA_CLUSTER := devel
AURORA_ROLE := $(shell whoami)

UNAME := $(shell uname)

UWSGI_VER = 2.0.10
UWSGI_DIR = uwsgi-$(UWSGI_VER)
UWSGI_FILE = $(UWSGI_DIR).tar.gz
UWSGI_URL = http://projects.unbit.it/downloads/$(UWSGI_FILE)

UWSGI_BUILD_NAME = pex_uwsgi
UWSGI_BUILD_INI_TARGET = buildconf/$(UWSGI_BUILD_NAME).ini

define UWSGI_BUILD_INI
[uwsgi]
main_plugin = python
inherit = base
bin_name = pex_uwsgi
endef

export UWSGI_BUILD_INI
export UWSGI_OPTS_INI

build: clean $(BUILD_DIR) $(UWSGI_FILE)
	cd $(BUILD_DIR) && tar zxvf $(UWSGI_FILE)
	cp pyuwsgi/resources/bootstrap.py $(BUILD_DIR)/$(UWSGI_DIR)/
	echo "$$UWSGI_BUILD_INI" > $(BUILD_DIR)/$(UWSGI_DIR)/$(UWSGI_BUILD_INI_TARGET)
	cd $(BUILD_DIR)/$(UWSGI_DIR) && $(PYTHON) uwsgiconfig.py --build $(UWSGI_BUILD_NAME)
	@echo
	@echo ========================================================
	@echo
	@echo built: $(BUILD_DIR)/$(UWSGI_DIR)/$(UWSGI_BUILD_NAME)
	@echo
	@echo ========================================================
	@echo

build_pydist: build
	cp -avf ./pyuwsgi ./$(BUILD_DIR)/
	cp -avf $(BUILD_DIR)/$(UWSGI_DIR)/$(UWSGI_BUILD_NAME) ./$(BUILD_DIR)/pyuwsgi/resources/
	cp ./$(BUILD_DIR)/$(UWSGI_DIR)/$(UWSGI_BUILD_NAME) ./$(BUILD_DIR)/pyuwsgi/resources/
	cd $(BUILD_DIR)/pyuwsgi && $(PYTHON) setup.py bdist_egg
	[ -d dist ] || mkdir dist
	cp -avf $(BUILD_DIR)/pyuwsgi/dist/*.egg ./dist/
	@echo
	@echo ========================================================
	@echo
	@echo egg dist: ./dist/
	@echo
	@echo ========================================================
	@echo

clean:
	rm -rvf $(BUILD_DIR)

distclean: clean
	rm -rvf dist

$(BUILD_DIR):
	mkdir $(BUILD_DIR)

$(UWSGI_FILE):
	cd $(BUILD_DIR) && wget $(UWSGI_URL)
