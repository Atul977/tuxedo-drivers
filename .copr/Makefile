srpm:
	cd $(CURDIR)

	make package-rpm

	find $(shell rpm --eval "%{_topdir}")/SRPMS/ -name '*.src.rpm' -exec cp {} $(outdir)/ \;

.PHONY: srpm
