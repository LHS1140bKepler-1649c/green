import cProfile, pstats, io
from functools import wraps
import time

def profile(_save):
    '''A decorator that uses cProfile to profile a function.'''
    def profiling(func):
        @wraps(func)
        def inner(*args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()
            retVal = func(*args, **kwargs)
            pr.disable()
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats()
            print(s.getvalue())
            if _save:
                with open('profiling.txt', 'w') as text:
                    text.write(s.getvalue())
            return retVal
        return inner
    return profiling
	

def timeit(func):
	'''Decorator to measure runtime of a function.'''
	def inner(*args, **kwargs):
		start = time.time()
		retVal = func(*args, **kwargs)
		end = time.time()
		total = end - start
		print(f'Total runtime: {total}')
		return retVal
	return inner