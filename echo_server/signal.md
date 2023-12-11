### Signal module in python
---
  - *signal* is a means for a prog to receive info from OS
  - *ctrl+c* pressed -> OS creates signal -> sends to prog
  - *signal* module in python describes these signals
  - to see all available signals on the OS:
	```python
	import signal
	print(signal.valid_signals())
	```
  - all signals have a default behaviour, but we can use this module to define it as we want
  - interrupt signal (*SIGINT*), typically *Ctrl+c*, has default behaviour to stop execution of prog. but we can add code which will execute once prog gets the signal
  - for achieving the above, we first define a function to run when the prog is informed of a signal:
	```python
	def signal_handler(signalNumber, frame):
		# <...code here...>
	```
	- OSes assign the signals an integer number, signalNumber refers to this number which is passed by the *signal* function while registering the handler for the signal
	- frame refers to the curr stack frame, it has attr which tell about the code at the time when signal was received.
		- eg: `frame.f_lineno` gives the line no. of code being executed
		      `frame.f_code.co_filename` gives the name of the file being run
  - registering the handler:
	```python
	# syntax
	# signal.signal(signal.<SIGNAME>, handler)

	signal.signal(signal.SIGINT, signal_handler)
	```
