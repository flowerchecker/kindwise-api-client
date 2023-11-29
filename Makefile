version-patch:
	bump2version patch

version-minor:
	bump2version minor

version-major:
	bump2version major

publish:
	poetry build
	poetry publish
