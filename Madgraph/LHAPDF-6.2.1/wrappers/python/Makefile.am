EXTRA_DIST = lhapdf.cpp lhapdf.pyx clhapdf.pxd

if WITH_CYTHON
lhapdf.cpp: lhapdf.pyx clhapdf.pxd
	cython lhapdf.pyx --cplus
else
lhapdf.cpp:
	@echo "Not (re)generating lhapdf.cpp since Cython is not installed"
endif



## fixes for out-of-source builds, especially "make distcheck"

FIXSOURCES = $(EXTRA_DIST)

fix-out-of-source: $(FIXSOURCES)
	for i in $^; do \
	  orig="$$i"; \
	  build="$$(basename $$i)"; \
	  if [ ! -e $${build} ]; then cp $${orig} $${build}; \
	  echo $${build} >> $@; fi; \
	done
	touch $@

if WITH_PYTHON

PYEXT_ENV = CC="$(CXX)" CXX="$(CXX)"

## Always force setup.py, it's not good at guessing what needs to rebuild
all-local: fix-out-of-source
	$(PYEXT_ENV) $(PYTHON) setup.py install --install-lib=build/ --force

install-exec-local:
	$(PYEXT_ENV) $(PYTHON) setup.py install --prefix=$(DESTDIR)$(prefix) --force

uninstall-local:
	rm -f $(DESTDIR)$(PYTHON_PATH)/lhapdf.so
	rm -f  $(DESTDIR)$(PYTHON_PATH)/LHAPDF-$(VERSION)-py$(PYTHON_VERSION).egg-info

clean-local: fix-out-of-source
	@rm -f $(builddir)/*.pyc
	@rm -rf $(builddir)/build
	@rm -rf dist
	if [ -e $< ]; then if [ -n "$$(cat $<)" ]; then rm -f $$(cat $<); fi; fi
	rm -f $<

distclean-local:
	@rm -f LHAPDF.egg-info

else

all-local: fix-out-of-source

clean-local: fix-out-of-source
	if [ -e $< ]; then if [ -n "$$(cat $<)" ]; then rm -f $$(cat $<); fi; fi
	rm -f $<

endif
