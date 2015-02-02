class TestExec:
	def __init__(self):
		hasnt_been_initiated = 5
		execfile("test_exec.py")
		print locals()

y = TestExec()
