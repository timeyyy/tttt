# content of test_sample.py
import pytest

class ButtonIndenting:
	
	def f():
		raise SystemExit(1)

	def test_mytest():
		with pytest.raises(SystemExit):
			f()
