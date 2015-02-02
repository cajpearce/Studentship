class TestExec:
	def __init__(self):
		print locals()
		addend = {}
		addend['hasnt_been_initiated'] = 5
		print locals() + addend
		execfile("test_exec.py")
		print locals()

y = TestExec()
