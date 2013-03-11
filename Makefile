THEDATE=`date +"%B %d, %Y"`
VERSION=0.02
TARFILE=AppTroller_v$(VERSION).tar

all:
	@echo "Type 'make test' to run all unit tests.  You probably don't care to do this, though.  Just run 'python AppTroller.py' for help."

test:	tests

tests:
	cd unit_tests && python ATUnitTests.py && cd ..

release:
	@sed -i "s/APPTROLLER_VERSION = '.*'/APPTROLLER_VERSION = '$(VERSION)'/g" AppTroller.py
	@sed -i "s/APPTROLLER_DATE = '.*'/APPTROLLER_DATE = '$(THEDATE)'/g" AppTroller.py
	@rm -f $(TARFILE).bz2 $(TARFILE).bz2.sig
	@mkdir AppTroller
	@cp *.py AppTroller
	@cp troll.cfg AppTroller
	@cp TODO AppTroller
	@cp README AppTroller
	@cp LICENSE AppTroller
	@cp Makefile AppTroller
	@cp -R unit_tests AppTroller
	@rm -f AppTroller/unit_tests/*~
	@rm -f AppTroller/unit_tests/*.failed
	@tar cf $(TARFILE) AppTroller
	@bzip2 -9 $(TARFILE)
	@rm -rf AppTroller *~
	@gpg -b $(TARFILE).bz2
	@echo
	@echo "Created release: $(TARFILE).bz2"

clean:
	@rm -f *~ *.pyc apktool.jar
